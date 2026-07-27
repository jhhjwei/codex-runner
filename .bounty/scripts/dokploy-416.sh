#!/usr/bin/env bash
set -euo pipefail

python3 <<'PY'
from pathlib import Path
import re


def replace_once(path: str, old: str, new: str) -> None:
    file = Path(path)
    text = file.read_text()
    if old not in text:
        raise SystemExit(f"Expected block not found in {path}")
    file.write_text(text.replace(old, new, 1))

# Shared validation constant.
replace_once(
    "packages/server/src/db/validations/destination.ts",
    'export const ADDITIONAL_FLAG_REGEX = /^--[a-zA-Z0-9-]+(=[a-zA-Z0-9._:/@-]+)?$/;',
    'export const CUSTOM_RCLONE_PROVIDER = "RcloneCustom";\n\nexport const ADDITIONAL_FLAG_REGEX = /^--[a-zA-Z0-9-]+(=[a-zA-Z0-9._:/@-]+)?$/;',
)

# Centralize S3/custom rclone target generation and avoid running a database dump twice.
utils_path = Path("packages/server/src/utils/backups/utils.ts")
utils = utils_path.read_text()
utils = utils.replace(
    'import type { BackupSchedule } from "@dokploy/server/services/backup";',
    'import { CUSTOM_RCLONE_PROVIDER } from "@dokploy/server/db/validations/destination";\nimport type { BackupSchedule } from "@dokploy/server/services/backup";',
    1,
)
old_credentials = '''export const getS3Credentials = (destination: Destination) => {
\tconst { accessKey, secretAccessKey, region, endpoint, provider } =
\t\tdestination;
\tconst rcloneFlags = [
\t\t`--s3-access-key-id=${quote([accessKey])}`,
\t\t`--s3-secret-access-key=${quote([secretAccessKey])}`,
\t\t`--s3-region=${quote([region])}`,
\t\t`--s3-endpoint=${quote([endpoint])}`,
\t\t"--s3-no-check-bucket",
\t\t"--s3-force-path-style",
\t];

\tif (provider) {
\t\trcloneFlags.unshift(`--s3-provider=${quote([provider])}`);
\t}

\tif (destination.additionalFlags?.length) {
\t\trcloneFlags.push(...destination.additionalFlags);
\t}

\treturn rcloneFlags;
};'''
new_credentials = '''export const isCustomRcloneDestination = (
\tdestination: Pick<Destination, "provider">,
) => destination.provider === CUSTOM_RCLONE_PROVIDER;

export const getRcloneCredentials = (
\tdestination: Pick<
\t\tDestination,
\t\t| "provider"
\t\t| "accessKey"
\t\t| "secretAccessKey"
\t\t| "region"
\t\t| "endpoint"
\t\t| "additionalFlags"
\t>,
) => {
\tif (isCustomRcloneDestination(destination)) {
\t\treturn destination.additionalFlags ?? [];
\t}

\tconst { accessKey, secretAccessKey, region, endpoint, provider } =
\t\tdestination;
\tconst rcloneFlags = [
\t\t`--s3-access-key-id=${quote([accessKey])}`,
\t\t`--s3-secret-access-key=${quote([secretAccessKey])}`,
\t\t`--s3-region=${quote([region])}`,
\t\t`--s3-endpoint=${quote([endpoint])}`,
\t\t"--s3-no-check-bucket",
\t\t"--s3-force-path-style",
\t];

\tif (provider) {
\t\trcloneFlags.unshift(`--s3-provider=${quote([provider])}`);
\t}

\tif (destination.additionalFlags?.length) {
\t\trcloneFlags.push(...destination.additionalFlags);
\t}

\treturn rcloneFlags;
};

// Backward-compatible alias for downstream imports while the UI and backup
// code migrate to the provider-neutral name.
export const getS3Credentials = getRcloneCredentials;

export const getRcloneDestination = (
\tdestination: Pick<Destination, "provider" | "bucket" | "endpoint">,
\tpath = "",
) => {
\tconst clean = (value: string) => value.trim().replace(/^\\/+|\\/+$/g, "");
\tconst cleanPath = clean(path);

\tif (!isCustomRcloneDestination(destination)) {
\t\treturn `:s3:${[clean(destination.bucket), cleanPath]
\t\t\t.filter(Boolean)
\t\t\t.join("/")}`;
\t}

\tconst remote = destination.endpoint.trim();
\tif (!remote || !remote.includes(":")) {
\t\tthrow new Error(
\t\t\t"Custom rclone destinations require a named remote or connection string (for example, gdrive: or :sftp,host=example.com:)",
\t\t);
\t}

\tconst remotePath = [clean(destination.bucket), cleanPath]
\t\t.filter(Boolean)
\t\t.join("/");
\tif (!remotePath) return remote;

\tconst separator = remote.endsWith(":") || remote.endsWith("/") ? "" : "/";
\treturn `${remote}${separator}${remotePath}`;
};'''
if old_credentials not in utils:
    raise SystemExit("getS3Credentials block not found")
utils = utils.replace(old_credentials, new_credentials, 1)
old_execution = '''\t# Run the backup command and capture the exit status
\tBACKUP_OUTPUT=$(${backupCommand} 2>&1 >/dev/null) || {
\t\techo "[$(date)] ❌ Error: Backup failed" >> ${logPath};
\t\techo "Error: $BACKUP_OUTPUT" >> ${logPath};
\t\texit 1;
\t}

\techo "[$(date)] ✅ backup completed successfully" >> ${logPath};
\techo "[$(date)] Starting upload to S3..." >> ${logPath};

\t# Run the upload command and capture the exit status
\tUPLOAD_OUTPUT=$(${backupCommand} | ${rcloneCommand} 2>&1 >/dev/null) || {
\t\techo "[$(date)] ❌ Error: Upload to S3 failed" >> ${logPath};
\t\techo "Error: $UPLOAD_OUTPUT" >> ${logPath};
\t\texit 1;
\t}

\techo "[$(date)] ✅ Upload to S3 completed successfully" >> ${logPath};'''
new_execution = '''\techo "[$(date)] Starting backup upload..." >> ${logPath};

\t# Stream the backup once directly into rclone. The previous implementation
\t# executed the database dump twice: once as a check and once for upload.
\tUPLOAD_OUTPUT=$(${backupCommand} | ${rcloneCommand} 2>&1 >/dev/null) || {
\t\techo "[$(date)] ❌ Error: Backup upload failed" >> ${logPath};
\t\techo "Error: $UPLOAD_OUTPUT" >> ${logPath};
\t\texit 1;
\t}

\techo "[$(date)] ✅ Backup upload completed successfully" >> ${logPath};'''
if old_execution not in utils:
    raise SystemExit("backup execution block not found")
utils = utils.replace(old_execution, new_execution, 1)
utils_path.write_text(utils)

# API validation supports either the existing S3 fields or a custom rclone remote.
schema_path = Path("packages/server/src/db/schema/destination.ts")
schema = schema_path.read_text()
schema = schema.replace(
    'import {\n\tADDITIONAL_FLAG_ERROR,\n\tADDITIONAL_FLAG_REGEX,\n} from "../validations/destination";',
    'import {\n\tADDITIONAL_FLAG_ERROR,\n\tADDITIONAL_FLAG_REGEX,\n\tCUSTOM_RCLONE_PROVIDER,\n} from "../validations/destination";',
    1,
)
validation_block = '''
const validateDestination = (
\tdata: {
\t\tprovider?: string | null;
\t\taccessKey?: string;
\t\tsecretAccessKey?: string;
\t\tbucket?: string;
\t\tendpoint?: string;
\t},
\tctx: z.RefinementCtx,
) => {
\tif (data.provider === CUSTOM_RCLONE_PROVIDER) {
\t\tif (!data.endpoint?.trim() || !data.endpoint.includes(":")) {
\t\t\tctx.addIssue({
\t\t\t\tcode: "custom",
\t\t\t\tpath: ["endpoint"],
\t\t\t\tmessage:
\t\t\t\t\t"Enter a named rclone remote or connection string, such as gdrive: or :sftp,host=example.com:",
\t\t\t});
\t\t}
\t\treturn;
\t}

\tfor (const [field, label] of [
\t\t["accessKey", "Access key"],
\t\t["secretAccessKey", "Secret access key"],
\t\t["bucket", "Bucket"],
\t\t["endpoint", "Endpoint"],
\t] as const) {
\t\tif (!data[field]?.trim()) {
\t\t\tctx.addIssue({
\t\t\t\tcode: "custom",
\t\t\t\tpath: [field],
\t\t\t\tmessage: `${label} is required for S3 destinations`,
\t\t\t});
\t\t}
\t}
};
'''
marker = 'export const apiCreateDestination = createSchema'
if marker not in schema:
    raise SystemExit("destination schema marker not found")
schema = schema.replace(marker, validation_block + '\n' + marker, 1)
schema = schema.replace(
    '\t.extend({\n\t\tserverId: z.string().optional(),\n\t});\n\nexport const apiFindOneDestination',
    '\t.extend({\n\t\tserverId: z.string().optional(),\n\t})\n\t.superRefine(validateDestination);\n\nexport const apiFindOneDestination',
    1,
)
schema = schema.replace(
    '\t.extend({\n\t\tserverId: z.string().optional(),\n\t});',
    '\t.extend({\n\t\tserverId: z.string().optional(),\n\t})\n\t.superRefine(validateDestination);',
    1,
)
schema_path.write_text(schema)

# Connection testing uses the same provider-neutral helpers as real backups.
router_path = Path("apps/dokploy/server/api/routers/destination.ts")
router = router_path.read_text()
router = router.replace(
    '\tfindDestinationById,\n\tIS_CLOUD,',
    '\tfindDestinationById,\n\tgetRcloneCredentials,\n\tgetRcloneDestination,\n\tIS_CLOUD,',
    1,
)
old_router = '''\t\t.mutation(async ({ input }) => {
\t\t\tconst {
\t\t\t\tsecretAccessKey,
\t\t\t\tbucket,
\t\t\t\tregion,
\t\t\t\tendpoint,
\t\t\t\taccessKey,
\t\t\t\tprovider,
\t\t\t\tadditionalFlags,
\t\t\t} = input;
\t\t\ttry {
\t\t\t\tconst rcloneFlags = [
\t\t\t\t\t`--s3-access-key-id=${quote([accessKey])}`,
\t\t\t\t\t`--s3-secret-access-key=${quote([secretAccessKey])}`,
\t\t\t\t\t`--s3-region=${quote([region])}`,
\t\t\t\t\t`--s3-endpoint=${quote([endpoint])}`,
\t\t\t\t\t"--s3-no-check-bucket",
\t\t\t\t\t"--s3-force-path-style",
\t\t\t\t\t"--retries 1",
\t\t\t\t\t"--low-level-retries 1",
\t\t\t\t\t"--timeout 10s",
\t\t\t\t\t"--contimeout 5s",
\t\t\t\t];
\t\t\t\tif (provider) {
\t\t\t\t\trcloneFlags.unshift(`--s3-provider=${quote([provider])}`);
\t\t\t\t}
\t\t\t\tif (additionalFlags?.length) {
\t\t\t\t\trcloneFlags.push(...additionalFlags);
\t\t\t\t}
\t\t\t\tconst rcloneDestination = `:s3:${bucket}`;
\t\t\t\tconst rcloneCommand = `rclone ls ${rcloneFlags.join(" ")} ${quote([rcloneDestination])}`;'''
new_router = '''\t\t.mutation(async ({ input }) => {
\t\t\ttry {
\t\t\t\tconst rcloneFlags = [
\t\t\t\t\t...getRcloneCredentials(input),
\t\t\t\t\t"--retries 1",
\t\t\t\t\t"--low-level-retries 1",
\t\t\t\t\t"--timeout 10s",
\t\t\t\t\t"--contimeout 5s",
\t\t\t\t];
\t\t\t\tconst rcloneDestination = getRcloneDestination(input);
\t\t\t\tconst rcloneCommand = `rclone lsd ${rcloneFlags.join(" ")} ${quote([rcloneDestination])}`;'''
if old_router not in router:
    raise SystemExit("destination router connection block not found")
router_path.write_text(router.replace(old_router, new_router, 1))

# Add a custom-rclone option to the provider selector.
constants_path = Path("apps/dokploy/components/dashboard/settings/destination/constants.ts")
constants = constants_path.read_text()
constants = 'import { CUSTOM_RCLONE_PROVIDER } from "@dokploy/server/db/validations/destination";\n\n' + constants
constants = constants.replace(
    '] = [\n',
    '] = [\n\t{\n\t\tkey: CUSTOM_RCLONE_PROVIDER,\n\t\tname: "Custom rclone remote (Google Drive, OneDrive, FTP, SFTP, etc.)",\n\t},\n',
    1,
)
constants_path.write_text(constants)

# Make the existing destination form conditionally validate and explain custom mode.
ui_path = Path("apps/dokploy/components/dashboard/settings/destination/handle-destinations.tsx")
ui = ui_path.read_text()
ui = ui.replace(
    '\tADDITIONAL_FLAG_REGEX,\n} from "@dokploy/server/db/validations/destination";',
    '\tADDITIONAL_FLAG_REGEX,\n\tCUSTOM_RCLONE_PROVIDER,\n} from "@dokploy/server/db/validations/destination";',
    1,
)
old_ui_schema = '''const addDestination = z.object({
\tname: z.string().min(1, "Name is required"),
\tprovider: z.string().min(1, "Provider is required"),
\taccessKeyId: z.string().min(1, "Access Key Id is required"),
\tsecretAccessKey: z.string().min(1, "Secret Access Key is required"),
\tbucket: z.string().min(1, "Bucket is required"),
\tregion: z.string(),
\tendpoint: z.string().min(1, "Endpoint is required"),
\tserverId: z.string().optional(),
\tadditionalFlags: z
\t\t.array(
\t\t\tz.object({
\t\t\t\tvalue: z
\t\t\t\t\t.string()
\t\t\t\t\t.min(1, "Flag cannot be empty")
\t\t\t\t\t.regex(ADDITIONAL_FLAG_REGEX, ADDITIONAL_FLAG_ERROR),
\t\t\t}),
\t\t)
\t\t.optional(),
});'''
new_ui_schema = '''const addDestination = z
\t.object({
\t\tname: z.string().min(1, "Name is required"),
\t\tprovider: z.string().min(1, "Provider is required"),
\t\taccessKeyId: z.string(),
\t\tsecretAccessKey: z.string(),
\t\tbucket: z.string(),
\t\tregion: z.string(),
\t\tendpoint: z.string(),
\t\tserverId: z.string().optional(),
\t\tadditionalFlags: z
\t\t\t.array(
\t\t\t\tz.object({
\t\t\t\t\tvalue: z
\t\t\t\t\t\t.string()
\t\t\t\t\t\t.min(1, "Flag cannot be empty")
\t\t\t\t\t\t.regex(ADDITIONAL_FLAG_REGEX, ADDITIONAL_FLAG_ERROR),
\t\t\t\t}),
\t\t\t)
\t\t\t.optional(),
\t})
\t.superRefine((data, ctx) => {
\t\tif (data.provider === CUSTOM_RCLONE_PROVIDER) {
\t\t\tif (!data.endpoint.trim() || !data.endpoint.includes(":")) {
\t\t\t\tctx.addIssue({
\t\t\t\t\tcode: "custom",
\t\t\t\t\tpath: ["endpoint"],
\t\t\t\t\tmessage:
\t\t\t\t\t\t"Enter a named remote or connection string, such as gdrive: or :sftp,host=example.com:",
\t\t\t\t});
\t\t\t}
\t\t\treturn;
\t\t}

\t\tfor (const [field, label] of [
\t\t\t["accessKeyId", "Access Key Id"],
\t\t\t["secretAccessKey", "Secret Access Key"],
\t\t\t["bucket", "Bucket"],
\t\t\t["endpoint", "Endpoint"],
\t\t] as const) {
\t\t\tif (!data[field].trim()) {
\t\t\t\tctx.addIssue({
\t\t\t\t\tcode: "custom",
\t\t\t\t\tpath: [field],
\t\t\t\t\tmessage: `${label} is required for S3 destinations`,
\t\t\t\t});
\t\t\t}
\t\t}
\t});'''
if old_ui_schema not in ui:
    raise SystemExit("destination UI schema block not found")
ui = ui.replace(old_ui_schema, new_ui_schema, 1)
ui = ui.replace(
    '\tconst { fields, append, remove } = useFieldArray({',
    '\tconst isCustomRclone =\n\t\tform.watch("provider") === CUSTOM_RCLONE_PROVIDER;\n\n\tconst { fields, append, remove } = useFieldArray({',
    1,
)
old_connection = '''\t\tconst connectionString = `:s3,provider=${provider},access_key_id=${accessKey},secret_access_key=${secretKey},endpoint=${endpoint}${region ? `,region=${region}` : ""}:${bucket}`;'''
new_connection = '''\t\tconst connectionString = isCustomRclone
\t\t\t? `${endpoint}${bucket ? `${endpoint.endsWith(":") || endpoint.endsWith("/") ? "" : "/"}${bucket.replace(/^\\/+/, "")}` : ""}`
\t\t\t: `:s3,provider=${provider},access_key_id=${accessKey},secret_access_key=${secretKey},endpoint=${endpoint}${region ? `,region=${region}` : ""}:${bucket}`;'''
if old_connection not in ui:
    raise SystemExit("connection string block not found")
ui = ui.replace(old_connection, new_connection, 1)
ui = ui.replace('<FormLabel>Access Key Id</FormLabel>', '<FormLabel>{isCustomRclone ? "Access Key Id (unused)" : "Access Key Id"}</FormLabel>', 1)
ui = ui.replace('<FormLabel>Secret Access Key</FormLabel>', '<FormLabel>{isCustomRclone ? "Secret Access Key (unused)" : "Secret Access Key"}</FormLabel>', 1)
ui = ui.replace('<FormLabel>Bucket</FormLabel>', '<FormLabel>{isCustomRclone ? "Remote Base Path (optional)" : "Bucket"}</FormLabel>', 1)
ui = ui.replace('<FormLabel>Region</FormLabel>', '<FormLabel>{isCustomRclone ? "Region (unused)" : "Region"}</FormLabel>', 1)
ui = ui.replace('<FormLabel>Endpoint</FormLabel>', '<FormLabel>{isCustomRclone ? "Rclone Remote / Connection String" : "Endpoint"}</FormLabel>', 1)
ui = ui.replace('placeholder={"https://us.bucket.aws/s3"}', 'placeholder={isCustomRclone ? "gdrive: or :sftp,host=example.com:" : "https://us.bucket.aws/s3"}', 1)
ui_path.write_text(ui)

# Update all backup implementations to use provider-neutral flags and targets.
backup_dir = Path("packages/server/src/utils/backups")
for file in backup_dir.glob("*.ts"):
    if file.name == "utils.ts":
        continue
    text = file.read_text()
    original = text
    text = text.replace("getS3Credentials", "getRcloneCredentials")
    text = re.sub(
        r'const rcloneDestination = `:s3:\$\{destination\.bucket\}/\$\{([^}]+)\}`;',
        r'const rcloneDestination = getRcloneDestination(destination, \1);',
        text,
    )

    if file.name == "web-server.ts":
        text = text.replace(
            'import { getBackupTimestamp, getRcloneCredentials, normalizeS3Path } from "./utils";',
            'import {\n\tgetBackupTimestamp,\n\tgetRcloneCredentials,\n\tgetRcloneDestination,\n\tnormalizeS3Path,\n} from "./utils";',
            1,
        )
        text = text.replace(
            'const s3Path = `:s3:${destination.bucket}/${backup.appName}/${normalizeS3Path(backup.prefix)}${backupFileName}`;',
            'const rclonePath = getRcloneDestination(\n\t\t\tdestination,\n\t\t\t`${backup.appName}/${normalizeS3Path(backup.prefix)}${backupFileName}`,\n\t\t);',
            1,
        )
        text = text.replace('"${s3Path}"', '"${rclonePath}"')
        text = text.replace("upload backup to S3", "upload backup to destination")
        text = text.replace("Uploaded backup to S3", "Uploaded backup to destination")

    if file.name == "index.ts":
        text = text.replace(
            'import { getRcloneCredentials, normalizeS3Path, scheduleBackup } from "./utils";',
            'import {\n\tgetRcloneCredentials,\n\tgetRcloneDestination,\n\tnormalizeS3Path,\n\tscheduleBackup,\n} from "./utils";',
            1,
        )
        text = text.replace(
            'const backupFilesPath = `:s3:${destination.bucket}/${appName}/${normalizeS3Path(backup.prefix)}`;',
            'const backupFilesPath = getRcloneDestination(\n\t\t\tdestination,\n\t\t\t`${appName}/${normalizeS3Path(backup.prefix)}`,\n\t\t);',
            1,
        )
        text = text.replace('${backupFilesPath}`;', '${backupFilesPath}`;')
        text = text.replace('${backupFilesPath}{}', '${backupFilesPath}/{}')

    if text != original and "getRcloneDestination(" in text and 'from "./utils"' in text and "getRcloneDestination," not in text:
        text = text.replace(
            "\tgetBackupTimestamp,\n\tgetRcloneCredentials,",
            "\tgetBackupTimestamp,\n\tgetRcloneCredentials,\n\tgetRcloneDestination,",
            1,
        )

    file.write_text(text)

# Fail loudly if a destination-specific S3 target remains in the backup code.
remaining = []
for file in backup_dir.glob("*.ts"):
    if file.name != "utils.ts" and ':s3:${destination.bucket}' in file.read_text():
        remaining.append(str(file))
if remaining:
    raise SystemExit(f"Unconverted S3 destination paths remain: {remaining}")
PY

corepack enable
pnpm install --frozen-lockfile
pnpm --filter @dokploy/server typecheck
pnpm --filter dokploy typecheck
pnpm biome check packages/server/src/db/validations/destination.ts packages/server/src/db/schema/destination.ts packages/server/src/utils/backups apps/dokploy/server/api/routers/destination.ts apps/dokploy/components/dashboard/settings/destination --write

git diff --check
git status --short
