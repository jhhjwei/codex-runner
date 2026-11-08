#!/usr/bin/env python3
"""一键发布器（零 credits）。

    python3 ops/common/publish/publish.py check   ops/drafts/<日期>/<主题>/manifest.json
    python3 ops/common/publish/publish.py probe   --platform all
    python3 ops/common/publish/publish.py fill    <manifest>          # 只填，不点发布
    python3 ops/common/publish/publish.py publish <manifest>          # 填完真发
    python3 ops/common/publish/publish.py readback --platform xhs --title "…"

为什么这条路不花 credits：
  模型不参与。本机进程用 osascript 对已登录的 Safari 执行 `do JavaScript`，
  脚本读 DOM、填表单、点按钮都是本地进程行为，不进任何会话上下文。
  （WebDriver 这条路在本机走不通：macOS 27 上 POST /session 始终报
   "You must enable 'Allow remote automation'"，别再去试。）

安全闸：
  * BLOCK 级问题一条都不发（标题超长、图片缺失、字数不够都在本地拦下）；
  * fill 模式永远不点发布键，用来验证「填得对不对」；
  * publish 模式必须显式加 --yes（防止手滑），发布后强制回读平台列表。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import contract  # noqa: E402
from core.applescript import Safari, AScriptError  # noqa: E402
from core.page import Page  # noqa: E402
from platforms.baijiahao import Baijiahao  # noqa: E402
from platforms.toutiao import Toutiao  # noqa: E402
from platforms.xhs import Xhs  # noqa: E402

ADAPTERS = {"xhs": Xhs(), "baijiahao": Baijiahao(), "toutiao": Toutiao()}


def log(msg):
    print("%s %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def cmd_check(args):
    path, root, targets = contract.load(args.manifest)
    bad = 0
    for t in targets:
        errs = contract.validate(t, root, check_text_gates=args.gates)
        head = "%s/%s  %s" % (t.get("platform"), t.get("kind"), (t.get("title") or "")[:26])
        blocks = errs.blocked
        print(("FAIL " if blocks else "PASS ") + head)
        if errs:
            print(errs.text())
        bad += len(blocks)
    print("\n结论：%d 条 BLOCK" % bad)
    return 1 if bad else 0


def cmd_probe(args):
    plats = list(ADAPTERS) if args.platform in ("all", None) else [args.platform]
    out = {}
    pg = Page(Safari(log=log), log=log)
    for name in plats:
        a = ADAPTERS[name]
        log("[probe] %s …" % name)
        try:
            info = a.probe(pg, log)
            out[name] = {
                "url": info.get("url"),
                "logged_in": info.get("logged_in"),
                "body_head": info.get("body_head"),
                "inputs": info.get("inputs"),
                "buttons": info.get("buttons"),
            }
            log("[probe] %s 登录=%s url=%s" % (name, info.get("logged_in"), info.get("url")))
        except Exception as e:
            out[name] = {"error": str(e)}
            log("[probe] %s 失败：%s" % (name, e))
    if args.out:
        Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        log("探测结果写到 %s" % args.out)
    return 0


def _load_targets(args):
    path, root, targets = contract.load(args.manifest)
    if args.only:
        targets = [t for t in targets if t.get("platform") == args.only]
    if not targets:
        raise SystemExit("没有匹配的 target")
    return path, root, targets


def _run(args, pg, do_submit):
    path, root, targets = _load_targets(args)
    results = []
    hard_fail = 0
    for t in targets:
        errs = contract.validate(t, root, check_text_gates=args.gates)
        if errs:
            print(errs.text())
        if errs.blocked:
            log("[%s] BLOCK，跳过" % t["platform"])
            results.append({"platform": t["platform"], "status": "blocked", "problems": list(errs)})
            hard_fail += 1
            continue
        a = ADAPTERS[t["platform"]]
        if t["kind"] not in a.kinds:
            log("[%s] 适配器 v1 不支持 %s（支持 %s）" % (t["platform"], t["kind"], a.kinds))
            results.append({"platform": t["platform"], "status": "unsupported"})
            hard_fail += 1
            continue
        rec = {"platform": t["platform"], "kind": t["kind"], "title": t.get("title")}
        try:
            a.open(pg, log)
            rec["url"] = pg.url()
            ev = a.fill(pg, t, root, log)
            rec["fill"] = ev
            ver = a.verify(pg, t, root)
            rec["verify"] = ver
            rec["page_text"] = pg.body_text(300)
            if do_submit:
                res = a.submit(pg, t, log)
                rec["submit"] = res
                time.sleep(3)
                # 微头条没有标题，回读用正文开头
                needle = (t.get("title") or "").strip()
                if not needle:
                    body = a.body_text(t, root).strip().replace("\n", " ")
                    needle = body[:12]
                rb = a.readback(pg, needle, log)
                rec["readback"] = rb
                rec["status"] = "published" if (res.get("ok") and rb.get("found")) else "unconfirmed"
                if rec["status"] == "unconfirmed":
                    hard_fail += 1
            else:
                rec["status"] = "filled"
        except Exception as e:
            rec["status"] = "error"
            rec["error"] = str(e)
            hard_fail += 1
            log("[%s] 失败：%s" % (t["platform"], e))
            try:
                rec["page_text"] = pg.body_text(400)
            except Exception:
                pass
        results.append(rec)
    return results, hard_fail


def cmd_fill(args):
    pg = Page(Safari(log=log), log=log)
    results, bad = _run(args, pg, do_submit=False)
    _report(args, results)
    log("fill 模式：没点发布键。核对完再跑 publish --yes")
    return 1 if bad else 0


def cmd_publish(args):
    if not args.yes:
        raise SystemExit("真发要加 --yes（先跑 fill 看一眼截图）")
    pg = Page(Safari(log=log), log=log)
    results, bad = _run(args, pg, do_submit=True)
    _report(args, results)
    return 1 if bad else 0


def cmd_readback(args):
    a = ADAPTERS[args.platform]
    pg = Page(Safari(log=log), log=log)
    rb = a.readback(pg, args.title, log)
    print(json.dumps(rb, ensure_ascii=False, indent=2))
    return 0 if rb.get("found") else 2


def _report(args, results):
    out = Path(args.outdir) / "result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    for r in results:
        print("%-10s %-12s %s" % (r["platform"], r.get("status"), r.get("title") or ""))
    log("结果写到 %s" % out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="三平台一键发布（零 credits）")
    ap.add_argument("--port", type=int, default=8799)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="只做内容契约校验")
    p.add_argument("manifest")
    p.add_argument("--gates", action="store_true", help="顺带跑目的闸 purpose_check")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("probe", help="探测登录态与页面结构")
    p.add_argument("--platform", default="all")
    p.add_argument("--out", default=None)
    p.add_argument("--outdir", default=os.path.expanduser("~/.qoder-notify/publish-shots"))
    p.add_argument("--shot", action="store_true")
    p.set_defaults(func=cmd_probe)

    for name, fn in (("fill", cmd_fill), ("publish", cmd_publish)):
        p = sub.add_parser(name, help="填表（不点发布）" if name == "fill" else "填完真发")
        p.add_argument("manifest")
        p.add_argument("--only", default=None, help="只发某个平台")
        p.add_argument("--outdir", default=None)
        p.add_argument("--gates", action="store_true")
        p.add_argument("--yes", action="store_true", help="publish 必带")
        p.set_defaults(func=fn)

    p = sub.add_parser("readback", help="回读平台列表确认可见")
    p.add_argument("--platform", required=True, choices=list(ADAPTERS))
    p.add_argument("--title", required=True)
    p.set_defaults(func=cmd_readback)

    args = ap.parse_args(argv)
    if getattr(args, "outdir", None) is None:
        base = Path(args.manifest).resolve().parent if getattr(args, "manifest", None) else Path.cwd()
        args.outdir = str(base / "shots")
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
