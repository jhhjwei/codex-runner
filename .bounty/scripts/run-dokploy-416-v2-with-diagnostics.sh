#!/usr/bin/env bash
set -uo pipefail

LOG_FILE="/tmp/dokploy-416-v2-${GITHUB_RUN_ID}.log"
TARGET_SCRIPT="$GITHUB_WORKSPACE/.bounty/scripts/dokploy-416-v2.sh"

set +e
bash "$TARGET_SCRIPT" 2>&1 | tee "$LOG_FILE"
STATUS=${PIPESTATUS[0]}
set -e

tail -n 250 "$LOG_FILE" > "${LOG_FILE}.tail"
ENCODED=$(base64 -w 0 "${LOG_FILE}.tail")
LOG_PATH=".automation/implementation-${GITHUB_RUN_ID}.log"

gh api \
  --method PUT \
  "repos/jhhjwei/codex-runner/contents/${LOG_PATH}" \
  -f message="ci: record Dokploy implementation diagnostics" \
  -f content="$ENCODED" \
  >/dev/null

exit "$STATUS"
