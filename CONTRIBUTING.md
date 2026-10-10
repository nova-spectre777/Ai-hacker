# Contributing

Thanks for helping improve Code Integrity Research Lab. This is a pre-alpha research project; reproducibility and honest status reporting matter more than broad feature claims.

## Before changing code

1. Read [the architecture](docs/architecture.md), [security policy](docs/security.md), and [migration plan](docs/migration-plan.md).
2. Keep changes focused and preserve legacy entry points unless a migration explicitly documents their replacement.
3. Do not include credentials, private code, datasets, checkpoints or experiment artifacts in commits.
4. Do not report benchmark results unless the run completed and the metric can be reproduced.

## Development setup

Python 3.10–3.12 is the intended range.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev,web]"
python -m pytest -q
python -m compileall -q src scripts cyber-lab
```

For cloud language-model training, install CUDA-compatible PyTorch and then `pip install -e ".[training]"`.

## Testing expectations

- Add tests for bug fixes and new behavior.
- Test static analysis without executing submitted source.
- Keep language-model metrics separate from security metrics.
- For data and model changes, document provenance, license, split strategy, seed and evaluation method.
- State clearly if a GPU run or provider integration has not been executed.

## Pull requests

A pull request should explain the problem, the change, compatibility impact, commands run, results, and remaining limitations. Keep the PR reviewable; prefer small changes over an unrelated bulk rewrite.
