from __future__ import annotations

import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

import scripts.hourly_income_guard as guard


FIXED_START = dt.datetime(2026, 8, 6, 7, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
FIXED_END = FIXED_START + dt.timedelta(hours=1)


def configure(monkeypatch, tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    pipeline = tmp_path / "opportunity-pipeline"
    health = pipeline / "health"
    audit = health / "audit"
    primary = health / "2026-08-06" / "07.md"
    latest = health / "latest-run.md"
    summary = pipeline / "SUMMARY.md"
    primary.parent.mkdir(parents=True)
    primary.write_text("- status: completed\n- external_action_count: 1\n", encoding="utf-8")
    latest.write_text("LATEST MUST SURVIVE\n", encoding="utf-8")
    summary.write_text("# Opportunity Pipeline Summary\n", encoding="utf-8")

    monkeypatch.setattr(guard, "ROOT", tmp_path)
    monkeypatch.setattr(guard, "PIPELINE", pipeline)
    monkeypatch.setattr(guard, "HEALTH", health)
    monkeypatch.setattr(guard, "AUDIT", audit)
    monkeypatch.setattr(guard, "LATEST", latest)
    monkeypatch.setattr(guard, "SUMMARY", summary)
    monkeypatch.setattr(guard, "audited_window", lambda now: (FIXED_START, FIXED_END))
    monkeypatch.setattr(guard, "age_minutes", lambda path, now: 0)
    monkeypatch.setattr(guard, "update_p0_issue", lambda *args: None)
    return primary, latest, summary, audit


def test_guard_never_overwrites_primary_or_latest(monkeypatch, tmp_path):
    primary, latest, summary, audit = configure(monkeypatch, tmp_path)
    original_primary = primary.read_text(encoding="utf-8")
    original_latest = latest.read_text(encoding="utf-8")
    monkeypatch.setattr(guard, "git_evidence", lambda start, end: (["abc\tpipeline commit"], ["claim"]))
    monkeypatch.setattr(guard, "previous_actions", lambda start: 0)

    assert guard.main() == 0
    assert primary.read_text(encoding="utf-8") == original_primary
    assert latest.read_text(encoding="utf-8") == original_latest
    assert (audit / "2026-08-06" / "07.md").exists()
    assert "enforcement_state: GREEN" in (audit / "2026-08-06" / "07.md").read_text(encoding="utf-8")
    assert "audit record:" in summary.read_text(encoding="utf-8")


def test_business_red_is_exit_10_and_still_preserves_primary(monkeypatch, tmp_path):
    primary, latest, _, audit = configure(monkeypatch, tmp_path)
    original_primary = primary.read_text(encoding="utf-8")
    original_latest = latest.read_text(encoding="utf-8")
    monkeypatch.setattr(guard, "git_evidence", lambda start, end: (["abc\tpipeline commit"], []))
    monkeypatch.setattr(guard, "previous_actions", lambda start: 0)

    assert guard.main() == 10
    assert primary.read_text(encoding="utf-8") == original_primary
    assert latest.read_text(encoding="utf-8") == original_latest
    report = (audit / "2026-08-06" / "07.md").read_text(encoding="utf-8")
    assert "enforcement_state: RED" in report
    assert "two consecutive hours without commercial action" in report
