# Maven dependency version rescue

This demo reproduces a real Maven failure caused by code using `StringUtils.isAllBlank` while the POM pins Apache Commons Lang 3.1, which does not provide that API.

The repaired project upgrades the dependency to 3.12.0. Both projects contain the same Java source, so the POM change is the only functional repair.

Run:

```bash
bash verify.sh
```

Expected result:

1. `broken/pom.xml` fails compilation.
2. `fixed/pom.xml` packages successfully.
3. The script prints `PASS: broken build rejected; repaired build verified`.

This demo proves the delivery format used by the fixed-price Maven Build Rescue package: reproduce, patch, and verify.
