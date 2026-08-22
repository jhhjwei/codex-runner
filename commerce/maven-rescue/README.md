# Maven Build Rescue

One fixed-scope service: repair one reproducible Maven dependency or build failure.

## Package

- Price: USD 65 fixed
- Delivery target: 24 hours after a reproducible input is accepted
- Scope: one Maven build blocker in one repository
- Revision: one revision within 48 hours, limited to the agreed blocker

## Accepted inputs

- A public repository or sanitized ZIP
- The exact failing command
- Complete error log
- Java and Maven versions

## Deliverables

- A patch or corrected `pom.xml`
- Dependency tree before and after the change
- The verification command and its exit status
- A short root-cause report

## Exclusions

No production login, deployment, database repair, new feature work, account sharing, credential handling, or continuing maintenance. The free preflight rejects work that cannot be reproduced locally or does not fit the fixed scope.

## Acceptance rule

The agreed Maven command must return exit code 0 in the delivery environment. Search results, explanations, and untested edits do not count as delivery.

## Public proof

[`demos/maven-build-rescue`](../../demos/maven-build-rescue) contains a deliberately broken Maven project, a corrected version, and a script that proves the broken build fails while the repaired build passes.
