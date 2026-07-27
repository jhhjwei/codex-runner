#!/usr/bin/env bash
set -euo pipefail

bash "$GITHUB_WORKSPACE/.bounty/scripts/dokploy-416-v2.sh"

python3 <<'PY'
from pathlib import Path

# Add a single helper that returns a shell-safe rclone destination argument.
utils_path = Path("packages/server/src/utils/backups/utils.ts")
utils = utils_path.read_text()
needle = '''export const getRcloneDestination = (
\tdestination: Pick<Destination, "provider" | "bucket" | "endpoint">,
\tpath = "",
) => {'''
if needle not in utils:
    raise SystemExit("getRcloneDestination not found")

end_marker = '''\treturn `${remote}${separator}${remotePath}`;
};
'''
helper = '''\treturn `${remote}${separator}${remotePath}`;
};

export const getRcloneDestinationArgument = (
\tdestination: Pick<Destination, "provider" | "bucket" | "endpoint">,
\tpath = "",
) => quote([getRcloneDestination(destination, path)]);
'''
if "getRcloneDestinationArgument" not in utils:
    if end_marker not in utils:
        raise SystemExit("getRcloneDestination end marker not found")
    utils = utils.replace(end_marker, helper, 1)
utils_path.write_text(utils)

# Database and compose backup modules: use the pre-quoted target and remove
# hand-written double quotes around user-controlled remote strings.
backup_dir = Path("packages/server/src/utils/backups")
for name in ["postgres.ts", "mysql.ts", "mariadb.ts", "mongo.ts", "libsql.ts", "compose.ts"]:
    path = backup_dir / name
    text = path.read_text()
    text = text.replace("getRcloneDestination,", "getRcloneDestinationArgument,")
    text = text.replace("getRcloneDestination(\n", "getRcloneDestinationArgument(\n")
    text = text.replace('"${rcloneDestination}"', '${rcloneDestination}')
    path.write_text(text)

# Web-server backup uses copyto rather than rcat.
web_path = backup_dir / "web-server.ts"
web = web_path.read_text()
web = web.replace("getRcloneDestination,", "getRcloneDestinationArgument,")
web = web.replace("getRcloneDestination(\n", "getRcloneDestinationArgument(\n")
web = web.replace('"${rclonePath}"', '${rclonePath}')
web_path.write_text(web)

# Retention cleanup must quote both the listing root and the delete template.
index_path = backup_dir / "index.ts"
index = index_path.read_text()
if 'import { quote } from "shell-quote";' not in index:
    index = index.replace(
        'import { scheduleJob } from "node-schedule";',
        'import { scheduleJob } from "node-schedule";\nimport { quote } from "shell-quote";',
        1,
    )
index = index.replace(
    'const rcloneList = `rclone lsf ${rcloneFlags.join(" ")} --include "*${backup.databaseType === "web-server" ? ".zip" : ".{sql.gz,bson.gz}"}" ${backupFilesPath}`;',
    'const rcloneList = `rclone lsf ${rcloneFlags.join(" ")} --include "*${backup.databaseType === "web-server" ? ".zip" : ".{sql.gz,bson.gz}"}" ${quote([backupFilesPath])}`;',
    1,
)
index = index.replace(
    'const rcloneDelete = `rclone delete ${rcloneFlags.join(" ")} ${backupFilesPath}/{}`;',
    'const rcloneDelete = `rclone deletefile ${rcloneFlags.join(" ")} ${quote([`${backupFilesPath}/{}`])}`;',
    1,
)
index_path.write_text(index)

# Expand redaction beyond S3 flags to common rclone connection-string and flag
# credentials. This protects structured logs and surfaced error messages.
redact_path = backup_dir / "redact.ts"
redact_path.write_text('''/**
 * Redacts credentials from rclone command strings and connection strings.
 *
 * Covers the existing S3 flags, provider-specific password/token flags, and
 * on-the-fly rclone connection-string parameters such as `pass=` or
 * `client_secret=`.
 */
export const redactRcloneCredentials = (command: string): string => {
\tconst sensitiveName =
\t\t"(?:access[_-]?key(?:[_-]?id)?|secret(?:[_-]?access[_-]?key)?|pass(?:word)?|token|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)";

\treturn command
\t\t.replace(/(--s3-access-key-id=)(?:"[^"]*"|'[^']*'|\\S+)/gi, '$1"[REDACTED]"')
\t\t.replace(/(--s3-secret-access-key=)(?:"[^"]*"|'[^']*'|\\S+)/gi, '$1"[REDACTED]"')
\t\t.replace(
\t\t\tnew RegExp(`(--[a-z0-9-]*${sensitiveName}=)(?:"[^"]*"|'[^']*'|\\\\S+)`, "gi"),
\t\t\t'$1"[REDACTED]"',
\t\t)
\t\t.replace(
\t\t\tnew RegExp(`([,:]${sensitiveName}=)([^,:\\\\s'"/]+)`, "gi"),
\t\t\t"$1[REDACTED]",
\t\t);
};
''')
PY

corepack enable
pnpm install --frozen-lockfile
pnpm --filter @dokploy/server typecheck
pnpm --filter dokploy typecheck
pnpm biome check packages/server/src/db/validations/destination.ts packages/server/src/db/schema/destination.ts packages/server/src/utils/backups apps/dokploy/server/api/routers/destination.ts apps/dokploy/components/dashboard/settings/destination --write

git diff --check
git status --short
