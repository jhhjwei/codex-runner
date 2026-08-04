#!/usr/bin/env python3
"""Primary hourly heartbeat and anti-idling guard for the income pipeline."""
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
LATEST = HEALTH / "latest-run.md"
SUMMARY = PIPELINE / "SUMMARY.md"
TZ = ZoneInfo("Asia/Shanghai")
ACTION_RE = re.compile(
    r"(?:^|\s)action_type\s*:\s*(contact|claim|pr|review_fix|accepted|payment|received)\b",
    re.I,
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
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


def api(endpoint: str) -> dict:
    result = run("gh", "api", endpoint, check=False)
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "gh api failed"}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "invalid GitHub API response"}


def audited_window(now: dt.datetime) -> tuple[dt.datetime, dt.datetime]:
    end = now.replace(minute=0, second=0, microsecond=0)
    return end - dt.timedelta(hours=1), end


def git_evidence(start: dt.datetime, end: dt.datetime) -> tuple[list[str], list[str]]:
    since = start.astimezone(dt.timezone.utc).isoformat()
    until = end.astimezone(dt.timezone.utc).isoformat()
    log = run(
        "git", "log", f"--since={since}", f"--until={until}",
        "--pretty=format:%H%x09%s", "--", "opportunity-pipeline", check=False,
    )
    commits = [line for line in log.stdout.splitlines() if line.strip()]
    patch = run(
        "git", "log", f"--since={since}", f"--until={until}", "-p", "--",
        "opportunity-pipeline", check=False,
    ).stdout
    actions = sorted({match.group(1).lower() for match in ACTION_RE.finditer(patch)})
    return commits, actions


def age_minutes(path: Path, now: dt.datetime) -> int | None:
    if not path.exists():
        return None
    modified = dt.datetime.fromtimestamp(path.stat().st_mtime, TZ)
    return int((now - modified).total_seconds() // 60)


def previous_actions(start: dt.datetime) -> int:
    previous = start - dt.timedelta(hours=1)
    path = HEALTH / previous.strftime("%Y-%m-%d") / f"{previous:%H}.md"
    if not path.exists():
        return 0
    match = re.search(
        r"^- commercial_actions:\s*(\d+)\s*$",
        path.read_text(encoding="utf-8"),
        re.M,
    )
    return int(match.group(1)) if match else 0


def downstream() -> dict:
    asyncapi = api("repos/asyncapi/studio/issues/1333")
    dokploy = api("repos/Dokploy/dokploy/pulls/4918")
    return {
        "asyncapi_state": asyncapi.get("state", "unknown"),
        "asyncapi_assignees": [item.get("login") for item in asyncapi.get("assignees", [])],
        "asyncapi_error": asyncapi.get("error"),
        "dokploy_state": dokploy.get("state", "unknown"),
        "dokploy_merged": dokploy.get("merged", False),
        "dokploy_mergeable": dokploy.get("mergeable"),
        "dokploy_error": dokploy.get("error"),
    }


def update_p0_issue(start: dt.datetime, end: dt.datetime, actions: list[str], reasons: list[str]) -> None:
    if not reasons:
        return
    repo = os.environ.get("GITHUB_REPOSITORY", "jhhjwei/codex-runner")
    title = "P0 冲刺偷懒处罚"
    body = f"""## RED enforcement update

- audited Beijing hour: {start:%Y-%m-%d %H}:00–{(end - dt.timedelta(seconds=1)):%H}:59
- trigger reasons: {', '.join(reasons)}
- verified commercial actions: {len(actions)} ({', '.join(actions) if actions else 'none'})
- responsibility state: primary executor failed closed

## Next-hour only action

Repair the primary chain and complete at least one verifiable contact, claim, PR, review fix, acceptance, payment or receipt action. Search, archive and report generation do not count.

## Acceptance criteria

1. Two consecutive primary heartbeats exist; fallback-only records do not qualify.
2. `health/latest-run.md` and `SUMMARY.md` stay within 90 minutes.
3. At least one structured `action_type:` marker has public evidence.
4. No reply, merge, payment or receipt is fabricated.
"""
    found = run(
        "gh", "issue", "list", "--repo", repo, "--state", "open",
        "--search", f'\"{title}\" in:title', "--json", "number", "--limit", "1",
        check=False,
    )
    number = None
    if found.returncode == 0:
        try:
            rows = json.loads(found.stdout)
            number = rows[0]["number"] if rows else None
        except (json.JSONDecodeError, KeyError, IndexError):
            number = None
    if number:
        run("gh", "issue", "comment", str(number), "--repo", repo, "--body", body)
    else:
        run("gh", "issue", "create", "--repo", repo, "--title", title, "--body", body)


def main() -> int:
    now = dt.datetime.now(TZ)
    start, end = audited_window(now)
    commits, actions = git_evidence(start, end)
    latest_age = age_minutes(LATEST, now)
    summary_age = age_minutes(SUMMARY, now)
    reasons: list[str] = []
    if not commits:
        reasons.append("primary hourly pipeline commit missing")
    if not actions and previous_actions(start) == 0:
        reasons.append("two consecutive hours without commercial action")
    if latest_age is None or latest_age > 90:
        reasons.append("latest-run stale >90m")
    if summary_age is None or summary_age > 90:
        reasons.append("SUMMARY stale >90m")

    state = downstream()
    status = "failed" if reasons else "completed"
    target = HEALTH / start.strftime("%Y-%m-%d") / f"{start:%H}.md"
    heartbeat = f"""# Hourly income conversion heartbeat

- Beijing hour: {start:%Y-%m-%d %H}:00–{(end - dt.timedelta(seconds=1)):%H}:59 +08:00
- status: {status}
- task: first-income hourly executor
- primary_heartbeat: true
- fallback: false
- commercial_actions: {len(actions)}
- commercial_action_types: {', '.join(actions) if actions else 'none'}
- git_evidence: {'; '.join(commits) if commits else 'none'}
- punishment_triggered: {str(bool(reasons)).lower()}
- trigger_reasons: {', '.join(reasons) if reasons else 'none'}

## Downstream

- AsyncAPI Studio #1333: state={state['asyncapi_state']}; assignees={state['asyncapi_assignees']}; error={state['asyncapi_error'] or 'none'}
- Dokploy PR #4918: state={state['dokploy_state']}; merged={state['dokploy_merged']}; mergeable={state['dokploy_mergeable']}; error={state['dokploy_error'] or 'none'}

## Commercial integrity

Only contact, claim, PR, review_fix, accepted, payment and received count. Search, archive and reports count as zero. No reply, merge, payment or receipt is inferred.
"""
    atomic_write(target, heartbeat)
    atomic_write(LATEST, heartbeat)

    old_summary = SUMMARY.read_text(encoding="utf-8") if SUMMARY.exists() else "# Opportunity Pipeline Summary\n"
    old_summary = re.sub(r"\n## Hourly guard status\n.*\Z", "", old_summary, flags=re.S)
    guard = f"""

## Hourly guard status

_Last updated: {now:%Y-%m-%d %H:%M:%S} +08:00_

- latest primary heartbeat: `{target.relative_to(ROOT)}`
- commercial actions in audited hour: {len(actions)} ({', '.join(actions) if actions else 'none'})
- enforcement state: {'RED' if reasons else 'GREEN'}
- trigger reasons: {', '.join(reasons) if reasons else 'none'}
- counting rule: search, archive and reports are not commercial progress
"""
    atomic_write(SUMMARY, old_summary.rstrip() + guard + "\n")
    update_p0_issue(start, end, actions, reasons)
    print(target.relative_to(ROOT))
    return 10 if reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
