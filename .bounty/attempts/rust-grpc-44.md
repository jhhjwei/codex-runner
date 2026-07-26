/attempt #44

Implementation plan:

1. Audit direct and transitive dependencies from the current `main` branch.
2. Upgrade compatible dependencies in a reviewable change set and document any intentionally deferred breaking upgrades.
3. Resolve compilation or lint regressions caused by the upgrades.
4. Validate with `cargo check`, `cargo test`, `cargo fmt --check`, and `cargo clippy --all-features --workspace -- -D warnings`.
5. Submit a focused pull request with a dependency-change summary, validation results, and a short demo.

Before implementation begins, please confirm that this task remains available despite the existing unmerged submissions.