Implements the dependency maintenance requested in issue #44.

/claim #44

## What changed

- Updated compatible direct dependency requirements.
- Refreshed the lockfile to current compatible transitive versions.
- Added a dependency update report with the validation commands used.

## Validation

- `cargo fmt --all -- --check`
- `cargo check --all-targets`
- `cargo test --all`
- `cargo clippy --all-features --workspace -- -D warnings`

## Scope note

Breaking major-version upgrades are not forced unless they can be completed without destabilizing the existing API and test suite. Any deferred incompatible upgrades will be documented clearly.