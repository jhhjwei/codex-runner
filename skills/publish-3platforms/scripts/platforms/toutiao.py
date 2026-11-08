"""今日头条 · 微头条（v1 只做这个体裁）。

2026-11-08 21:31 真发过一条：1700 字、3 张图。踩到的坑：
  * 编辑器是 ProseMirror：改 innerText 不进模型，必须派发 paste（带 text/html）；预置草稿要先清；
  * 图片抽屉缩略图不是 <img>，是 div.item 的 background-image，数图只能数 div.item；
  * **每点一次「确定」都把整批再插一遍**——今天因此多出 9 张、点了 6 次删除键才回到 3 张。
    所以这里严格只点一次，并在插入后回数正文里的图片数，多了立刻报错。
  * 头条长图文（内嵌图）v1 不做：那次内嵌图上传失败，降级成了微头条。
"""
from __future__ import annotations

import time

from .base import Adapter

CREATE = "https://mp.toutiao.com/profile_v4/weitoutiao/publish"
MANAGER = "https://mp.toutiao.com/profile_v4/weitoutiao"

JS_BODY_LEN = """
const el=document.querySelector('.ProseMirror');
return el? (el.innerText||'').length : -1;
"""

JS_TILES = "document.querySelectorAll('.upload-list .img-box-item, .upload-list .item, .btn-upload-list .item, .pic-select-image-item-wrap').length"

JS_OPEN_DRAWER = """
const b=document.querySelector('.weitoutiao-image-plugin');
const t=b && (b.querySelector('.syl-toolbar-button') || b);
if(!t) return false;
const r=t.getBoundingClientRect();
const o={bubbles:true,cancelable:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,button:0};
for(const ty of ['mouseover','mouseenter','mousedown','mouseup','click']) t.dispatchEvent(new MouseEvent(ty,o));
return true;
"""

JS_PICK_ONE = """
const els=[...document.querySelectorAll('input[type=file]')].filter(e=>{
  const p=e.closest('.upload-image-panel'); return p && p.getBoundingClientRect().width>200;
});
if(!els.length) return -1;
const bin=atob(arguments[0]), arr=new Uint8Array(bin.length);
for(let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i);
const dt=new DataTransfer();
dt.items.add(new File([arr], arguments[1], {type:'image/png'}));
const el=els[0];
el.files=dt.files;
el.dispatchEvent(new Event('change',{bubbles:true}));
return 1;
"""

JS_UPLOADED_COUNT = """
const p=document.querySelector('.upload-image-panel');
if(!p) return 0;
const m=/已上传 (\\d+) 张/.exec(p.innerText||'');
return m? parseInt(m[1]) : 0;
"""

JS_CONFIRM_UP = """
[...document.querySelectorAll('[class*=modal],[class*=dialog],[class*=Dialog]')]
  .some(el=>el.getBoundingClientRect().width>200 && /确定发布|确认发布/.test(el.innerText||''))
"""

JS_INSERTED = """
const el=document.querySelector('.ProseMirror');
if(!el) return -1;
return el.querySelectorAll('img, [data-type=image]').length;
"""


class Toutiao(Adapter):
    name = "toutiao"
    kinds = ("weitoutiao",)
    composer = CREATE
    home = "https://mp.toutiao.com/profile_v4/index"
    list_url = MANAGER

    def fill(self, pg, t, root, log=print):
        ev = {}
        if not pg.wait_sel(".ProseMirror", 40):
            raise RuntimeError("[toutiao] 编辑器没出来（可能没登录）")
        pg.sleep(1.5)

        body = self.body_text(t, root).strip()
        if not pg.clear_editor(".ProseMirror"):
            raise RuntimeError("[toutiao] 旧草稿清不掉，别再 paste（会变两遍）")
        ev["body_len"] = pg.set_editor(".ProseMirror", body)
        log("[toutiao] 正文 %s 字（源 %d）" % (ev["body_len"], len(body)))
        if ev["body_len"] < len(body) * 0.8:
            raise RuntimeError("[toutiao] 正文没灌进去：%s" % ev["body_len"])
        if ev["body_len"] > len(body) * 1.2:
            raise RuntimeError("[toutiao] 正文重复了：%s 字，源 %d（草稿没清干净）" % (ev["body_len"], len(body)))

        imgs = self.image_paths(t, root)
        if imgs:
            # 2026-11-08 23:4x 实测：屏幕锁了（visibilityState=hidden / hasFocus=false）时，
            # 图片抽屉能传能开，但点「确定」只关窗不落图 —— 插入走的是 ProseMirror 的焦点路径。
            # 这种情况不硬发图，只发文字，并把原因记进结果，别让调用方以为图进去了。
            vis = pg.js("return document.visibilityState")
            if vis != "visible":
                ev["images_skipped"] = "页面不可见（%s），头条插图落不了，只发文字" % vis
                log("[toutiao] 跳过插图：%s" % ev["images_skipped"])
                return ev
            ev["images_in_body"] = self._images(pg, imgs, log)
        return ev

    def _images(self, pg, paths, log):
        # 图片键绑的是鼠标事件：el.click() 打不开抽屉，要整串 mouseover/mousedown/mouseup/click
        if not pg.js(JS_OPEN_DRAWER):
            raise RuntimeError("[toutiao] 找不到图片键")
        pg.sleep(2.5)
        if not pg.wait_sel(".upload-image-panel input[type=file]", 15):
            raise RuntimeError("[toutiao] 图片抽屉里没有文件输入框")
        # 抽屉只认单张：一次塞多张进 input.files 会被清空（实测 files.length=0）
        for i, p in enumerate(paths, 1):
            self._one(pg, p, i, log)
        log("[toutiao] 抽屉里排到 %s 张" % pg.count(JS_TILES))
        # 只点一次「确定」：多一次就整批重插
        self.click_text(pg, "确定", exact=True, timeout=8, log=log)
        pg.sleep(3)
        n = pg.count(JS_INSERTED)
        log("[toutiao] 正文里已插入 %s 张" % n)
        if n > len(paths):
            raise RuntimeError("[toutiao] 图多插了：正文 %s，源 %d（确定点多了）" % (n, len(paths)))
        return n

    def _one(self, pg, path, idx, log):
        import base64
        raw = base64.b64encode(open(path, "rb").read()).decode()
        pg.js(JS_PICK_ONE, raw, path.rsplit("/", 1)[-1])
        end = time.time() + 15
        while time.time() < end:
            got = pg.js(JS_UPLOADED_COUNT)
            if isinstance(got, (int, float)) and got >= idx:
                return
            pg.sleep(1)
        raise RuntimeError("[toutiao] 第 %d 张没传完" % idx)

    def verify(self, pg, t, root):
        return {"body_len": pg.js(JS_BODY_LEN), "images_in_body": pg.count(JS_INSERTED)}

    def submit(self, pg, t, log=print):
        # 只点一次：多平台实测点第二下会重复提交
        self.click_text(pg, "发布", exact=True, timeout=8, log=log)
        pg.sleep(2)
        # 有的版本会再弹一个「确定发布」，只在真弹了的时候点一次
        if pg.js(JS_CONFIRM_UP):
            self.click_text(pg, "确定", exact=True, timeout=3, log=log)
        log("[toutiao] 已点发布，等结果…")
        return self.wait_result(pg, ["/weitoutiao"], ["发布成功", "审核中", "提交成功"],
                               ["发布失败", "不能为空", "请填写"], not_url_bits=["/publish"])

    def readback(self, pg, title, log=print):
        # 微头条没有标题字段，needle 是正文开头（publish.py 会传）
        needle = (title or "")[:12]
        pg.open(MANAGER)
        pg.sleep(4)
        body = pg.body_text(6000)
        found = bool(needle) and needle in body
        row = None
        if found:
            i = body.index(needle)
            row = body[max(0, i - 80):i + 200]
        return {"found": found, "needle": needle, "row": row, "url": pg.url()}
