"""Safari 的 AppleScript 通道：safaridriver 被 macOS 27 拒了之后的替补。

为什么还能用：
  * Safari 的「允许来自 Apple 事件的 JavaScript」已经是开的（AllowJavaScriptFromAppleEvents=1），
    osascript 能直接 `do JavaScript`，不需要 WebDriver、不需要 admin 密码。
  * 唯一代价：`do JavaScript` 只能同步执行，拿不到 Promise ⇒ 所有等待靠"多问几次"。

这里的字符串处理格外小心：JS 先压成一行，再按 AppleScript 的反斜杠/引号规则转义，
写进临时 .scpt 跑，避免命令行参数被 shell 再吃一层。
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time


class AScriptError(RuntimeError):
    pass


def _as_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _minify(js: str) -> str:
    # AppleScript 字符串不能跨行；换行在 JS 里多数可换成空格，但 // 注释会吃掉后半行
    out = []
    for line in js.splitlines():
        t = line.strip()
        if t.startswith("//"):
            continue
        out.append(t)
    return " ".join(out)


class Safari:
    def __init__(self, log=print):
        self.log = log

    # ---- 底层 ----
    def _osascript(self, lines, timeout=60):
        src = "tell application \"Safari\"\n" + "\n".join(lines) + "\nend tell"
        with tempfile.NamedTemporaryFile("w", suffix=".scpt", delete=False, encoding="utf-8") as f:
            f.write(src)
            path = f.name
        try:
            r = subprocess.run(["/usr/bin/osascript", path], capture_output=True, text=True, timeout=timeout)
        finally:
            os.unlink(path)
        if r.returncode != 0:
            raise AScriptError((r.stderr or r.stdout).strip()[:400])
        return r.stdout.rstrip("\n")

    def js(self, script, *args, timeout=60):
        """在 front window 的当前标签里跑同步 JS，返回值按 JSON 解析（解析不了就当字符串）。

        两个和 WebDriver 不一样的坑：
          * do JavaScript 不包函数体，顶层 `return` 会语法错 ⇒ 统一裹成 IIFE；
          * 没有 arguments ⇒ 传参改成前置 `const __A=[…]` 并把 arguments[i] 换掉。
        """
        body = script
        for i in range(len(args)):
            body = body.replace("arguments[%d]" % i, "__A[%d]" % i)
        pre = "const __A=%s;" % json.dumps(list(args), ensure_ascii=False) if args else ""
        one = "(function(){%s %s})()" % (pre, _minify(body))
        out = self._osascript(["do JavaScript %s in current tab of front window" % _as_quote(one)], timeout)
        if out == "missing value":
            return None
        try:
            return json.loads(out)
        except Exception:
            return out

    def ensure_window(self):
        try:
            if self._osascript(["count of windows"], timeout=20).strip() in ("", "0"):
                self._osascript(["make new document"])
        except AScriptError:
            pass

    def open(self, url, reuse=True):
        self.ensure_window()
        self._osascript(["set URL of current tab of front window to %s" % _as_quote(url)])

    def tabs(self):
        return self._osascript(["get URL of every tab of front window"], timeout=30)

    def url(self):
        return self._osascript(["get URL of current tab of front window"], timeout=30)

    def title(self):
        return self._osascript(["get name of current tab of front window"], timeout=30)

    # ---- 常用等待 ----
    def wait_ready(self, timeout=40, extra=None):
        end = time.time() + timeout
        while time.time() < end:
            try:
                st = self.js("return document.readyState", timeout=15)
                if st == "complete" and (extra is None or self.js(extra, timeout=15)):
                    return True
            except AScriptError:
                pass
            time.sleep(0.8)
        return False

    def wait_js(self, cond, timeout=30, poll=0.7):
        end = time.time() + timeout
        last = None
        while time.time() < end:
            try:
                if self.js("return (%s)" % cond, timeout=20):
                    return True
            except AScriptError as e:
                last = e
            time.sleep(poll)
        if last:
            self.log("[as] 等待超时：%s（%s）" % (cond, last))
        return False
