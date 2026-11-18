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
