# Security Policy

## Scope

This project is pre-alpha. The local scanner and training scripts are research tools and are not a security guarantee.

## Supported versions

Only the current default branch and the active rebuild branch receive ongoing development. No released version has been declared stable.

## Reporting a vulnerability

Do not publish secrets, access tokens, private datasets, or a weaponizable exploit against a private deployment in a public issue. If GitHub private vulnerability reporting is enabled, use it. Otherwise, contact the repository maintainer privately through GitHub and provide:
- affected commit or file;
- minimal reproduction;
- expected and actual behavior;
- security impact and assumptions;
- a proposed mitigation, if known.

Please allow time for investigation before public disclosure. Reports will be assessed based on reproducibility and impact.

## Operational guidance

Do not commit credentials or private corpora. Use authorized test environments only. Treat scanner results as leads requiring human review, and do not expose private training data or model artifacts through the web dashboard.
