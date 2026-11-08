"""平台适配器基类：probe / open / fill / verify / submit / readback 六步。"""
from __future__ import annotations

import time
from pathlib import Path


class Adapter:
    name = ""
    kinds: tuple = ()
    composer = ""
    home = ""
    list_url = ""
    login_url = ""

    # ---- 探测 ----
    def probe(self, pg, log=print):
        pg.open(self.home or self.composer)
        pg.sleep(2)
        scan = pg.scan()
        body = pg.body_text(500)
        url = pg.url()
        logged_in = not any(k in url.lower() for k in ("login", "passport", "sso", "signin")) \
            and not any(k in body for k in ("扫码登录", "请登录", "登录后"))
        return {
            "platform": self.name,
            "url": url,
            "logged_in": logged_in,
            "body_head": body,
            "inputs": scan.get("inputs"),
            "buttons": scan.get("buttons"),
        }

    # ---- 打开 ----
    def open(self, pg, log=print):
        pg.open(self.composer)
        pg.sleep(2)
        return pg.url()

    # ---- 子类实现 ----
    def fill(self, pg, t, root, log=print):
        raise NotImplementedError

    def verify(self, pg, t, root):
        raise NotImplementedError

    def submit(self, pg, t, log=print):
        raise NotImplementedError

    def readback(self, pg, title, log=print):
        raise NotImplementedError

    # ---- 公共 ----
    @staticmethod
    def body_text(t, root):
        p = Path(root) / (t.get("body") or "")
        return p.read_text(encoding="utf-8") if p.exists() else ""

    @staticmethod
    def image_paths(t, root):
        return [str((Path(root) / x).resolve()) for x in (t.get("images") or []) if x]

    def click_text(self, pg, text, exact=True, timeout=8, scope=None, log=print):
        ok = pg.click_text(text, exact=exact, scope=scope, timeout=timeout)
        if not ok:
            raise RuntimeError("[%s] 点不到「%s」" % (self.name, text))
        return True

    def wait_result(self, pg, ok_url_bits, ok_text, fail_text, timeout=90, not_url_bits=()):
        end = time.time() + timeout
        while time.time() < end:
            url = pg.url() or ""
            if any(b in url for b in ok_url_bits) and not any(b in url for b in not_url_bits):
                return {"ok": True, "url": url, "signal": "url"}
            txt = pg.body_text(600)
            if any(k in txt for k in ok_text):
                return {"ok": True, "url": url, "signal": "toast"}
            if any(k in txt for k in fail_text):
                return {"ok": False, "url": url, "signal": txt[:150]}
            time.sleep(2)
        return {"ok": False, "url": pg.url(), "signal": "timeout"}
