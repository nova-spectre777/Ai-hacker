# Architecture

## Product identity

**Code Integrity Research Lab (CIRL)**  
Tagline: *A reproducible code-security AI research platform for authorized defensive analysis.*  
Historical/internal codename: AI Hacker.

This is a pre-alpha research project. The design separates token prediction, security detection, static analysis, and claims about confirmed vulnerabilities.

## Current component map

| Component | Location | Status |
|---|---|---|
| Python pattern scanner | `src/code_integrity_lab/security/scanner.py` | Implemented; tests added; CI result must be checked |
| Legacy dashboard scanner import | `cyber-lab/scanner.py` | Compatibility shim |
| Tiny synthetic-data neural network | `src/code_integrity_lab/model/toy_network.py` | Implemented teaching demo; not a detector |
| Legacy dashboard model import | `cyber-lab/neural_net.py` | Compatibility shim |
| Tokenizer training | `src/code_integrity_lab/tokenizer/train_tokenizer.py` | CLI implemented; cloud execution not verified |
| From-scratch Transformer training | `src/code_integrity_lab/training/train_lm.py` | CLI implemented; GPU training not verified |
| Local Flask dashboard | `src/code_integrity_lab/web/` | Packaged UI/API; it does not start cloud jobs |
| Binary-classification metrics | `src/code_integrity_lab/evaluation/metrics.py` | Utility implemented; not yet used by a detector |
| Legacy training paths | `cyber-lab/cloud/` | Compatibility entry points |
| Training configuration example | `configs/training-tiny.yaml` | Reference only; not loaded automatically |
| Cloud orchestration and job queue | Planned | Not implemented |
| Labeled vulnerability training and benchmark | Planned | Not implemented |
| AST/data-flow engine and SARIF export | Planned | Not implemented |

## Intended data and model flow

1. **Data intake:** accept permitted corpora; record source, license, provenance, and preprocessing metadata.
2. **Quality controls:** remove secrets and private data, normalize, deduplicate, and separate projects across evaluation splits.
3. **Tokenizer:** learn a byte-level BPE vocabulary from the corpus.
4. **Base model:** initialize a decoder-only Transformer randomly and train next-token prediction.
5. **Checkpointing:** save model, tokenizer, configuration, random seed, and training/evaluation metadata.
6. **Security specialization:** separately train or adapt security-task components on curated labels and vulnerable/fixed examples.
7. **Evidence production:** combine model hypotheses with deterministic analysis tools and controlled tests.
8. **Evaluation:** measure language modeling and vulnerability analysis with different metrics.
9. **Human review:** verify findings before considering them confirmed or disclosing them.

## Design principles

- Prefer reproducibility over opaque convenience.
- Keep model training separate from inference and static-analysis rules.
- Keep the training corpus outside version control unless a dataset is explicitly permitted and intentionally included.
- Never represent heuristic findings as confirmed vulnerabilities.
- Keep old dashboard entry points while migrating so the existing demo remains available.
- Log actual metrics and errors; do not synthesize progress indicators or benchmark scores.

The Flask application and active template now live in the package; `cyber-lab/app.py` remains a compatibility entry point. Cloud orchestration, supervised vulnerability training, AST/data-flow analysis, and dashboard-triggered cloud training remain planned, not implemented.
