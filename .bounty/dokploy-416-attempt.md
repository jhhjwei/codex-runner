/attempt #416

I’m starting with a focused implementation plan for generic rclone-backed backup destinations while preserving the existing S3 flow:

1. Introduce a destination type/config abstraction without breaking current S3 records.
2. Add a generic rclone remote/config path for Google Drive, OneDrive, FTP and SFTP.
3. Reuse the abstraction for connection testing, upload and retention cleanup.
4. Add validation and tests for command construction and backward compatibility.
5. Submit a small first PR if the full UI + migration scope is too large for one review.

Please let me know if you prefer a staged PR or a single end-to-end change.