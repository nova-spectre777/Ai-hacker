# Security and Responsible Use

## Intended use

CIRL is intended for defensive software engineering, code review, secure development, and security research on code and systems that the operator owns or is explicitly authorized to assess.

Permitted research includes analyzing intentionally vulnerable lab projects, studying public security fixes within their license terms, testing patches in isolated environments, and reviewing evidence-backed findings with maintainers.

## Finding lifecycle

1. Record the source location and suspicious data flow or operation.
2. State assumptions and required preconditions.
3. Separate heuristic evidence from verified behavior.
4. Test safely in a controlled environment, where testing is necessary and authorized.
5. Compare with known advisories when claiming novelty.
6. Have a human reviewer examine severity and remediation.
7. Follow responsible-disclosure practices if another party's software is affected.

A scanner match is not proof of exploitability. A clean result is not proof that software is secure.

## Dataset handling

- Verify the license and provenance for every source.
- Remove API keys, passwords, tokens, private keys and personal data before training.
- Never put private code, datasets, checkpoints or credentials in Git history.
- Keep source manifests and dataset hashes for reproducibility.
- Avoid training/evaluation leakage from mirrored repositories or near-identical snippets.
- Do not label uncertain examples as confirmed vulnerable or safe without review.

## Runtime safety

The current source scanner parses source but does not execute it or make network requests. Preserve that property unless future controlled execution is specifically designed, isolated, and documented.

Do not commit cloud credentials. Use provider secret stores or protected environment variables. Limit cloud instance permissions, use disposable workspaces where possible, and monitor storage and spend.

## Reporting a vulnerability in this project

Do not post secrets or exploitable details for a private deployment in a public issue. Use GitHub private vulnerability reporting if enabled for this repository; otherwise contact the repository maintainer privately and include a minimal reproduction, affected commit, impact, and proposed mitigation.

## Known limitations

- The current scanner relies on a small set of regular expressions.
- Its findings can be false positives and false negatives.
- The toy neural network has no cybersecurity training.
- The Transformer training CLI is a base language-model pipeline, not a validated detector.
- Unknown-vulnerability discovery is an ambition, not a guaranteed capability.
