# Initial Opportunity Archive Import — 2026-07-28

## Action completed

Created a version-controlled opportunity archive under `opportunity-pipeline/` and imported the currently recoverable active and rejected opportunities from the income-project context.

## Imported active/upstream records

- Dokploy #416 / PR #4918
- 1btc-news #33 Quantum Visualizer
- 1btc-news #30 Developer Power Map
- 1btc-news #29 Sales Agent
- 1btc-news #28 Satoshi Stash Monitor
- 1btc-news #39 Moltbook daily task
- Haveno #1093 remote-node transaction errors
- microG #2994 RCS support
- microG #2843 WearOS support
- AsyncAPI 2026 Microgrant program
- TypeORM #3357 historical lead pending re-verification

## Imported rejected records

- TypeORM #12578 — closed/completed
- Formbricks #3302 — stale aggregator result; original closed
- Strapi #11998 — stale aggregator result; original closed
- Haveno #792 — closed/completed

## Storage rules activated

- Canonical URL deduplication
- Aggregator-source merging
- L1–L12 funnel stages and D archive
- Evidence, verification, economics, next action, upgrade and drop conditions
- Public-data-only storage; no credentials or private customer information

## Remaining backfill

Older leads without reliable original URLs were not reconstructed from memory. They will be imported only after rediscovery and bottom-level verification.
