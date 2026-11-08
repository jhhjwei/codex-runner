"""内容契约：manifest 长什么样、每个平台收什么规格、不合格怎么报。

一条内容 = 一个目录，目录里放 manifest.json + 正文 + 图片/封面/视频：

    ops/drafts/<日期>/<主题>/
      manifest.json
      body-xhs.txt  body-bjh.txt  body-tt.txt
      img/01.png img/02.png ...
      cover.png
      video.mp4

manifest.json:
    {
      "schema": "publish/1",
      "targets": [
        {"platform": "xhs", "kind": "note",
         "title": "≤20 字", "body": "body-xhs.txt",
         "images": ["img/01.png", ...], "topics": ["AI"],
         "schedule": null}
      ]
    }

设计取舍：
  * 一个 manifest 可以写多条 target ⇒ 一次命令发三个平台。
  * 正文一律用文件（不写进 json），避免引号/换行在 json 里打架。
  * schedule 留空=立即发；写 "YYYY-MM-DD HH:MM" 只是记录，脚本不做守候
    （守候是定时任务的事，长会话干等正是 AGENTS.md 里点名要避免的）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# ---- 平台规格（唯一事实源；改这里，不放别处）----
LIMITS = {
    "xhs": {
        "note": {
            "title": (1, 20),
            "body": (1, 1000),
            "images": (1, 18),
            "image_formats": {".jpg", ".jpeg", ".png", ".webp"},
            "image_max_mb": 32,
            "image_min_side": 300,
            "video": False,
            "cover": False,
            "topics_max": 10,
        },
    },
    "baijiahao": {
        "article": {
            "title": (5, 40),
            "body": (200, 20000),
            "images": (1, 20),
            "image_formats": {".jpg", ".jpeg", ".png", ".gif"},
            "image_max_mb": 5,
            "image_min_side": 300,
            "video": False,
            "cover": True,          # 图文必须有封面；没给 cover 就用 images[0]
            "topics_max": 0,
        },
    },
    "toutiao": {
        "weitoutiao": {
            "title": (0, 0),        # 微头条没有标题栏，title 只用作台账/回读
            "body": (10, 2000),
            "images": (0, 9),
            "image_formats": {".jpg", ".jpeg", ".png"},
            "image_max_mb": 10,
            "image_min_side": 200,
            "video": False,
            "cover": False,
            "topics_max": 5,
        },
        "article": {
            "title": (5, 30),
            "body": (300, 30000),
            "images": (0, 20),
            "image_formats": {".jpg", ".jpeg", ".png"},
            "image_max_mb": 10,
            "image_min_side": 300,
            "video": False,
            "cover": True,
            "topics_max": 5,
        },
    },
}

IMAGE_MIN_BYTES = 1024          # 小于 1KB 基本是占位/空文件
VIDEO_FORMATS = {".mp4", ".mov"}


class ContractError(list):
    """收集所有问题再一次性报，不要一条一条挤牙膏。"""

    def add(self, level, where, msg):
        self.append({"level": level, "where": where, "msg": msg})

    @property
    def blocked(self):
        return [x for x in self if x["level"] == "BLOCK"]

    def text(self):
        return "\n".join("  [%s] %-28s %s" % (x["level"], x["where"], x["msg"]) for x in self)


def _img_size(path):
    """不装 Pillow，自己读 PNG/JPEG 头。"""
    try:
        with open(path, "rb") as f:
            head = f.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                w = int.from_bytes(head[16:20], "big")
                h = int.from_bytes(head[20:24], "big")
                return w, h
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    b = f.read(1)
                    if not b:
                        return None
                    if b != b"\xff":
                        continue
                    m = f.read(1)
                    while m == b"\xff":
                        m = f.read(1)
                    if m in (b"\xc0", b"\xc1", b"\xc2"):
                        f.read(3)
                        h = int.from_bytes(f.read(2), "big")
                        w = int.from_bytes(f.read(2), "big")
                        return w, h
                    seg = f.read(2)
                    if len(seg) < 2:
                        return None
                    f.seek(int.from_bytes(seg, "big") - 2, 1)
    except OSError:
        return None
    return None


def load(manifest_path):
    p = Path(manifest_path).resolve()
    if not p.exists():
        raise SystemExit("manifest 不存在：%s" % p)
    with open(p, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != "publish/1":
        raise SystemExit("schema 必须是 publish/1，当前 %r" % doc.get("schema"))
    targets = doc.get("targets") or []
    if not targets:
        raise SystemExit("targets 是空的")
    return p, p.parent, targets


def validate(target, root, check_text_gates=False):
    """返回 problems（list），空表示可以发。"""
    errs = ContractError()
    plat = target.get("platform")
    kind = target.get("kind")
    root = Path(root)
    where = "%s/%s" % (plat, kind)

    if plat not in LIMITS:
        errs.add("BLOCK", where, "不支持的平台，只有 %s" % list(LIMITS))
        return errs
    if kind not in LIMITS[plat]:
        errs.add("BLOCK", where, "不支持的体裁，%s 只有 %s" % (plat, list(LIMITS[plat])))
        return errs
    spec = LIMITS[plat][kind]

    title = (target.get("title") or "").strip()
    lo, hi = spec["title"]
    if hi and not (lo <= len(title) <= hi):
        errs.add("BLOCK", where + ".title", "%d 字，要求 %d–%d" % (len(title), lo, hi))

    body_path = root / (target.get("body") or "")
    body = ""
    if not target.get("body"):
        errs.add("BLOCK", where + ".body", "没指定正文文件")
    elif not body_path.exists():
        errs.add("BLOCK", where + ".body", "文件不存在：%s" % body_path)
    else:
        body = body_path.read_text(encoding="utf-8")
        lo_b, hi_b = spec["body"]
        n = len(body.strip())
        if not (lo_b <= n <= hi_b):
            errs.add("BLOCK", where + ".body", "%d 字，要求 %d–%d" % (n, lo_b, hi_b))
        if "\r" in body:
            errs.add("WARN", where + ".body", "正文含 \\r，粘贴易出双回车")
        if "![" in body or "##" in body:
            errs.add("WARN", where + ".body", "含 markdown 语法，纯文本平台会原样显示")

    imgs = target.get("images") or []
    imgs = [x for x in imgs if x]
    lo_i, hi_i = spec["images"]
    if not (lo_i <= len(imgs) <= hi_i):
        errs.add("BLOCK", where + ".images", "%d 张，要求 %d–%d" % (len(imgs), lo_i, hi_i))
    for rel in imgs:
        f = root / rel
        if not f.exists():
            errs.add("BLOCK", where + ".images", "不存在：%s" % rel)
            continue
        ext = f.suffix.lower()
        if ext not in spec["image_formats"]:
            errs.add("BLOCK", where + ".images", "%s 格式 %s 不收（收 %s）" % (rel, ext, sorted(spec["image_formats"])))
        mb = f.stat().st_size / 1048576
        if mb > spec["image_max_mb"]:
            errs.add("BLOCK", where + ".images", "%s 有 %.1fMB，上限 %dMB" % (rel, mb, spec["image_max_mb"]))
        if f.stat().st_size < IMAGE_MIN_BYTES:
            errs.add("BLOCK", where + ".images", "%s 只有 %d 字节，像空文件" % (rel, f.stat().st_size))
        size = _img_size(str(f))
        if size is None:
            errs.add("WARN", where + ".images", "%s 读不出宽高（可能不是真图片）" % rel)
        elif min(size) < spec["image_min_side"]:
            errs.add("WARN", where + ".images", "%s 只有 %dx%d，边长建议 ≥%d" % (rel, size[0], size[1], spec["image_min_side"]))

    if spec.get("cover") and not target.get("cover") and not imgs:
        errs.add("BLOCK", where + ".cover", "这个体裁要封面")

    vid = target.get("video")
    if vid:
        f = root / vid
        if not f.exists():
            errs.add("BLOCK", where + ".video", "不存在：%s" % vid)
        elif f.suffix.lower() not in VIDEO_FORMATS:
            errs.add("BLOCK", where + ".video", "只收 mp4/mov")
    elif spec.get("video"):
        errs.add("BLOCK", where + ".video", "这个体裁要视频")

    topics = target.get("topics") or []
    if len(topics) > (spec.get("topics_max") or 0):
        errs.add("WARN", where + ".topics", "%d 个话题，超出平台舒适区 %d" % (len(topics), spec.get("topics_max")))

    sched = target.get("schedule")
    if sched:
        errs.add("INFO", where + ".schedule", "记录为 %s；脚本不会守着等到点" % sched)

    if check_text_gates and body:
        import subprocess
        here = Path(__file__).resolve().parents[3]  # ops/common/publish/core -> repo root
        gate = here / "ops" / "common" / "purpose_check.py"
        if gate.exists():
            body_tmp = root / ("%s.%s.gate.txt" % (body_path.stem, plat))
            body_tmp.write_text(body, encoding="utf-8")
            r = subprocess.run(["/usr/bin/python3", str(gate), str(body_tmp)], capture_output=True, text=True)
            body_tmp.unlink(missing_ok=True)
            if r.returncode not in (0,):
                errs.add("BLOCK", where + ".gate", "目的闸未过 rc=%s %s" % (r.returncode, (r.stdout or "").strip().splitlines()[-1:] or ""))
    return errs
