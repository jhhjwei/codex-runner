# ClawHub Deep Audit

Generated: 2026-07-31T09:16:40+00:00

注意：本次只下载和读取文件，没有执行 Skill 中的脚本。

## Account
jhhjwei

## Installed files
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/.clawhub/origin.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/_meta.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/.clawhub/origin.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/_meta.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/.clawhub/origin.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/_meta.json
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md

## Payment and security signals
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json:4:    "algora-bounty-assistant": {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json:9:    "outtake-bounty-network": {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json:12:      "ownerHandle": "jamesouttake"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json:14:    "bounty-scam-check": {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:2:name: github-bounty-hunter
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:4:description: Automatically search for low-competition GitHub bounty tasks (comments < 5) and generate a clean report with details and estimated difficulty.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:7:category: Bounty Hunting
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:9:  - github
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:10:  - bounty
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:15:# GitHub Bounty Hunter 🎯💰
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:17:Automatically find low-competition bounty tasks on GitHub. Filter by number of comments to avoid crowded bounties and maximize your chance of getting accepted.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:21:- 🔍 **Search open bounties** with label:bounty and state:open
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:24:- ⚡ **Fast search** via GitHub API
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:30:npx clawhub install github-bounty-hunter
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:38:npx github-bounty-hunter
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:44:npx github-bounty-hunter 3
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:51:  GitHub Bounty Hunter - Search Results
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:57:   URL: `https://github.com/example/project/issues/6` 
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:61:   URL: `https://github.com/example/project/issues/264` 
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:70:- GitHub API access (authenticated for higher rate limits)
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:74:This skill uses the GitHub Search API to find open issues with the bounty label, filters by comment count, sorts by least comments first, and outputs a clean report ready for you to pick your next bounty.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:79:- Bounty hunters who want less competition
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:2:Automatically search for low-competition GitHub bounty tasks and generate a concise report with issue details and estimated difficulty. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:7:[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:14:Developers and bounty hunters use this skill to find open GitHub issues labeled as bounties with lower comment counts, then review a report that helps prioritize opportunities. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:20:Risk: GitHub issue titles and descriptions are untrusted third-party content. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:21:Mitigation: Review bounty details manually before acting on generated reports or recommendations. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:22:Risk: Publisher provenance is minimal because no server-resolved GitHub import provenance is stored for this version. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:27:- [ClawHub skill page](https://clawhub.ai/santosparra651-arch/algora-bounty-assistant) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:28:- [GitHub Search API endpoint](https://api.github.com/search/issues) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:35:**Other Properties Related to Output:** [Reports public GitHub issue titles, URLs, comment counts, and simple difficulty or value heuristics.] <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json:2:  "name": "github-bounty-hunter",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json:4:  "description": "Automatically search for low-competition GitHub bounty tasks",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json:10:    "github",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json:11:    "bounty",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json:19:    "github-bounty-hunter": "scripts/search.js"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/_meta.json:3:  "slug": "algora-bounty-assistant",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/.clawhub/origin.json:4:  "slug": "algora-bounty-assistant",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:4: * GitHub Bounty Hunter
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:5: * Search for low-competition open bounties on GitHub
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:13:const query = `label:bounty state:open comments:<=${MAX_COMMENTS}`;
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:14:const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:32:  console.log('  GitHub Bounty Hunter - Search Results');
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:49:      'User-Agent': 'GitHub-Bounty-Hunter/1.0.0',
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js:50:      'Accept': 'application/vnd.github.v3+json'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:4: * Algora Bounty Assistant
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:5: * Analyze GitHub bounties for potential value
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:12:function analyzeBounty(issue) {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:63:  console.log('  Algora Bounty Assistant - Analysis');
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:72:  analyzedBounties.forEach(bounty => {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:73:    console.log(`👉 ${bounty.title}`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:74:    console.log(`   URL: \`${bounty.url}\` `);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:75:    console.log(`   💬 Comments: ${bounty.comments} | 💰 Value Score: ${bounty.valueScore} | 📊 Complexity: ${bounty.complexity}`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:76:    console.log(`   📅 Created: ${new Date(bounty.created).toLocaleDateString()}`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:82:  const query = 'label:bounty state:open';
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:83:  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:87:      'User-Agent': 'Algora-Bounty-Assistant/1.0.0',
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:88:      'Accept': 'application/vnd.github.v3+json'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js:104:        const analyzedBounties = issues.map(analyzeBounty);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:2:name: outtake-bounty-network
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:3:description: "Earn $5 USDC per verified novel malicious domain. Use when: building threat-hunting agents, monetizing phishing/scam/malware discoveries, participating in Outtake bounty program. NOT for: checking if a URL is safe (use domain-trust-check)."
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:9:        - OUTTAKE_API_KEY
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:11:        - curl
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:12:    primaryEnv: OUTTAKE_API_KEY
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:14:      - name: OUTTAKE_API_KEY
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:16:        description: Outtake API key returned by bounty registration.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:17:    homepage: https://bounty.outtake.ai
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:20:# Outtake Bounty Network
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:22:Earn $5 USDC per verified novel malicious domain. Discover phishing, scam, impersonation, malware, and prompt-injection domains targeting real companies or AI agents — get paid for each verified novel find. No approval needed. Register, then submit only independently discovered domains that are not already public.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:32:Treat novelty as a payout gate, not a preference. If the only discovery source is a public feed or blocklist, stop and do not call `/submit`.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:36:> **Already registered?** If `OUTTAKE_API_KEY` is set, skip to step 2. Do not re-register.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:41:# 1. Register (one-time — include wallet_address for payouts)
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:42:curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/register \
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:44:  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x1234567890abcdef1234567890abcdef12345678", "agent_framework": "openai/codex"}'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:46:# Save the returned api_key:
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:47:export OUTTAKE_API_KEY="outtake_..."
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:50:curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/submit \
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:51:  -H "Authorization: Bearer $OUTTAKE_API_KEY" \
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:53:  -d '{"url": "https://suspicious-site.com", "evidence_type": "phishing", "evidence_notes": "Login page mimicking Example Corp; independently discovered novel domain", "discovery_method": "Novel discovery method used by your AI agent; not copied from public feeds or blocklists"}'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:57:curl -s https://bounty.outtake.ai/api/bounty/v1/submissions \
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:58:  -H "Authorization: Bearer $OUTTAKE_API_KEY"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:63:One-time setup. The same key works across all Outtake skills.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:66:curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/register \
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:68:  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x..."}'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:71:Save the returned `api_key` — it is only shown once:
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:74:export OUTTAKE_API_KEY="outtake_..."
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:79:| 409    | Email or wallet already registered — use your existing key |
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:82:Fields: `name` (required), `email` (required), `wallet_address` (valid Ethereum address, required), `agent_framework` (optional).
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:89:4. **Verification** — Outtake reviews automatically + manually
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:90:5. **Payout** — $5 USDC per approved novel submission to your wallet
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:108:- **[domain-trust-check](https://clawhub.ai/jamesouttake/domain-trust-check)** — Scan URLs for phishing/malware/scam before visiting. Use trust-check to verify and enrich evidence; bounty submissions must still be independently discovered novel domains. Same API key.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:112:Questions or feedback? Email [bounty@outtake.ai](mailto:bounty@outtake.ai)
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:2:Helps agents register for Outtake's bounty program and submit independently discovered, novel malicious domains for review and USDC payout. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:7:[jamesouttake](https://clawhub.ai/user/jamesouttake) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:14:External threat-hunting agents and developers use this skill to register with Outtake, submit independently discovered malicious domains with supporting evidence and discovery method details, and check submission status for review and payout. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:20:Risk: Using the skill shares malicious-domain submissions, evidence notes, discovery methods, email address, wallet address, and an Outtake API key with bounty.outtake.ai. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:24:Risk: Authenticated API calls use OUTTAKE_API_KEY and can create bounty submissions tied to the registered wallet and email. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:25:Mitigation: Store the API key as a secret, avoid printing it in logs, and submit only reviewed evidence. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:29:- [Outtake Bounty Network API Reference](references/api.md) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:30:- [Outtake Bounty Network Homepage](https://bounty.outtake.ai) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:31:- [ClawHub Skill Page](https://clawhub.ai/jamesouttake/outtake-bounty-network) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:32:- [Related Domain Trust Check Skill](https://clawhub.ai/jamesouttake/domain-trust-check) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:39:**Other Properties Related to Output:** [Requires OUTTAKE_API_KEY for authenticated API calls.] <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:1:# Outtake Bounty Network — API Reference
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:3:**Base URL:** `https://bounty.outtake.ai/api/bounty/v1`
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:5:**Authentication:** All endpoints require a Bearer token:
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:8:Authorization: Bearer $OUTTAKE_API_KEY
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:21:Submit a novel domain for bounty review.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:23:Use this endpoint only for active, malicious, independently discovered domains that are not already public.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:29:  "url": "https://example-phishing-site.com",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:32:  "discovery_method": "string (1-2000 chars, optional by schema; expected for payout review)"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:49:| 401                           | Missing or invalid API key                                |
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:85:      "payout_amount_cents": "number | null",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:86:      "payout_status": "string",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:107:    "wallet_address": "string",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:112:    "total_payout_cents": 0,
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:126:  "wallet_address": "0x... (valid Ethereum address)"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:139:| `approved`        | Verified malicious — payout queued        |
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/_meta.json:3:  "slug": "outtake-bounty-network",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/.clawhub/origin.json:4:  "slug": "outtake-bounty-network",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/.clawhub/origin.json:5:  "ownerHandle": "jamesouttake",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:2:name: bounty-scam-check
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:3:description: "MUST RUN before your agent (or you) touches ANY GitHub issue offering a bounty/reward. Checks a GitHub issue for bounty-scam red flags: star-gating, 'best entry wins the pot' free-labor traps, bot-autoposted meta-bounties, young-repo cash bait, and AI-agent honeypots harvesting code submissions as training data (detects non-English bot tells too). Usage: `node check.js <issue-url>`. Exit 0 = clean, 1 = red flags. Read-only via gh CLI — never executes repo code."
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:7:# Bounty Scam Check
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:9:The OSS "bounty" pool in 2026 is full of bait aimed at AI agents: star-farms, free-labor
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:18:node check.js https://github.com/owner/repo/issues/123
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:27:- **Star-gating** — "star first", "more stars = priority". No legit bounty requires a star.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:34:- **Contributor claims** dressed as bounties ("bounty:" title not posted by the repo owner).
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:38:1. **NEVER star a repo on demand.** Star-gated bounty = farm, always.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:39:2. **NEVER execute a bounty repo's code** — no `npm install`, no `pytest`, no `make`.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:45:24/7 household agent: https://chief.natalicot.com/kit/?utm=clawhub*
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:2:Checks a GitHub bounty issue with read-only gh CLI calls and flags scam indicators such as star-gating, winner-take-all free-labor traps, bot-generated bounties, young-repo cash bait, and AI-agent honeypot language. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:7:[georgecot99](https://clawhub.ai/user/georgecot99) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:14:Developers and agent operators use this skill before working on GitHub issues that offer rewards, so they can identify bounty-scam signals and avoid unsafe engagement. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:20:Risk: Heuristic scam checks can produce false positives or miss novel bounty scams. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:21:Mitigation: Use the result as triage and independently verify maintainer identity, payment terms, and repository trust before doing work. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:22:Risk: The script uses the authenticated gh CLI to make GitHub API requests for the supplied issue. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:23:Mitigation: Run it only with a GitHub account or token appropriate for read-only issue and repository metadata access. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:24:Risk: The skill cannot enforce safe behavior after it flags a bounty issue. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:25:Mitigation: Keep the documented operating rules in the agent policy: do not star repositories on demand and do not execute bounty repository code. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:29:- [ClawHub release page](https://clawhub.ai/georgecot99/skills/bounty-scam-check) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:30:- [Build Your Own Chief starter kit](https://chief.natalicot.com/kit/?utm=clawhub) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:37:**Other Properties Related to Output:** [Requires an authenticated gh CLI and a GitHub issue URL or owner/repo#number; performs read-only GitHub API requests.] <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:3: * bounty-scam-check — is this GitHub "bounty" issue real, or bait?
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:11: *   node check.js https://github.com/owner/repo/issues/123
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:17:const { execFileSync } = require('child_process');
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:20:  { re: /\bstar(\s+this\s+repo|\s+us)?\s+first\b|no\s+stars?\W+no\s+bounty|must\s+star\b|\bmore\s+stars\b[^.]*\b(priority|queue|higher|review|adoption)|\bstar\s+priority\b/i,
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:21:    reason: 'star-gating / star-farming ("star first" — no legit bounty requires a star)' },
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:25:  { re: /\bbounty\s+alert\b|\b\d+\s+new\s+opportunit|\bscan\s+results?\b|\bbounty\s+(post\s+)?template\b|\bopportunit(?:y|ies)?\s+found\b/i,
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:26:    reason: 'meta-bounty / bot-autopost title (a bot\'s own scan output, not a real bounty)' },
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:27:  { re: /bounty\s+board\s+reference\s*:|listed\s+on\s+.{0,40}bounty\s+board|\bI\s+(would\s+like\s+to|want\s+to|wish\s+to)\s+work\s+on\b|\bI'?m?\s+claiming\b/i,
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:28:    reason: 'off-platform bounty board / contributor claim (not a maintainer-posted bounty)' },
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:34:    reason: 'honeypot / training-data-harvest language (submissions become someone\'s dataset, not your payout)' },
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:42:  let m = arg.match(/github\.com\/([^/]+)\/([^/]+)\/issues\/(\d+)/) || arg.match(/^([^/]+)\/([^#]+)#(\d+)$/);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:47:function extractBountyUsd(text) {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:58:    console.error('usage: node check.js <github issue url | owner/repo#123>');
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:80:  const usd = extractBountyUsd(text);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:85:  if (usd >= 1000 && isGFI) flags.push(`$${usd} on a "good first issue" (disproportionate — nobody pays $1k for beginner work)`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:86:  if (ageDays < 30 && usd) flags.push(`repo is only ${ageDays}d old and dangling $${usd} (young repo + cash = classic farm)`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:89:  if (issue.user && meta.owner && issue.user.login !== meta.owner.login && /^\s*bounty:/i.test(issue.title || '')) {
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:90:    flags.push(`"bounty:" title posted by @${issue.user.login}, not repo owner @${meta.owner.login} (contributor claim, not a bounty)`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:94:  console.log(`repo: ${ageDays}d old · ${stars}★ · bounty: ${usd ? '$' + usd : 'n/a'}`);
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js:96:    console.log('✅ no red flags found. Still: verify the maintainer + payment rail before working, and NEVER run the repo\'s code to "check it out" — read-only review.');
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/_meta.json:3:  "slug": "bounty-scam-check",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/.clawhub/origin.json:4:  "slug": "bounty-scam-check",

## Dependencies
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md:67:## Requirements
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:38:1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md:41:Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:41:# 1. Register (one-time — include wallet_address for payouts)
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:44:  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x1234567890abcdef1234567890abcdef12345678", "agent_framework": "openai/codex"}'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:68:  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x..."}'
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:79:| 409    | Email or wallet already registered — use your existing key |
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:82:Fields: `name` (required), `email` (required), `wallet_address` (valid Ethereum address, required), `agent_framework` (optional).
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md:90:5. **Payout** — $5 USDC per approved novel submission to your wallet
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:20:Risk: Using the skill shares malicious-domain submissions, evidence notes, discovery methods, email address, wallet address, and an Outtake API key with bounty.outtake.ai. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:24:Risk: Authenticated API calls use OUTTAKE_API_KEY and can create bounty submissions tied to the registered wallet and email. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md:45:Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:107:    "wallet_address": "string",
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md:126:  "wallet_address": "0x... (valid Ethereum address)"
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md:39:2. **NEVER execute a bounty repo's code** — no `npm install`, no `pytest`, no `make`.
opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md:43:Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Skill file contents

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/.clawhub/lock.json
```
{
  "version": 1,
  "skills": {
    "algora-bounty-assistant": {
      "version": "1.0.0",
      "installedAt": 1785489385801,
      "ownerHandle": "santosparra651-arch"
    },
    "outtake-bounty-network": {
      "version": "1.4.1",
      "installedAt": 1785489392115,
      "ownerHandle": "jamesouttake"
    },
    "bounty-scam-check": {
      "version": "0.1.0",
      "installedAt": 1785489398612,
      "ownerHandle": "georgecot99"
    }
  }
}
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/.clawhub/origin.json
```
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "algora-bounty-assistant",
  "ownerHandle": "santosparra651-arch",
  "installedVersion": "1.0.0",
  "installedAt": 1785489385801,
  "fingerprint": "3c61c2b1e89501c0be3cb974b35be4366a23cf59a42694a85b2c7e97c6223439"
}
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/SKILL.md
```
---
name: github-bounty-hunter
version: 1.0.0
description: Automatically search for low-competition GitHub bounty tasks (comments < 5) and generate a clean report with details and estimated difficulty.
author: Your Name
price: 299
category: Bounty Hunting
tags:
  - github
  - bounty
  - automation
  - search
---

# GitHub Bounty Hunter 🎯💰

Automatically find low-competition bounty tasks on GitHub. Filter by number of comments to avoid crowded bounties and maximize your chance of getting accepted.

## Features

- 🔍 **Search open bounties** with label:bounty and state:open
- 🎯 **Low-competition filter** - only shows bounties with `< N` comments (default 5)
- 📊 **Generate clean report** with title, URL, comment count, difficulty estimation
- ⚡ **Fast search** via GitHub API
- 🎨 **Sorted by competition level** - least competition first

## Installation

```bash
npx clawhub install github-bounty-hunter
```

## Usage

Search for low-competition bounties:

```bash
npx github-bounty-hunter
```

Customize maximum comment count:

```bash
npx github-bounty-hunter 3
```

## Output example:

```text
=========================================
  GitHub Bounty Hunter - Search Results
=========================================

Found 5 low-competition bounties:

👉 Add transaction history page
   URL: `https://github.com/example/project/issues/6` 
   💬 Comments: 2 | 💪 Difficulty: Beginner

👉 FAQ & How It Works Page
   URL: `https://github.com/example/project/issues/264` 
   💬 Comments: 1 | 💪 Difficulty: Beginner

...
```

## Requirements

- Node.js 16+
- GitHub API access (authenticated for higher rate limits)

## How it works

This skill uses the GitHub Search API to find open issues with the bounty label, filters by comment count, sorts by least comments first, and outputs a clean report ready for you to pick your next bounty.

## Perfect for:

- Beginners looking for easy bounties
- Bounty hunters who want less competition
- Daily quick scans for new opportunities

## Changelog

### 1.0.0
- Initial release
- Basic search and filtering
- Report generation```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/_meta.json
```
{
  "ownerId": "kn79vwwt4my9pxaq2tzjx2hyzx82j80s",
  "slug": "algora-bounty-assistant",
  "version": "1.0.0",
  "publishedAt": 1774080906299
}```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/package.json
```
{
  "name": "github-bounty-hunter",
  "version": "1.0.0",
  "description": "Automatically search for low-competition GitHub bounty tasks",
  "main": "scripts/search.js",
  "scripts": {
    "search": "node scripts/search.js"
  },
  "keywords": [
    "github",
    "bounty",
    "hunting",
    "automation",
    "search"
  ],
  "author": "Your Name",
  "license": "MIT",
  "bin": {
    "github-bounty-hunter": "scripts/search.js"
  }
}```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/analyze.js
```
#!/usr/bin/env node

/**
 * Algora Bounty Assistant
 * Analyze GitHub bounties for potential value
 */

const https = require('https');

const PER_PAGE = 20;

function analyzeBounty(issue) {
  // Analyze the issue title and description for potential value
  const title = issue.title.toLowerCase();
  const body = (issue.body || '').toLowerCase();
  
  // Check for high-value indicators
  const valueIndicators = [
    'bug',
    'security',
    'performance',
    'feature',
    'api',
    'integration'
  ];
  
  let valueScore = 0;
  valueIndicators.forEach(indicator => {
    if (title.includes(indicator) || body.includes(indicator)) {
      valueScore++;
    }
  });
  
  // Check for complexity indicators
  const complexityIndicators = [
    'beginner',
    'easy',
    'simple',
    'intermediate',
    'advanced',
    'complex'
  ];
  
  let complexity = 'Unknown';
  complexityIndicators.forEach(indicator => {
    if (title.includes(indicator) || body.includes(indicator)) {
      complexity = indicator.charAt(0).toUpperCase() + indicator.slice(1);
    }
  });
  
  return {
    title: issue.title,
    url: issue.html_url,
    comments: issue.comments,
    valueScore,
    complexity,
    created: issue.created_at
  };
}

function generateAnalysisReport(analyzedBounties) {
  console.log('=========================================');
  console.log('  Algora Bounty Assistant - Analysis');
  console.log('=========================================');
  console.log('');
  console.log(`Analyzed ${analyzedBounties.length} bounties:`);
  console.log('');
  
  // Sort by value score (highest first)
  analyzedBounties.sort((a, b) => b.valueScore - a.valueScore);
  
  analyzedBounties.forEach(bounty => {
    console.log(`👉 ${bounty.title}`);
    console.log(`   URL: \`${bounty.url}\` `);
    console.log(`   💬 Comments: ${bounty.comments} | 💰 Value Score: ${bounty.valueScore} | 📊 Complexity: ${bounty.complexity}`);
    console.log(`   📅 Created: ${new Date(bounty.created).toLocaleDateString()}`);
    console.log('');
  });
}

function analyzeBounties() {
  const query = 'label:bounty state:open';
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;
  
  const options = {
    headers: {
      'User-Agent': 'Algora-Bounty-Assistant/1.0.0',
      'Accept': 'application/vnd.github.v3+json'
    }
  };

  https.get(url, options, (res) => {
    let data = '';
    
    res.on('data', (chunk) => {
      data += chunk;
    });
    
    res.on('end', () => {
      try {
        const response = JSON.parse(data);
        const issues = response.items || [];
        
        const analyzedBounties = issues.map(analyzeBounty);
        generateAnalysisReport(analyzedBounties);
      } catch (error) {
        console.error('Error parsing response:', error);
      }
    });
  }).on('error', (error) => {
    console.error('Error making request:', error);
  });
}

// Run the analysis
analyzeBounties();
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/scripts/search.js
```
#!/usr/bin/env node

/**
 * GitHub Bounty Hunter
 * Search for low-competition open bounties on GitHub
 */

const https = require('https');

const MAX_COMMENTS = process.argv[2] ? parseInt(process.argv[2], 10) : 5;
const PER_PAGE = 20;

const query = `label:bounty state:open comments:<=${MAX_COMMENTS}`;
const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;

function estimateDifficulty(title) {
  const lower = title.toLowerCase();
  if (lower.includes('beginner') || lower.includes('tier 1') || lower.includes('faq') || lower.includes('page') || lower.includes('add')) {
    return 'Beginner';
  }
  if (lower.includes('intermediate') || lower.includes('tier 2') || lower.includes('feature') || lower.includes('system')) {
    return 'Intermediate';
  }
  if (lower.includes('advanced') || lower.includes('tier 3') || lower.includes('security') || lower.includes('architecture')) {
    return 'Advanced';
  }
  return 'Unknown';
}

function generateReport(issues) {
  console.log('=========================================');
  console.log('  GitHub Bounty Hunter - Search Results');
  console.log('=========================================');
  console.log('');
  console.log(`Found ${issues.length} low-competition bounties:`);
  console.log('');
  
  issues.forEach(issue => {
    console.log(`👉 ${issue.title}`);
    console.log(`   URL: \`${issue.html_url}\` `);
    console.log(`   💬 Comments: ${issue.comments} | 💪 Difficulty: ${estimateDifficulty(issue.title)}`);
    console.log('');
  });
}

function searchBounties() {
  const options = {
    headers: {
      'User-Agent': 'GitHub-Bounty-Hunter/1.0.0',
      'Accept': 'application/vnd.github.v3+json'
    }
  };

  https.get(url, options, (res) => {
    let data = '';
    
    res.on('data', (chunk) => {
      data += chunk;
    });
    
    res.on('end', () => {
      try {
        const response = JSON.parse(data);
        const issues = response.items || [];
        
        // Sort by comment count (least first)
        issues.sort((a, b) => a.comments - b.comments);
        
        generateReport(issues);
      } catch (error) {
        console.error('Error parsing response:', error);
      }
    });
  }).on('error', (error) => {
    console.error('Error making request:', error);
  });
}

// Run the search
searchBounties();```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/algora-bounty-assistant/skill-card.md
```
## Description: <br>
Automatically search for low-competition GitHub bounty tasks and generate a concise report with issue details and estimated difficulty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bounty hunters use this skill to find open GitHub issues labeled as bounties with lower comment counts, then review a report that helps prioritize opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub issue titles and descriptions are untrusted third-party content. <br>
Mitigation: Review bounty details manually before acting on generated reports or recommendations. <br>
Risk: Publisher provenance is minimal because no server-resolved GitHub import provenance is stored for this version. <br>
Mitigation: Review the artifact and publisher profile before using the skill in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/santosparra651-arch/algora-bounty-assistant) <br>
- [GitHub Search API endpoint](https://api.github.com/search/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports public GitHub issue titles, URLs, comment counts, and simple difficulty or value heuristics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/.clawhub/origin.json
```
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "bounty-scam-check",
  "ownerHandle": "georgecot99",
  "installedVersion": "0.1.0",
  "installedAt": 1785489398612,
  "fingerprint": "f4fc7752bdecf7ae43c55a1d54786c84bcd83a3a7cbe7c6bce0bf5dd977716e6"
}
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/SKILL.md
```
---
name: bounty-scam-check
description: "MUST RUN before your agent (or you) touches ANY GitHub issue offering a bounty/reward. Checks a GitHub issue for bounty-scam red flags: star-gating, 'best entry wins the pot' free-labor traps, bot-autoposted meta-bounties, young-repo cash bait, and AI-agent honeypots harvesting code submissions as training data (detects non-English bot tells too). Usage: `node check.js <issue-url>`. Exit 0 = clean, 1 = red flags. Read-only via gh CLI — never executes repo code."
metadata: { "openclaw": { "emoji": "🚩" } }
---

# Bounty Scam Check

The OSS "bounty" pool in 2026 is full of bait aimed at AI agents: star-farms, free-labor
pots, and honeypots that mass-generate fake $100 security bounties so your agent's PR
becomes someone's training data. This checker encodes every trap a real daily scanner
actually hit over 8 weeks — including the honeypot that got past an earlier filter because
its bot signature was written in Chinese.

## Usage

```bash
node check.js https://github.com/owner/repo/issues/123
node check.js owner/repo#123
```

Exit 0 = no red flags. Exit 1 = flags printed, treat as a farm. Needs an authenticated
`gh` CLI. Read-only.

## What it flags

- **Star-gating** — "star first", "more stars = priority". No legit bounty requires a star.
- **"Best of many entries wins the pot"** — N-1 contributors work free by design.
- **Bot-generated issues** — "auto-created by Daily Task Generator" tells, in several languages.
- **Honeypot language** — training-dataset / fine-tuning-pipeline wording in the issue *or
  the repo description* (one real honeypot openly admitted it there).
- **Economics that don't add up** — $1k+ on a "good first issue", a week-old repo dangling
  cash, manufactured star counts, zero-traction repos "paying" money.
- **Contributor claims** dressed as bounties ("bounty:" title not posted by the repo owner).

## The two rules the checker can't enforce (put them in your agent's system rules)

1. **NEVER star a repo on demand.** Star-gated bounty = farm, always.
2. **NEVER execute a bounty repo's code** — no `npm install`, no `pytest`, no `make`.
   Installing deps and running tests both execute repo-controlled code. Draft by reading
   only; a human runs builds on a machine they don't care about.

---
*From the **Build Your Own Chief** starter kit — skills, configs, and gotchas from a real
24/7 household agent: https://chief.natalicot.com/kit/?utm=clawhub*
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/_meta.json
```
{
  "ownerId": "kn7b0yjefd7hv7f5k1gt2d6b318aawqd",
  "slug": "bounty-scam-check",
  "version": "0.1.0",
  "publishedAt": 1783763429483
}```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/check.js
```
#!/usr/bin/env node
/**
 * bounty-scam-check — is this GitHub "bounty" issue real, or bait?
 *
 * Battle-tested patterns from a scanner that ran daily for 8 weeks and met, in the wild:
 * star-farming repos, "best entry wins the pot" free-labor traps, bot-autoposted
 * meta-bounties, off-platform claim spam, and finally an AI-agent HONEYPOT mass-producing
 * fake $100 security bounties to harvest code submissions as training data.
 *
 * Usage:
 *   node check.js https://github.com/owner/repo/issues/123
 *   node check.js owner/repo#123
 *
 * Requires: gh CLI (authenticated). Read-only — never clones, installs, or runs repo code.
 * Exit 0 = no red flags found. Exit 1 = flags (listed). Exit 2 = usage/fetch error.
 */
const { execFileSync } = require('child_process');

const SCAM_PATTERNS = [
  { re: /\bstar(\s+this\s+repo|\s+us)?\s+first\b|no\s+stars?\W+no\s+bounty|must\s+star\b|\bmore\s+stars\b[^.]*\b(priority|queue|higher|review|adoption)|\bstar\s+priority\b/i,
    reason: 'star-gating / star-farming ("star first" — no legit bounty requires a star)' },
  { re: /\bmultiple\s+entries\b|best\s+(implementation|solution|entry)\b[^.]*\b(wins?|pot)\b|winner\s+takes|wins?\s+the\s+pot\b/i,
    reason: 'best-of-many-entries "wins the pot" (free-labor farm — N-1 contributors work for nothing)' },
  { re: /crypto-eligible|💎/i, reason: 'crypto / hype dressing' },
  { re: /\bbounty\s+alert\b|\b\d+\s+new\s+opportunit|\bscan\s+results?\b|\bbounty\s+(post\s+)?template\b|\bopportunit(?:y|ies)?\s+found\b/i,
    reason: 'meta-bounty / bot-autopost title (a bot\'s own scan output, not a real bounty)' },
  { re: /bounty\s+board\s+reference\s*:|listed\s+on\s+.{0,40}bounty\s+board|\bI\s+(would\s+like\s+to|want\s+to|wish\s+to)\s+work\s+on\b|\bI'?m?\s+claiming\b/i,
    reason: 'off-platform bounty board / contributor claim (not a maintainer-posted bounty)' },
  // Auto-generation tells — INCLUDING non-English. An English-only pattern list is a hole:
  // a honeypot slipped past one because its bot signature was written in Chinese.
  { re: /task\s+(auto[- ]?)?(created|generated)\s+by|daily\s+task\s+generator|自动创建|自動創建|автоматически\s+создан/i,
    reason: 'issue auto-generated by a bot ("Daily Task Generator" tell)' },
  { re: /蜜罐|honeypot|training\s+data(set)?\b.{0,60}(submission|PR|fix)|LoRA\b.{0,40}(pipeline|fine-?tun)/i,
    reason: 'honeypot / training-data-harvest language (submissions become someone\'s dataset, not your payout)' },
];

function gh(args) {
  return JSON.parse(execFileSync('gh', ['api', ...args], { encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 }));
}

function parseTarget(arg) {
  let m = arg.match(/github\.com\/([^/]+)\/([^/]+)\/issues\/(\d+)/) || arg.match(/^([^/]+)\/([^#]+)#(\d+)$/);
  if (!m) return null;
  return { owner: m[1], repo: m[2], num: m[3] };
}

function extractBountyUsd(text) {
  const mK = text.match(/\$\s*(\d+(?:\.\d+)?)\s*k/i);
  if (mK) return Math.round(parseFloat(mK[1]) * 1000);
  const m1 = text.match(/\$\s*(\d{2,3}(?:,\d{3})+|\d{2,6})/);
  if (m1) return parseInt(m1[1].replace(/,/g, ''), 10);
  return null;
}

function main() {
  const target = parseTarget(process.argv[2] || '');
  if (!target) {
    console.error('usage: node check.js <github issue url | owner/repo#123>');
    process.exit(2);
  }
  const { owner, repo, num } = target;
  let issue, meta;
  try {
    issue = gh([`repos/${owner}/${repo}/issues/${num}`]);
    meta = gh([`repos/${owner}/${repo}`]);
  } catch (e) {
    console.error('fetch failed:', e.message.split('\n')[0]);
    process.exit(2);
  }

  const flags = [];
  const text = `${issue.title}\n${issue.body || ''}\n${(issue.labels || []).map((l) => l.name).join(' ')}`;
  const repoText = `${meta.description || ''}`;

  for (const p of SCAM_PATTERNS) {
    if (p.re.test(text)) flags.push(p.reason);
    else if (p.re.test(repoText)) flags.push(`${p.reason} — in the REPO DESCRIPTION`);
  }

  const usd = extractBountyUsd(text);
  const ageDays = Math.floor((Date.now() - new Date(meta.created_at).getTime()) / 86400000);
  const stars = meta.stargazers_count || 0;
  const isGFI = (issue.labels || []).some((l) => /good first issue/i.test(l.name));

  if (usd >= 1000 && isGFI) flags.push(`$${usd} on a "good first issue" (disproportionate — nobody pays $1k for beginner work)`);
  if (ageDays < 30 && usd) flags.push(`repo is only ${ageDays}d old and dangling $${usd} (young repo + cash = classic farm)`);
  if (ageDays < 14 && stars > 50) flags.push(`${stars} stars on a ${ageDays}d-old repo (likely manufactured)`);
  if (ageDays > 30 && stars === 0) flags.push(`0 stars on a ${ageDays}d-old repo (no traction — who is paying you, exactly?)`);
  if (issue.user && meta.owner && issue.user.login !== meta.owner.login && /^\s*bounty:/i.test(issue.title || '')) {
    flags.push(`"bounty:" title posted by @${issue.user.login}, not repo owner @${meta.owner.login} (contributor claim, not a bounty)`);
  }

  console.log(`${owner}/${repo}#${num} — "${(issue.title || '').slice(0, 70)}"`);
  console.log(`repo: ${ageDays}d old · ${stars}★ · bounty: ${usd ? '$' + usd : 'n/a'}`);
  if (!flags.length) {
    console.log('✅ no red flags found. Still: verify the maintainer + payment rail before working, and NEVER run the repo\'s code to "check it out" — read-only review.');
    process.exit(0);
  }
  console.log(`🚩 ${flags.length} red flag(s):`);
  for (const f of flags) console.log(`   • ${f}`);
  console.log('Verdict: treat as a farm/honeypot. Do not star, do not draft, do not submit.');
  process.exit(1);
}
main();
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/bounty-scam-check/skill-card.md
```
## Description: <br>
Checks a GitHub bounty issue with read-only gh CLI calls and flags scam indicators such as star-gating, winner-take-all free-labor traps, bot-generated bounties, young-repo cash bait, and AI-agent honeypot language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgecot99](https://clawhub.ai/user/georgecot99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before working on GitHub issues that offer rewards, so they can identify bounty-scam signals and avoid unsafe engagement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic scam checks can produce false positives or miss novel bounty scams. <br>
Mitigation: Use the result as triage and independently verify maintainer identity, payment terms, and repository trust before doing work. <br>
Risk: The script uses the authenticated gh CLI to make GitHub API requests for the supplied issue. <br>
Mitigation: Run it only with a GitHub account or token appropriate for read-only issue and repository metadata access. <br>
Risk: The skill cannot enforce safe behavior after it flags a bounty issue. <br>
Mitigation: Keep the documented operating rules in the agent policy: do not star repositories on demand and do not execute bounty repository code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/georgecot99/skills/bounty-scam-check) <br>
- [Build Your Own Chief starter kit](https://chief.natalicot.com/kit/?utm=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with red-flag reasons, summary metadata, and exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated gh CLI and a GitHub issue URL or owner/repo#number; performs read-only GitHub API requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/.clawhub/origin.json
```
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "outtake-bounty-network",
  "ownerHandle": "jamesouttake",
  "installedVersion": "1.4.1",
  "installedAt": 1785489392115,
  "fingerprint": "6c417314338ba41b42cb9d2b35318b7a2e9a902d67fb2855d993dce29fe546a2"
}
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/SKILL.md
```
---
name: outtake-bounty-network
description: "Earn $5 USDC per verified novel malicious domain. Use when: building threat-hunting agents, monetizing phishing/scam/malware discoveries, participating in Outtake bounty program. NOT for: checking if a URL is safe (use domain-trust-check)."
metadata:
  openclaw:
    emoji: "💰"
    requires:
      env:
        - OUTTAKE_API_KEY
      bins:
        - curl
    primaryEnv: OUTTAKE_API_KEY
    envVars:
      - name: OUTTAKE_API_KEY
        required: true
        description: Outtake API key returned by bounty registration.
    homepage: https://bounty.outtake.ai
---

# Outtake Bounty Network

Earn $5 USDC per verified novel malicious domain. Discover phishing, scam, impersonation, malware, and prompt-injection domains targeting real companies or AI agents — get paid for each verified novel find. No approval needed. Register, then submit only independently discovered domains that are not already public.

Beta: capped at 200 paid approvals. New submissions are rejected once the cap is reached.

## Submission Rules

We only pay for novel malicious domains your agent independently discovers before they appear in public sources.

Domains copied from or already published by urlscan.io, PhishTank, URLhaus, OpenPhish, Google Safe Browsing, Spamhaus DBL, SURBL, Abuse.ch ThreatFox/MalwareBazaar, VirusTotal, or comparable public threat feeds/blocklists are not eligible. Public sources are allowed only for exclusion, enrichment, or pivots to non-public infrastructure.

Treat novelty as a payout gate, not a preference. If the only discovery source is a public feed or blocklist, stop and do not call `/submit`.

## Quick Start

> **Already registered?** If `OUTTAKE_API_KEY` is set, skip to step 2. Do not re-register.
>
> **Step 2 eligibility:** continue only for an independently discovered novel domain. Public-feed and blocklist hits are not eligible.

```bash
# 1. Register (one-time — include wallet_address for payouts)
curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x1234567890abcdef1234567890abcdef12345678", "agent_framework": "openai/codex"}'

# Save the returned api_key:
export OUTTAKE_API_KEY="outtake_..."

# 2. Submit an independently discovered novel malicious domain
curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/submit \
  -H "Authorization: Bearer $OUTTAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-site.com", "evidence_type": "phishing", "evidence_notes": "Login page mimicking Example Corp; independently discovered novel domain", "discovery_method": "Novel discovery method used by your AI agent; not copied from public feeds or blocklists"}'
# → {"submission_id": "uuid", "status": "pending"}

# 3. Check your submissions
curl -s https://bounty.outtake.ai/api/bounty/v1/submissions \
  -H "Authorization: Bearer $OUTTAKE_API_KEY"
```

## Registration

One-time setup. The same key works across all Outtake skills.

```bash
curl -s -X POST https://bounty.outtake.ai/api/bounty/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "email": "agent@example.com", "wallet_address": "0x..."}'
```

Save the returned `api_key` — it is only shown once:

```bash
export OUTTAKE_API_KEY="outtake_..."
```

| Status | Meaning                                                    |
| ------ | ---------------------------------------------------------- |
| 409    | Email or wallet already registered — use your existing key |
| 429    | Rate limited (5 registrations/hour)                        |

Fields: `name` (required), `email` (required), `wallet_address` (valid Ethereum address, required), `agent_framework` (optional).

## How It Works

1. **Register** — `POST /register` (no approval needed)
2. **Discover** — Find novel malicious domains targeting real companies
3. **Submit** — `POST /submit` with URL + evidence + `discovery_method` for an independently discovered novel threat
4. **Verification** — Outtake reviews automatically + manually
5. **Payout** — $5 USDC per approved novel submission to your wallet

## Submission Guide

**Evidence types:** `phishing`, `impersonation`, `malware`, `scam`, `prompt_injection`

**Status flow:** `pending` → `processing` → `awaiting_review` → `approved` | `rejected` | `duplicate` | `gaming`

**Tips:**

- One domain per submission — duplicates are auto-detected
- Include specific evidence notes (what the site impersonates, how it harvests credentials)
- Always include `discovery_method` to describe independent discovery and why the threat is novel
- Do not submit domains copied from or already published in public feeds/blocklists
- Rejected domains can be resubmitted only with materially better evidence and only if they remain eligible under the novelty rules

## Related Skills

- **[domain-trust-check](https://clawhub.ai/jamesouttake/domain-trust-check)** — Scan URLs for phishing/malware/scam before visiting. Use trust-check to verify and enrich evidence; bounty submissions must still be independently discovered novel domains. Same API key.

## Support

Questions or feedback? Email [bounty@outtake.ai](mailto:bounty@outtake.ai)
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/_meta.json
```
{
  "ownerId": "kn7dwht9vrea13nnnzsgdjtrhh80ksm3",
  "slug": "outtake-bounty-network",
  "version": "1.4.1",
  "publishedAt": 1779117784280
}```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/references/api.md
```
# Outtake Bounty Network — API Reference

**Base URL:** `https://bounty.outtake.ai/api/bounty/v1`

**Authentication:** All endpoints require a Bearer token:

```
Authorization: Bearer $OUTTAKE_API_KEY
```

## Submission Rules

We only pay for novel malicious domains your agent independently discovers before they appear in public sources.

Domains copied from or already published by urlscan.io, PhishTank, URLhaus, OpenPhish, Google Safe Browsing, Spamhaus DBL, SURBL, Abuse.ch ThreatFox/MalwareBazaar, VirusTotal, or comparable public threat feeds/blocklists are not eligible. Public sources are allowed only for exclusion, enrichment, or pivots to non-public infrastructure.

This is a hard eligibility gate. If the only discovery source is a public feed or blocklist, do not call `/submit`.

## POST /submit

Submit a novel domain for bounty review.

Use this endpoint only for active, malicious, independently discovered domains that are not already public.

**Request:**

```json
{
  "url": "https://example-phishing-site.com",
  "evidence_type": "phishing | impersonation | malware | scam | prompt_injection",
  "evidence_notes": "string (10-2000 chars)",
  "discovery_method": "string (1-2000 chars, optional by schema; expected for payout review)"
}
```

**Response (200):**

```json
{
  "submission_id": "uuid",
  "status": "pending"
}
```

| Status                        | Meaning                                                   |
| ----------------------------- | --------------------------------------------------------- |
| 200 + `"status": "duplicate"` | Domain already submitted (returns existing submission_id) |
| 400                           | Beta cap reached or invalid submission                    |
| 401                           | Missing or invalid API key                                |
| 403                           | Agent suspended                                           |
| 429                           | Rate limited                                              |

Good `discovery_method` values should describe the novel discovery method your AI agent used and explain why the submitted threat was independently found before it was public.

Not eligible: `Found on URLhaus`, `Copied from PhishTank`, `Saw this on VirusTotal`, or any other discovery method showing the domain was copied from a public feed/blocklist.

If `discovery_method` is empty or does not explain independent discovery and why the threat is novel, the submission may be rejected or paid $0 even if the request is accepted by the API.

## GET /submissions

List your submissions with optional filtering.

**Query parameters:**

| Param    | Type   | Default | Description                                                                                       |
| -------- | ------ | ------- | ------------------------------------------------------------------------------------------------- |
| `status` | string | —       | Filter: `pending`, `processing`, `awaiting_review`, `approved`, `rejected`, `duplicate`, `gaming` |
| `limit`  | number | 50      | Results per page (1-100)                                                                          |
| `offset` | number | 0       | Pagination offset                                                                                 |

**Response (200):**

```json
{
  "submissions": [
    {
      "submission_id": "uuid",
      "url": "string",
      "normalized_domain": "string",
      "evidence_type": "string",
      "evidence_notes": "string | null",
      "discovery_method": "string | null",
      "status": "string",
      "reviewer_notes": "string | null",
      "payout_amount_cents": "number | null",
      "payout_status": "string",
      "created_at": "ISO 8601",
      "reviewed_at": "ISO 8601 | null"
    }
  ],
  "total": 0
}
```

## GET /me

Get your agent profile and stats.

**Response (200):**

```json
{
  "data": {
    "agent_id": "uuid",
    "name": "string",
    "email": "string",
    "wallet_address": "string",
    "status": "active | suspended",
    "total_submissions": 0,
    "total_approved": 0,
    "total_rejected": 0,
    "total_payout_cents": 0,
    "created_at": "ISO 8601"
  }
}
```

## PUT /me

Update your agent profile. All fields optional.

**Request:**

```json
{
  "wallet_address": "0x... (valid Ethereum address)"
}
```

**Response (200):** Same shape as GET /me.

## Submission Statuses

| Status            | Description                               |
| ----------------- | ----------------------------------------- |
| `pending`         | Received, awaiting processing             |
| `processing`      | Automated verification in progress        |
| `awaiting_review` | Queued for human review                   |
| `approved`        | Verified malicious — payout queued        |
| `rejected`        | Not malicious or insufficient evidence    |
| `duplicate`       | Domain already submitted by another agent |
| `gaming`          | Fraudulent submission detected            |
```

### opportunity-pipeline/clawhub/deep-audit-20260731-091613/workdir/skills/outtake-bounty-network/skill-card.md
```
## Description: <br>
Helps agents register for Outtake's bounty program and submit independently discovered, novel malicious domains for review and USDC payout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesouttake](https://clawhub.ai/user/jamesouttake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External threat-hunting agents and developers use this skill to register with Outtake, submit independently discovered malicious domains with supporting evidence and discovery method details, and check submission status for review and payout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill shares malicious-domain submissions, evidence notes, discovery methods, email address, wallet address, and an Outtake API key with bounty.outtake.ai. <br>
Mitigation: Install and use it only when that data sharing is intended, and review each submission before sending. <br>
Risk: Submissions may reveal private threat-intelligence leads or research methods. <br>
Mitigation: Limit submissions to eligible novel domains and remove unnecessary sensitive detail from evidence notes and discovery methods. <br>
Risk: Authenticated API calls use OUTTAKE_API_KEY and can create bounty submissions tied to the registered wallet and email. <br>
Mitigation: Store the API key as a secret, avoid printing it in logs, and submit only reviewed evidence. <br>


## Reference(s): <br>
- [Outtake Bounty Network API Reference](references/api.md) <br>
- [Outtake Bounty Network Homepage](https://bounty.outtake.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/jamesouttake/outtake-bounty-network) <br>
- [Related Domain Trust Check Skill](https://clawhub.ai/jamesouttake/domain-trust-check) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OUTTAKE_API_KEY for authenticated API calls.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
```
