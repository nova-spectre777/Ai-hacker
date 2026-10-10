# Code Integrity Research Lab

**Tagline:** A reproducible code-security AI research platform for authorized defensive analysis.

*Historical/internal codename: AI Hacker.*

The Code Integrity Research Lab (CIRL) is an early-stage research codebase exploring genuine code-language-model training and evidence-backed defensive software analysis. The project prioritizes reproducibility, transparent evaluation, and clear separation between implemented features and research goals.

> **Current status: pre-alpha.** The repository contains a small local static-analysis dashboard, a tiny NumPy backpropagation demonstration, and an initial randomly initialized Transformer training pipeline. No trained language-model checkpoint or validated vulnerability-detection model is included. The cloud training code has not been certified across all GPU environments.

## Start here

- [Architecture](docs/architecture.md)
- [Training from scratch](docs/training.md)
- [Cloud setup](docs/cloud.md)
- [Security boundaries](docs/security.md)
- [Evaluation methodology](docs/evaluation.md)
- [Roadmap](docs/roadmap.md)
- [FAQ](docs/faq.md)
- [Base-model card](docs/model_cards/base-code-language-model.md)
- [Migration plan](docs/migration-plan.md)

## Repository map

```text
src/code_integrity_lab/       Maintained Python package
  security/scanner.py         Conservative Python source pattern checks
  model/toy_network.py        Tiny synthetic-data backpropagation demo
  web/app.py + templates/     Local dashboard and JSON API
  evaluation/metrics.py       Binary-classification metric helpers
  tokenizer/                  Tokenizer training
  training/                   Randomly initialized Transformer training
  cloud/ utils/               Extension points for cloud and shared tooling
cyber-lab/                    Legacy dashboard and compatibility entry points
configs/                      Reference experiment configuration
data/                         Dataset handling instructions; datasets are not included
docs/                         Architecture, training, security, evaluation and roadmap
scripts/                      Environment diagnostics
tests/                        Automated regression tests
notebooks/                    Research notebook conventions
docker/                       Container planning notes; no image is certified yet
```

The earlier `cyber-lab/` entry points remain as compatibility shims while the migration proceeds. Refer to [the migration plan](docs/migration-plan.md) for what has and has not moved.

## Local scanner dashboard

The dashboard runs on localhost and checks pasted Python source for a small set of suspicious patterns. It does not execute pasted code or contact remote targets. Findings are static-analysis leads, not proof of exploitability.

On Windows, from `cyber-lab/`:

1. Install Python 3.11 or 3.12.
2. Run `run.bat`.
3. Open http://127.0.0.1:5000.

Or follow [the local dashboard guide](cyber-lab/README.md).

## Cloud model training

The training entry points create a decoder-only Transformer with **randomly initialized weights**; they do not load a pretrained checkpoint.

Install the package and dashboard/test dependencies:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -e ".[dev,web]"
```

For training, install a PyTorch build compatible with the GPU runtime first, then:

```bash
pip install -e ".[training]"
python scripts/check_environment.py
cil-train-tokenizer --corpus /data/code_corpus.txt --out artifacts/tokenizer --vocab-size 32000
cil-train-lm --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-tiny --size tiny --max-steps 20 --batch-size 2 --grad-accum 8 --save-steps 10 --logging-steps 1 --seed 42
```

Read [docs/cloud.md](docs/cloud.md) before starting a paid instance. Begin with a tiny test, confirm that evaluation and checkpoint recovery work, and estimate resources before scaling up.

## Validate changes

```bash
pip install -e ".[dev,web]"
python -m pytest -q
python -m compileall -q src scripts cyber-lab
```

The CI workflow is configured to run unit tests and Python compilation across Python 3.10–3.12. Check the latest Actions result before merging; a passing CI run is not evidence of model quality, and CI does not run GPU training.

## What this project does not claim

- It does not include a trained frontier-scale language model.
- The toy NumPy network is not a vulnerability classifier.
- Language-model loss or perplexity is not vulnerability-detection accuracy.
- The static scanner is not a replacement for security review or comprehensive analysis.
- No capability to discover zero-day or previously unknown vulnerabilities is guaranteed.

## Responsible use

Use datasets according to their licenses and assess only software you own or are explicitly authorized to test. Validate findings safely, preserve evidence, and follow responsible-disclosure practices.

## License status

A permissive open-source license has not yet been selected. See [LICENSE](LICENSE) before reusing or redistributing the code.
