#!/usr/bin/env bash
set -euo pipefail

# Run the original transformation. Its first revision may stop at the final
# formatter because the custom provider item was not inserted into constants.ts.
set +e
bash "$GITHUB_WORKSPACE/.bounty/scripts/dokploy-416.sh"
FIRST_STATUS=$?
set -e

python3 <<'PY'
from pathlib import Path

path = Path("apps/dokploy/components/dashboard/settings/destination/constants.ts")
text = path.read_text()
item = '''\t{
\t\tkey: CUSTOM_RCLONE_PROVIDER,
\t\tname: "Custom rclone remote (Google Drive, OneDrive, FTP, SFTP, etc.)",
\t},
'''
if "key: CUSTOM_RCLONE_PROVIDER" not in text:
    marker = "> = [\n"
    if marker not in text:
        raise SystemExit("S3 provider array marker not found")
    text = text.replace(marker, marker + item, 1)
    path.write_text(text)
PY

# Re-run the complete validation suite. This is authoritative even if the first
# revision stopped at its formatter step.
corepack enable
pnpm install --frozen-lockfile
pnpm --filter @dokploy/server typecheck
pnpm --filter dokploy typecheck
pnpm biome check packages/server/src/db/validations/destination.ts packages/server/src/db/schema/destination.ts packages/server/src/utils/backups apps/dokploy/server/api/routers/destination.ts apps/dokploy/components/dashboard/settings/destination --write

git diff --check
git status --short
