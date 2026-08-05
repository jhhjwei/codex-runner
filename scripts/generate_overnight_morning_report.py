#!/usr/bin/env python3
"""Generate a repository-native overnight morning report and notify via GitHub Issues."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "opportunity-pipeline"
HEALTH = PIPELINE / "health"
REPORT_ROOT = PIPELINE / "reports" / "morning"
LATEST_REPORT = REPORT_ROOT / "latest-morning-report.md"
SUMMARY = PIPELINE / "SUMMARY.md"
TZ = ZoneInfo("Asia/Shanghai")
COMMERCIAL_TYPES = {"contact", "claim", "pr", "review_fix", "accepted", "payment", "received"}


def run(*args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def field(text: str, name: str, default: str = "unknown") -> str:
    match = re.search(rf"^-\s*{re.escape(name)}\s*:\s*(.+?)\s*$", text, re.M)
    return match.group(1).strip() if match else default


def api(endpoint: str) -> dict:
    result = run("gh", "api", endpoint)
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "gh api failed"}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "invalid JSON"}


def overnight_hours(now: dt.datetime) -> list[dt.datetime]:
    today = now.date()
    previous = today - dt.timedelta(days=1)
    hours = [dt.datetime.combine(previous, dt.time(hour=h), TZ) for h in (22, 23)]
    hours.extend(dt.datetime.combine(today, dt.time(hour=h), TZ) for h in range(0, 9))
    return hours


def read_hour(hour: dt.datetime) -> dict:
    folder = HEALTH / hour.strftime("%Y-%m-%d")
    primary = folder / f"{hour:%H}.md"
    fallback = folder / f"{hour:%H}-fallback.md"
    if primary.exists():
        path = primary
        heartbeat = "主心跳"
    elif fallback.exists():
        path = fallback
        heartbeat = "仅 fallback"
    else:
        return {
            "hour": hour,
            "heartbeat": "该小时无心跳记录",
            "status": "unknown",
            "actions": 0,
            "types": "none",
            "git": "none",
            "downstream": "无记录",
            "errors": "主心跳与 fallback 均缺失",
            "path": None,
        }

    text = path.read_text(encoding="utf-8")
    actions_raw = field(text, "commercial_actions", field(text, "external_actions", "0"))
    try:
        actions = int(re.search(r"\d+", actions_raw).group(0))
    except (AttributeError, ValueError):
        actions = 0
    action_types = field(text, "commercial_action_types", "none")
    valid_types = [part.strip().lower() for part in action_types.split(",") if part.strip().lower() in COMMERCIAL_TYPES]
    if actions > 0 and not valid_types:
        actions = 0
        action_types = "none (missing valid structured action_type evidence)"

    downstream_lines = []
    for line in text.splitlines():
        if line.startswith("- AsyncAPI") or line.startswith("- Dokploy"):
            downstream_lines.append(line.removeprefix("- "))
    errors = field(text, "trigger_reasons", "none")
    return {
        "hour": hour,
        "heartbeat": heartbeat,
        "status": field(text, "status"),
        "actions": actions,
        "types": action_types,
        "git": field(text, "git_evidence", field(text, "evidence", "none")),
        "downstream": "；".join(downstream_lines) if downstream_lines else "未在小时记录中列明",
        "errors": errors,
        "path": path.relative_to(ROOT).as_posix(),
    }


def changed_files(start: dt.datetime, end: dt.datetime) -> list[str]:
    result = run(
        "git", "log",
        f"--since={start.astimezone(dt.timezone.utc).isoformat()}",
        f"--until={end.astimezone(dt.timezone.utc).isoformat()}",
        "--name-only", "--pretty=format:", "--", "opportunity-pipeline",
    )
    return sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})


def classify_changed(paths: list[str]) -> dict[str, list[str]]:
    groups = {"主机会库": [], "Inbox": [], "当月归档": []}
    for path in paths:
        low = path.lower()
        if "/health/" in low or "/reports/" in low or low.endswith("summary.md"):
            continue
        if "inbox" in low:
            groups["Inbox"].append(path)
        elif "archive" in low or "归档" in path:
            groups["当月归档"].append(path)
        elif any(token in low for token in ("opportun", "pipeline", "lead", "candidate", "verified", "master")):
            groups["主机会库"].append(path)
    return groups


def pipeline_counts() -> str:
    if not SUMMARY.exists():
        return "SUMMARY.md 缺失"
    text = SUMMARY.read_text(encoding="utf-8")
    values = []
    for stage in ("L3", "L4", "L6", "L9", "L10", "L11", "L12"):
        match = re.search(rf"\|\s*{stage}\b[^|]*\|\s*(\d+)\s*\|", text)
        values.append(f"{stage}={match.group(1) if match else 'unknown'}")
    return "、".join(values)


def live_downstream() -> tuple[str, str]:
    asyncapi = api("repos/asyncapi/studio/issues/1333")
    dokploy = api("repos/Dokploy/dokploy/pulls/4918")
    async_text = (
        f"state={asyncapi.get('state', 'unknown')}；"
        f"assignees={[item.get('login') for item in asyncapi.get('assignees', [])]}；"
        f"error={asyncapi.get('error', 'none')}"
    )
    dokploy_text = (
        f"state={dokploy.get('state', 'unknown')}；merged={dokploy.get('merged', False)}；"
        f"mergeable={dokploy.get('mergeable')}；error={dokploy.get('error', 'none')}"
    )
    return async_text, dokploy_text


def find_or_create_issue(title: str, body: str) -> int | None:
    repo = os.environ.get("GITHUB_REPOSITORY", "jhhjwei/codex-runner")
    found = run(
        "gh", "issue", "list", "--repo", repo, "--state", "open",
        "--search", f'\"{title}\" in:title', "--json", "number,title", "--limit", "20",
    )
    if found.returncode == 0:
        try:
            rows = json.loads(found.stdout)
            for row in rows:
                if title in row.get("title", ""):
                    return int(row["number"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass
    created = run(
        "gh", "issue", "create", "--repo", repo, "--title", title,
        "--body", body, "--assignee", "@me",
    )
    if created.returncode != 0:
        return None
    match = re.search(r"/(\d+)\s*$", created.stdout.strip())
    return int(match.group(1)) if match else None


def comment_issue(number: int | None, body: str) -> None:
    if not number:
        return
    repo = os.environ.get("GITHUB_REPOSITORY", "jhhjwei/codex-runner")
    run("gh", "issue", "comment", str(number), "--repo", repo, "--body", body)


def main() -> int:
    now = dt.datetime.now(TZ)
    hours = overnight_hours(now)
    records = [read_hour(hour) for hour in hours]
    start = hours[0]
    end = hours[-1] + dt.timedelta(hours=1)
    changed = changed_files(start, end)
    groups = classify_changed(changed)
    asyncapi, dokploy = live_downstream()

    total_actions = sum(item["actions"] for item in records)
    missing = [item for item in records if item["heartbeat"] == "该小时无心跳记录"]
    fallback_only = [item for item in records if item["heartbeat"] == "仅 fallback"]
    failed = [item for item in records if item["status"] != "completed"]
    punishment = bool(missing or fallback_only or failed or total_actions == 0)

    rows = []
    for item in records:
        evidence = item["git"] if item["git"] != "none" else "无"
        rows.append(
            f"| {item['hour']:%H}:00 | {item['heartbeat']} | {item['status']} | "
            f"{item['actions']}（{item['types']}） | {item['downstream']} | {evidence} | {item['errors']} |"
        )

    changed_sections = []
    for label, paths in groups.items():
        changed_sections.append(f"- **{label}：** " + ("、".join(f"`{p}`" for p in paths[:10]) if paths else "夜间无提交增量"))

    status = "RED / ESCALATED" if punishment else "GREEN"
    unique_action = (
        "处理现有 PR/Review 或提交一个具有公开证据的联系、认领、PR 或申请；禁止候选泛搜索和报告扩写。"
        if punishment
        else "继续推进距离付款最近的现有机会，不扩张低质量候选搜索。"
    )
    report = f"""# 首笔收入转化冲刺夜间晨报

**统计区间：{start:%Y年%m月%d日22:00}—{end:%Y年%m月%d日08:59}（北京时间）**  
**生成时间：{now:%Y-%m-%d %H:%M:%S} +08:00**  
**执行环境：GitHub Actions 仓库内审计，不依赖 ChatGPT Connector 权限**

| 时段 | 心跳 | 状态 | 真实商业动作 | Dokploy / AsyncAPI等状态 | GitHub提交证据 | 错误和阻塞 |
|---|---|---|---:|---|---|---|
{chr(10).join(rows)}

## 主机会库、Inbox和归档核对

{chr(10).join(changed_sections)}

## 夜间汇总

- **累计真实外部动作：{total_actions}**
- **累计 Pipeline：{pipeline_counts()}**
- **AsyncAPI #1333：** {asyncapi}
- **Dokploy PR #4918：** {dokploy}
- **首笔收入状态：** 未发现到账前，不得宣称已付款或到账。
- **处罚状态：** {status}
- **缺失小时：** {', '.join(item['hour'].strftime('%Y-%m-%d %H:00') for item in missing) if missing else '无'}
- **仅 fallback 小时：** {', '.join(item['hour'].strftime('%Y-%m-%d %H:00') for item in fallback_only) if fallback_only else '无'}
- **未完成小时数：** {len(failed)}
- **当天09:00后的唯一主动作：** {unique_action}

## 商业完整性声明

只把联系、认领、PR、Review修复、接受、付款和到账算作商业进展。搜索、归档、报告和候选筛除均计为0。不得虚构回复、合并、付款或到账。
"""

    dated = REPORT_ROOT / f"{now:%Y-%m-%d}.md"
    atomic_write(dated, report)
    atomic_write(LATEST_REPORT, report)

    morning_issue = find_or_create_issue(
        "首笔收入转化冲刺晨报",
        "该 Issue 由 GitHub Actions 每天北京时间09:10更新，用于发送仓库原生晨报通知。",
    )
    comment_issue(morning_issue, report)

    if punishment:
        p0_issue = find_or_create_issue(
            "P0 冲刺偷懒处罚",
            "主链路异常或连续无真实商业动作时，由仓库自动更新。",
        )
        comment_issue(
            p0_issue,
            f"## {now:%Y-%m-%d} 晨报处罚更新\n\n"
            f"- 状态：{status}\n- 缺失小时：{len(missing)}\n- 仅 fallback：{len(fallback_only)}\n"
            f"- 未完成小时：{len(failed)}\n- 夜间真实商业动作：{total_actions}\n"
            f"- 下一主动作：{unique_action}\n\n不得虚构回复、合并、付款或到账。",
        )

    print(dated.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
