"""Page：把"人怎么操作网页"抽象成几个动作，底层走 Safari 的 AppleScript 通道。

为什么不用 WebDriver 了（2026-11-08 实测负面结论）：
  macOS 27.2 上 `AllowRemoteAutomation` 已是 true、`safaridriver --enable` 返回 0，
  但 POST /session 仍报 "You must enable 'Allow remote automation'"。换了 cfprefsd 重启、
  杀掉旧 driver、Safari 重启都无效。⇒ WebDriver 在这台机器上不可用，别再试。

剩下的路只有一条：osascript 的 `do JavaScript`。它已验证可用，且支持：
  * 同步读 DOM、改 DOM、触发 click；
  * 用 File + DataTransfer 把本地文件塞进 input.files（实测页面 change 事件正常触发）。

上传的实现在这里：文件读成 base64 → 注入页面 → File → DataTransfer → input.files → change。
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import time
from pathlib import Path

from .applescript import Safari, AScriptError

JS_FIND = """
const el=document.querySelector(arguments[0]);
return el? true : false;
"""

JS_CLICK = """
const el=document.querySelector(arguments[0]);
if(!el) return false;
el.scrollIntoView({block:'center'});
el.click();
return true;
"""

JS_CLICK_TEXT = """
const want=arguments[0], exact=arguments[1], scope=arguments[2]||'button,a,[role=button],div,span,li';
const all=[...document.querySelectorAll(scope)];
for(const el of all){
  const t=(el.innerText||'').trim();
  if(exact? t===want : t.includes(want)){
    const r=el.getBoundingClientRect();
    // 只看真在视口里的：小红书这类页面会把同一组 tab 复制一份丢到 -9000 处
    if(r.width>4&&r.height>4&&r.x>-1&&r.y>-1&&r.x<window.innerWidth&&r.y<window.innerHeight){
      el.scrollIntoView({block:'center'}); el.click(); return true;
    }
  }
}
return false;
"""

JS_SET_INPUT = """
const el=document.querySelector(arguments[0]);
if(!el) return -1;
el.focus();
const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
setter.call(el, arguments[1]);
el.dispatchEvent(new Event('input',{bubbles:true}));
el.dispatchEvent(new Event('change',{bubbles:true}));
el.dispatchEvent(new Event('blur',{bubbles:true}));
return el.value.length;
"""

JS_CLEAR_EDITOR = """
const el=document.querySelector(arguments[0]);
if(!el) return -1;
el.focus();
document.execCommand('selectAll');
document.execCommand('delete');
return (el.innerText||'').length;
"""

JS_SET_EDITOR = """
const el=document.querySelector(arguments[0]);
if(!el) return -1;
const text=arguments[1];
el.focus();
// 先清干净：草稿会被页面自动带回，只 paste 会变成"旧稿+新稿"两遍
document.execCommand('selectAll');
document.execCommand('delete');
try{
  const dt=new DataTransfer();
  dt.setData('text/plain', text);
  const html=text.split(/\\n{2,}/).map(p=>'<p>'+p.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>')+'</p>').join('');
  dt.setData('text/html', html);
  el.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));
}catch(e){}
let n=(el.innerText||'').length;
if(n < text.length*0.8){ document.execCommand('insertText', false, text); n=(el.innerText||'').length; }
return n;
"""

# 先把文件灌进 input.files（不点开原生选择框），再派发 change
JS_UPLOAD_ONE = """
const sel=arguments[0], b64=arguments[1], name=arguments[2], mime=arguments[3];
const el=document.querySelector(sel);
if(!el) return -1;
const bin=atob(b64), arr=new Uint8Array(bin.length);
for(let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i);
const file=new File([arr], name, {type: mime});
const dt=new DataTransfer();
if(el.multiple){ for(const f of (window.__PQ||[])) dt.items.add(f); }
dt.items.add(file);
window.__PQ=[...dt.files];
const dt2=new DataTransfer();
for(const f of window.__PQ) dt2.items.add(f);
el.files=dt2.files;
el.dispatchEvent(new Event('change',{bubbles:true}));
return el.files.length;
"""

JS_UPLOAD_RESET = "window.__PQ=[]; return true;"


class Page:
    def __init__(self, safari: Safari, log=print):
        self.s = safari
        self.log = log

    # ---------- 基础 ----------
    def open(self, url, wait=2.0):
        self.s.open(url)
        self.s.wait_ready(40)
        time.sleep(wait)
        return self.url()

    def url(self):
        return self.s.url()

    def js(self, code, *args, timeout=60):
        return self.s.js(code, *args, timeout=timeout)

    def sleep(self, t):
        time.sleep(t)

    def wait(self, cond, timeout=30):
        return self.s.wait_js(cond, timeout=timeout)

    def wait_sel(self, css, timeout=20):
        return self.s.wait_js("!!document.querySelector(%s)" % json.dumps(css), timeout=timeout)

    # ---------- 读 ----------
    def exists(self, css):
        try:
            return bool(self.js(JS_FIND, css))
        except AScriptError:
            return False

    def count(self, js_expr):
        try:
            return int(self.js("return (%s)" % js_expr) or 0)
        except (AScriptError, TypeError, ValueError):
            return -1

    def text_len(self, css):
        try:
            return int(self.js("""
            const el=document.querySelector(arguments[0]);
            return el? ((el.innerText && el.innerText.length) ? el.innerText.length : (el.value||'').length) : -1;
            """, css) or -1)
        except (AScriptError, TypeError, ValueError):
            return -1

    def body_text(self, limit=600):
        try:
            return self.js("return (document.body?document.body.innerText:'').slice(0,%d)" % limit) or ""
        except AScriptError:
            return ""

    def scan(self):
        """把页面上的输入框和按钮列出来，用于 probe 校准选择器。"""
        return {
            "inputs": self.js("""
            const out=[];
            for(const el of document.querySelectorAll('input,textarea,[contenteditable="true"]')){
              const r=el.getBoundingClientRect(); if(r.width<2||r.height<2) continue;
              out.push({tag:el.tagName.toLowerCase(), type:el.type||'', ph:el.placeholder||'',
                        cls:(el.className||'').toString().slice(0,60), len:(el.innerText||el.value||'').length});
            }
            return JSON.stringify(out.slice(0,40));
            """),
            "buttons": self.js("""
            const out=[], seen={};
            for(const el of document.querySelectorAll('button,a,[role=button]')){
              const r=el.getBoundingClientRect(); if(r.width<8||r.height<8) continue;
              const t=(el.innerText||'').trim(); if(!t||t.length>20) continue;
              if(seen[t]) continue; seen[t]=1; out.push(t);
            }
            return JSON.stringify(out.slice(0,40));
            """),
        }

    # ---------- 点 ----------
    def click(self, css):
        return bool(self.js(JS_CLICK, css))

    def click_text(self, text, exact=True, scope=None, timeout=8):
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.js(JS_CLICK_TEXT, text, exact, scope):
                    self.log("[page] 点「%s」" % text)
                    return True
            except AScriptError:
                pass
            time.sleep(0.5)
        return False

    # ---------- 写 ----------
    def set_input(self, css, text):
        return self.js(JS_SET_INPUT, css, text)

    def set_editor(self, css, text):
        return self.js(JS_SET_EDITOR, css, text)

    def clear_editor(self, css, tries=4):
        """把富文本清空；页面会把草稿自动带回来，不清就直接 paste 会变成两遍。"""
        n = -1
        for _ in range(tries):
            try:
                n = self.js(JS_CLEAR_EDITOR, css)
            except AScriptError:
                n = -1
            if isinstance(n, (int, float)) and n <= 5:
                return True
            time.sleep(0.8)
        return False

    # ---------- 上传 ----------
    def upload(self, css, paths, timeout=30, wait_before=0.5):
        """逐张灌进 input.files。返回最终 files.length。"""
        paths = [os.path.abspath(p) for p in paths]
        for p in paths:
            if not os.path.exists(p):
                raise FileNotFoundError(p)
        self.js(JS_UPLOAD_RESET)
        n = 0
        for p in paths:
            raw = Path(p).read_bytes()
            mime = mimetypes.guess_type(p)[0] or "image/png"
            n = self.js(JS_UPLOAD_ONE, css, base64.b64encode(raw).decode(), os.path.basename(p), mime)
            if n == -1:
                raise AScriptError("上传框不存在：%s" % css)
            self.log("[page] 塞入 %s（input.files=%s）" % (os.path.basename(p), n))
            time.sleep(wait_before)
        return n
