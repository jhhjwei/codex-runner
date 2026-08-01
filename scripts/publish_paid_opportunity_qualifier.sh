#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$ROOT/skills/paid-opportunity-qualifier"
SLUG="paid-opportunity-qualifier"
NAME="Paid Opportunity Qualifier"
OWNER="jhhjwei"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "ERROR: clawhub CLI is not installed." >&2
  echo "Install with: npm i -g clawhub" >&2
  exit 1
fi

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "ERROR: missing $SKILL_DIR/SKILL.md" >&2
  exit 1
fi

if ! clawhub whoami | grep -qx "$OWNER"; then
  echo "ERROR: clawhub is not authenticated as $OWNER." >&2
  echo "Run: clawhub login" >&2
  exit 1
fi

MODE="${1:---dry-run}"
case "$MODE" in
  --dry-run|--publish) ;;
  *)
    echo "Usage: $0 [--dry-run|--publish]" >&2
    exit 2
    ;;
esac

ARGS=(
  skill publish "$SKILL_DIR"
  --slug "$SLUG"
  --name "$NAME"
  --owner "$OWNER"
  --version "1.0.0"
  --changelog "Initial release: evidence-gated paid opportunity qualification and fixed-scope delivery handoff."
  --tags "latest"
  --topics "github,bounty,microgrant,freelance,automation"
  --source-repo "jhhjwei/codex-runner"
  --source-ref "main"
  --source-path "skills/paid-opportunity-qualifier"
)

if [[ "$MODE" == "--dry-run" ]]; then
  ARGS+=(--dry-run --json)
  echo "Running ClawHub dry run..."
else
  echo "Publishing to ClawHub as $OWNER..."
fi

clawhub "${ARGS[@]}"
