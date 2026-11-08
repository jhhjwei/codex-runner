"""百家号图文（2026-11-08 23:2x 重写：编辑器换代后的实测配方）。

页面现状（都是现读的，别照旧笔记抄）：
  * 标题是 Lexical：`[contenteditable=true]` 且带 `__lexicalEditor`；
    只有 `parseEditorState/setEditorState` 能一次写干净。
  * 正文是 UEditor（iframe#ueditor_0），但 **`window.UE` 已经是 undefined**——
    实例挂在 iframe 自己的窗口上：`iframe.contentWindow.editor`。
    ⇒ 顶层用不了 `UE.getEditor()`，旧写法必然报"UEditor 没加载出来"。
  * 正文插图的对话框在顶层文档（`.cheetah-modal`），里面的 input[type=file]
    是 multiple 的：**必须一次 change 把 N 个文件全灌进去**。
    逐张 change 会累加出重复项，且卡在 0% 让「确认」永远灰着（实测踩过）。
  * 封面：设置封面 → 选择封面 → 弹窗「正文/本地上传」，里面也有一个
    input[type=file]（single），传完点「确定」。
  * 插图确认后图片是以 `<p class="bjh-image-container">` 落在正文里的，
    把它整段 outerHTML 取出来再排进正文，格式由平台自己维持。
"""
from __future__ import annotations

import base64
import json
import mimetypes
import time
from pathlib import Path

from .base import Adapter

CREATE = "https://baijiahao.baidu.com/builder/rc/edit?type=news"
MANAGER = "https://baijiahao.baidu.com/builder/rc/content?type=news"

# ---------- 标题（Lexical） ----------
JS_TITLE_SET = """
const text=arguments[0];
const els=[...document.querySelectorAll('[contenteditable="true"]')].filter(e=>e.__lexicalEditor);
if(!els.length) return -1;
const el=els.sort((a,b)=>a.innerText.length-b.innerText.length)[0];
const ed=el.__lexicalEditor;
const state={root:{children:[{children:[{detail:0,format:0,mode:'normal',style:'',text:text,type:'text',version:1}],
  direction:null,format:'',indent:0,type:'paragraph',version:1,textFormat:0,textStyle:''}],
  direction:null,format:'',indent:0,type:'root',version:1}};
ed.setEditorState(ed.parseEditorState(JSON.stringify(state)));
return el.innerText.length;
"""

JS_TITLE_LEN = """
const els=[...document.querySelectorAll('[contenteditable="true"]')].filter(e=>e.__lexicalEditor);
if(!els.length) return -1;
const el=els.sort((a,b)=>a.innerText.length-b.innerText.length)[0];
return el.innerText.length;
"""

# ---------- 正文（UEditor in iframe） ----------
# 注意：wait() 会把条件包成 `return (...)`，所以这里只能写表达式，不能写语句
JS_ED_READY = """
!!(document.getElementById('ueditor_0') && document.getElementById('ueditor_0').contentWindow
   && document.getElementById('ueditor_0').contentWindow.editor)
"""

JS_BODY_LEN = """
const f=document.getElementById('ueditor_0');
const ed=f && f.contentWindow && f.contentWindow.editor;
return ed? ed.getContentLength(true) : -1;
"""

JS_BODY_SET = """
const f=document.getElementById('ueditor_0');
const ed=f && f.contentWindow && f.contentWindow.editor;
if(!ed) return -1;
ed.setContent(arguments[0]);
return ed.getContentLength(true);
"""

JS_IMG_CONTAINERS = """
// 一张图在正文里会落成两段 p.bjh-image-container（图 + 图注），所以按 img.src 去重
const f=document.getElementById('ueditor_0');
const d=f && f.contentDocument;
if(!d) return JSON.stringify([]);
const seen={}, out=[];
for(const p of d.querySelectorAll('p.bjh-image-container')){
  const img=p.querySelector('img');
  const src=img? img.getAttribute('src') : '';
  if(!src || seen[src]) continue;
  seen[src]=1; out.push(p.outerHTML);
}
return JSON.stringify(out);
"""

JS_BODY_IMGCOUNT = """
const f=document.getElementById('ueditor_0');
const d=f && f.contentDocument;
if(!d) return -1;
const s=new Set([...d.querySelectorAll('p.bjh-image-container img')].map(i=>i.getAttribute('src')));
return s.size;
"""

# ---------- 插图按钮（UEditor 绑的是鼠标事件，el.click() 不触发） ----------
JS_CLICK_IMAGE_BTN = """
const btn=document.querySelector('.edui-for-insertimage');
const t=btn && (btn.querySelector('.edui-icon')||btn);
if(!t) return false;
const r=t.getBoundingClientRect();
const o={bubbles:true,cancelable:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,button:0};
for(const ty of ['mouseover','mousedown','mouseup','click']) t.dispatchEvent(new MouseEvent(ty,o));
return true;
"""

# ---------- 顶层弹窗（插图 / 封面共用） ----------
JS_MODAL_STATE = """
const ms=[...document.querySelectorAll('.cheetah-modal')].filter(m=>m.getBoundingClientRect().width>200);
if(!ms.length) return JSON.stringify({open:false});
const m=ms[ms.length-1];
const btn=[...m.querySelectorAll('button')].find(b=>/^(确认|确定)$/.test((b.innerText||'').trim()));
const st=m.querySelector('.status');
const imgs=[...m.querySelectorAll('img,[role=image]')].filter(e=>e.getBoundingClientRect().width>20).length;
return JSON.stringify({open:true, hasFile:!!m.querySelector('input[type=file]'),
  dis: btn? !!btn.disabled : null, imgs: imgs,
  status: st? (st.innerText||'').replace(/\\s+/g,' ') : ''});
"""

JS_MODAL_FILES = """
const sel='.cheetah-modal-content input[type=file]';
const els=[...document.querySelectorAll(sel)].filter(e=>{
  const m=e.closest('.cheetah-modal');
  return m && m.getBoundingClientRect().width>200;
});
if(!els.length) return -1;
const el=els[els.length-1];
const payload=arguments[0];
const dt=new DataTransfer();
for(const it of payload){
  const bin=atob(it.b64), arr=new Uint8Array(bin.length);
  for(let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i);
  dt.items.add(new File([arr], it.name, {type: it.mime}));
}
el.files=dt.files;
el.dispatchEvent(new Event('change',{bubbles:true}));
return el.files.length;
"""

JS_MODAL_OK = """
const ms=[...document.querySelectorAll('.cheetah-modal')].filter(m=>m.getBoundingClientRect().width>200);
if(!ms.length) return false;
const m=ms[ms.length-1];
const btn=[...m.querySelectorAll('button')].find(b=>/^(确认|确定)$/.test((b.innerText||'').trim()));
if(!btn) return false;
btn.click();
return true;
"""

JS_COVER_CLICK = """
const el=[...document.querySelectorAll('div')].find(e=>(e.innerText||'').trim()==='选择封面' && e.className.indexOf('default')>=0)
  || [...document.querySelectorAll('*')].find(e=>(e.innerText||'').trim()==='更换' && e.getBoundingClientRect().width>0);
if(!el) return false;
el.scrollIntoView({block:'center'});
const r=el.getBoundingClientRect();
const t=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2) || el;
const o={bubbles:true,cancelable:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,button:0};
for(const ty of ['mouseover','mousedown','mouseup','click']) t.dispatchEvent(new MouseEvent(ty,o));
return true;
"""

# 上一轮失败会把弹窗留在 DOM 里（还带着遮罩），再点插图键只会把它关掉/叠加
JS_CLOSE_MODAL = """
const ms=[...document.querySelectorAll('.cheetah-modal')].filter(m=>m.getBoundingClientRect().width>200);
if(!ms.length) return false;
const m=ms[ms.length-1];
const x=m.querySelector('.cheetah-modal-close')
  || [...m.querySelectorAll('button')].find(b=>(b.innerText||'').trim()==='取消');
if(!x) return false;
x.click();
return true;
"""

JS_COVER_STATE = """
const lbl=[...document.querySelectorAll('*')].find(e=>(e.innerText||'').trim()==='设置封面' && e.getBoundingClientRect().width>0);
if(!lbl) return JSON.stringify({found:false, has:false});
let item=lbl; for(let i=0;i<4;i++) item=item.parentElement || item;
const imgs=[...item.querySelectorAll('img')].filter(i=>i.getBoundingClientRect().width>100 && /picproxy|rmb\\.bdstatic/.test(i.src||''));
return JSON.stringify({found:true, has: imgs.length>0});
"""

JS_MODAL_OPEN = """
[...document.querySelectorAll('.cheetah-modal')].some(m=>m.getBoundingClientRect().width>200)
"""

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Baijiahao(Adapter):
    name = "baijiahao"
    kinds = ("article",)
    composer = CREATE
    home = "https://baijiahao.baidu.com/builder/rc/home"
    list_url = MANAGER

    # ---------- 对外 ----------
    def fill(self, pg, t, root, log=print):
        ev = {}
        if not pg.wait(JS_ED_READY, timeout=45):
            raise RuntimeError("[baijiahao] 正文编辑器没出来（可能没登录）")
        pg.sleep(1)
        self._close_modal(pg)

        ev["title_len"] = pg.js(JS_TITLE_SET, t["title"])
        if ev["title_len"] != len(t["title"]):
            raise RuntimeError("[baijiahao] 标题没写准：%s ≠ %d" % (ev["title_len"], len(t["title"])))
        pg.sleep(0.4)

        # 图片：先整体传进弹窗拿服务端地址（确认后才会落到正文里）
        # 先清空正文：页面刷新会带回上一次的草稿（含图），不清就会把旧图算进本次
        rel_imgs = t.get("images") or []
        paths = [str((root / rel).resolve()) for rel in rel_imgs]
        containers = []
        if paths:
            pg.js(JS_BODY_SET, "<p></p>")
            pg.sleep(0.5)
            containers = self._upload_images(pg, paths, log)
            containers = containers[-len(paths):]
            log("[baijiahao] 插图 %d/%d 张" % (len(containers), len(paths)))

        body = self.body_text(t, root).strip()
        html = self._compose(body, containers)
        ev["body_len"] = pg.js(JS_BODY_SET, html)
        log("[baijiahao] 正文 %s（源 %d 字）" % (ev["body_len"], len(body)))
        # 注意：js() 会把 "901.0" 解析成 float，别拿 isinstance(x, int) 判
        if not isinstance(ev["body_len"], (int, float)) or ev["body_len"] < len(body) * 0.8:
            raise RuntimeError("[baijiahao] 正文只进 %s 字（源 %d）" % (ev["body_len"], len(body)))

        # setContent 之后编辑器还要一拍才把图渲染进 DOM，别立刻数
        end = time.time() + 20
        ev["images"] = 0
        while time.time() < end:
            ev["images"] = pg.js(JS_BODY_IMGCOUNT)
            if isinstance(ev["images"], (int, float)) and ev["images"] >= len(paths):
                break
            pg.sleep(1)
        if paths and (ev["images"] or 0) < len(paths):
            raise RuntimeError("[baijiahao] 正文里只有 %s 张图（应 %d）" % (ev["images"], len(paths)))

        cover = t.get("cover")
        if cover:
            # 草稿会带回上次设过的封面，这时页面上只有「更换」，再点反而打不开弹窗
            st = pg.js(JS_COVER_STATE) or {}
            if st.get("has"):
                ev["cover"] = "kept"
                log("[baijiahao] 封面已在（草稿带回），不重设")
            else:
                self._set_cover(pg, str((root / cover).resolve()), log)
                ev["cover"] = True
        return ev

    def verify(self, pg, t, root):
        return {
            "title_len": pg.js(JS_TITLE_LEN),
            "body_len": pg.js(JS_BODY_LEN),
            "images": pg.js(JS_BODY_IMGCOUNT),
        }

    def submit(self, pg, t, log=print):
        # 只点一次：点完页面会跳到 /builder/rc/clue（首发后的推荐页），再点会重复提交
        self.click_text(pg, "发布", exact=True, timeout=8, log=log)
        log("[baijiahao] 已点发布，等结果…")
        return self.wait_result(
            pg, ["/builder/rc/clue", "/content", "/success"],
            ["已经发布成功", "发布成功", "提交成功"],
            ["发布失败", "请填写", "不能为空", "标题不能", "审核不通过"], timeout=120)

    def readback(self, pg, title, log=print):
        pg.open(MANAGER)
        pg.sleep(4)
        body = pg.body_text(6000)
        found = title in body
        row = None
        if found:
            i = body.index(title)
            row = body[max(0, i - 120):i + 220]
        return {"found": found, "row": row, "url": pg.url()}

    # ---------- 内部 ----------
    def _compose(self, body, containers):
        """正文按空行切段；图片平均排在段落之间（不挤在开头，也不全堆结尾）。"""
        paras = [p.strip() for p in body.replace("\r\n", "\n").split("\n\n") if p.strip()]
        out = ['<p>%s</p>' % _esc(p).replace("\n", "<br>") for p in paras]
        if containers and out:
            n, m = len(containers), len(out)
            # 第 i 张图放在第 round((i+1)*m/(n+1)) 段之后
            buckets = {}
            for i, c in enumerate(containers):
                pos = int(round((i + 1) * m / (n + 1))) - 1
                pos = max(0, min(m - 1, pos))
                buckets.setdefault(pos, []).append(c)
            merged = []
            for idx, p in enumerate(out):
                merged.append(p)
                merged.extend(buckets.get(idx, []))
            out = merged
        elif containers:
            out = containers
        return "".join(out)

    def _wait_modal(self, pg, timeout=20, need_status=False):
        end = time.time() + timeout
        last = {}
        while time.time() < end:
            st = pg.js(JS_MODAL_STATE)
            if isinstance(st, str):
                st = json.loads(st)
            last = st or {}
            if last.get("open") and last.get("hasFile"):
                if not need_status or last.get("dis") is False:
                    return last
            time.sleep(0.5)
        return last

    def _payload(self, paths):
        out = []
        for p in paths:
            raw = Path(p).read_bytes()
            out.append({
                "b64": base64.b64encode(raw).decode(),
                "name": Path(p).name,
                "mime": mimetypes.guess_type(p)[0] or "image/png",
            })
        return out

    def _close_modal(self, pg):
        if pg.js(JS_MODAL_OPEN):
            pg.js(JS_CLOSE_MODAL)
        end = time.time() + 8
        while time.time() < end and pg.js(JS_MODAL_OPEN):
            pg.sleep(0.5)

    def _open_image_modal(self, pg, log=print):
        """关掉残留弹窗再点插图键；点不亮就重来（遮罩动画没退干净时第一下会被吃掉）。"""
        st = {}
        for attempt in range(3):
            self._close_modal(pg)
            pg.sleep(0.5)
            if not pg.js(JS_CLICK_IMAGE_BTN):
                raise RuntimeError("[baijiahao] 找不到插图按钮")
            pg.sleep(1.5)
            st = self._wait_modal(pg, timeout=8)
            if st.get("hasFile"):
                return st
            log("[baijiahao] 插图弹窗第 %d 次没开，重试" % (attempt + 1))
        raise RuntimeError("[baijiahao] 插图弹窗没出来")

    def _upload_images(self, pg, paths, log=print):
        self._open_image_modal(pg, log)
        pg.sleep(0.5)

        n = pg.js(JS_MODAL_FILES, self._payload(paths))
        if n != len(paths):
            raise RuntimeError("[baijiahao] 只塞进 %s 个文件（应 %d）" % (n, len(paths)))
        log("[baijiahao] 塞入 %d 张，等上传…" % n)

        end = time.time() + 40
        while time.time() < end:
            st = pg.js(JS_MODAL_STATE)
            if isinstance(st, str):
                st = json.loads(st)
            if st.get("dis") is False:
                break
            time.sleep(1)
        if st.get("dis") is not False:
            raise RuntimeError("[baijiahao] 上传没完成（确认键一直灰着）：%s" % st.get("status"))

        pg.js(JS_MODAL_OK)
        pg.sleep(3)
        containers = pg.js(JS_IMG_CONTAINERS)
        if isinstance(containers, str):
            containers = json.loads(containers)
        return containers or []

    def _set_cover(self, pg, path, log=print):
        st = {}
        for attempt in range(3):
            self._close_modal(pg)
            if not pg.js(JS_COVER_CLICK):
                raise RuntimeError("[baijiahao] 找不到「选择封面」")
            pg.sleep(2)
            st = self._wait_modal(pg, timeout=8)
            if st.get("hasFile"):
                break
        if not st.get("hasFile"):
            raise RuntimeError("[baijiahao] 封面弹窗没出来")
        n = pg.js(JS_MODAL_FILES, self._payload([path]))
        if n != 1:
            raise RuntimeError("[baijiahao] 封面没塞进上传框")
        end = time.time() + 30
        while time.time() < end:
            st = pg.js(JS_MODAL_STATE)
            if isinstance(st, str):
                st = json.loads(st)
            if st.get("imgs", 0) >= 1 and st.get("dis") is False:
                break
            time.sleep(1)
        pg.js(JS_MODAL_OK)
        pg.sleep(2.5)
        log("[baijiahao] 封面已选：%s" % Path(path).name)
