/claim #416

## Summary

Adds a provider-neutral custom rclone destination while preserving the existing S3 flow.

- adds **Custom rclone remote** to backup destination settings
- accepts a named rclone remote such as `gdrive:` / `onedrive:` or an on-the-fly connection string such as `:sftp,host=example.com,user=alice:`
- supports an optional remote base path
- reuses the same destination builder for connection tests, database backups, compose backups, web-server backups, and retention cleanup
- shell-quotes every generated destination argument and redacts passwords, tokens, secrets, and access keys from logs/errors
- keeps all existing S3 providers and credentials behavior unchanged
- updates backup logs to say “destination” instead of “S3”
- fixes the streaming backup path so database dumps are no longer executed twice before upload

This enables Google Drive, OneDrive, FTP, SFTP, and other rclone-supported backends without adding provider-specific database columns.

## Validation

- `pnpm --filter @dokploy/server typecheck`
- `pnpm --filter dokploy typecheck`
- Biome check on changed files
- `git diff --check`

## Notes

For OAuth-backed remotes such as Google Drive and OneDrive, a named remote already configured on the Dokploy host can be used. For stateless providers such as FTP and SFTP, an rclone connection string can be supplied directly.
