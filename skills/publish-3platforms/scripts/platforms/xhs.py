"""小红书图文笔记。

2026-11-08 21:17 真发过一次，三个硬点：
  * 发布键在 closed shadow root 里：el.shadowRoot 是 null，`el._sr` 才拿得到（WebKit 私有属性）；
  * 标题是受控 input，必须走原生 value setter + input 事件；
  * 正文是 Quill（div.ql-editor），要派发 paste，否则字数统计不更新、发布键可能不亮。
"""
from __future__ import annotations

import time

from .base import Adapter

CREATE = "https://creator.xiaohongshu.com/publish/publish?source=official"
MANAGER = "https://creator.xiaohongshu.com/new/note-manager"

EDITOR = "div.tiptap.ProseMirror, div.ql-editor"

JS_TITLE_LEN = """
const el=[...document.querySelectorAll('input')].find(i=>/标题/.test(i.placeholder||''));
return el? el.value.length : -1;
"""

JS_THUMBS = "new Set([...document.querySelectorAll('img')].map(i=>i.src).filter(s=>s.startsWith('blob:'))).size"

JS_PUBLISH = """
let el=null;
const b=document.querySelector('xhs-publish-btn');
if(b){
  const sr=b.shadowRoot||b._sr;
  if(sr) el=[...sr.querySelectorAll('button')].find(x=>/发布/.test(x.innerText||''));
}
if(!el) el=[...document.querySelectorAll('button')].filter(x=>/发布/.test(x.innerText||'')&&x.getBoundingClientRect().width>40).pop();
if(!el) return false;
el.scrollIntoView({block:'center'}); el.click(); return true;
"""


class Xhs(Adapter):
    name = "xhs"
    kinds = ("note",)
    composer = CREATE
    home = "https://creator.xiaohongshu.com/new/home"
    list_url = MANAGER

    def open(self, pg, log=print):
        pg.open(CREATE)
        pg.sleep(3)
        # 默认停在「上传视频」。页面里同组 tab 有重复节点，必须按"在视口内"挑那个再点。
        for _ in range(3):
            pg.js("""
            const tabs=[...document.querySelectorAll('.creator-tab')].filter(e=>{
              const r=e.getBoundingClientRect();
              return /上传图文/.test(e.innerText||'') && r.x>0 && r.y>0 && r.width>4;
            });
            if(tabs.length){ tabs[0].click(); return true; }
            return false;
            """)
            pg.sleep(2)
            if pg.wait_sel("input[type=file][multiple], input[type=file][accept*='image']", 4):
                return pg.url()
        log("[xhs] 没能切到「上传图文」，当前仍是视频上传")
        return pg.url()

    def fill(self, pg, t, root, log=print):
        ev = {}
        imgs = self.image_paths(t, root)
        if imgs:
            if not pg.wait_sel("input[type=file]", 15):
                raise RuntimeError("[xhs] 没等到图片上传框")
            before = pg.count(JS_THUMBS)
            n = pg.upload("input[type=file]", imgs, wait_before=1.0)
            ev["images_in_input"] = n
            pg.sleep(3)
            after = pg.count(JS_THUMBS)
            ev["blob_before"], ev["blob_after"] = before, after
            log("[xhs] 图片进了 %s 张（页面新增 blob %s 个）" % (n, after - before))
            if after - before < len(imgs):
                raise RuntimeError("[xhs] 图片只进了 %s/%d，停手不硬发" % (after - before, len(imgs)))

        ev["title_len"] = pg.set_input("input[placeholder*='标题']", t["title"])
        if ev["title_len"] != len(t["title"]):
            ev["title_len"] = pg.js(JS_TITLE_LEN)
        if ev["title_len"] != len(t["title"]):
            raise RuntimeError("[xhs] 标题没写准：%s ≠ %d" % (ev["title_len"], len(t["title"])))
        pg.sleep(0.5)

        body = self.body_text(t, root).strip()
        ev["body_len"] = pg.set_editor(EDITOR, body)
        log("[xhs] 正文 %s 字（源 %d）" % (ev["body_len"], len(body)))
        if ev["body_len"] < len(body) * 0.8:
            raise RuntimeError("[xhs] 正文没灌进去：%s" % ev["body_len"])

        for topic in (t.get("topics") or []):
            try:
                self._topic(pg, topic)
                ev.setdefault("topics", []).append(topic)
            except Exception as e:
                log("[xhs] 话题「%s」没加上（不挡发布）：%s" % (topic, e))
        return ev

    def _topic(self, pg, topic):
        if not pg.click_text("话题", exact=False, timeout=4):
            raise RuntimeError("没有话题按钮")
        pg.sleep(1)
        if not pg.wait_sel("input[placeholder*='话题']", 6):
            raise RuntimeError("没有话题输入框")
        pg.set_input("input[placeholder*='话题']", "#" + topic)
        pg.sleep(1.5)
        pg.click_text("#" + topic, exact=False, timeout=4, scope="li,div,span")

    def verify(self, pg, t, root):
        return {"title_len": pg.js(JS_TITLE_LEN), "body_len": pg.text_len(EDITOR), "thumbs": pg.count(JS_THUMBS)}

    def submit(self, pg, t, log=print):
        if not pg.js(JS_PUBLISH):
            raise RuntimeError("[xhs] 找不到发布键")
        log("[xhs] 已点发布，等结果…")
        return self.wait_result(pg, ["publish/success", "note-manager"], ["发布成功", "提交成功"], ["发布失败", "不能为空", "请上传"])

    def readback(self, pg, title, log=print):
        pg.open(MANAGER)
        pg.sleep(4)
        body = pg.body_text(4000)
        found = title in body
        row = None
        if found:
            i = body.index(title)
            row = body[max(0, i - 100):i + 160]
        return {"found": found, "row": row, "url": pg.url()}
