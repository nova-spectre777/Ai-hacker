# Migration Plan

## Goal

Move from the original `cyber-lab/` prototype to a conventional `src/code_integrity_lab/` Python package without silently breaking the local dashboard or cloud entry points.

## Audit findings

- The original root contained a README, a GitHub Actions workflow, and `cyber-lab/`.
- The dashboard imported scanner and toy-network functions from sibling files.
- The cloud tokenizer and Transformer trainer lived in `cyber-lab/cloud/`.
- The NumPy network was a synthetic-data teaching demo, not a security model.
- The Transformer training code created a model from configuration, but cloud training had not been verified.
- The former `.github/workflows/import-hackerai.yml` cloned an unrelated external repository, deleted the checked-out working tree, copied external files over it and pushed to `main` on push events. This was a critical repository-integrity risk. It is removed on this branch and replaced by read-only CI.

## Phase 1 changes

- Add `pyproject.toml` and optional dependency groups.
- Move scanner implementation to `src/code_integrity_lab/security/scanner.py`.
- Move the toy network to `src/code_integrity_lab/model/toy_network.py`.
- Move tokenizer and Transformer entry-point implementations into the package.
- Retain old file paths as compatibility shims.
- Add unit tests, environment diagnostics, CI and documentation.
- Move the Flask dashboard and active template into `src/code_integrity_lab/web/`.
- Add binary-classification metric utilities.
- Rebrand dashboard strings to Code Integrity Research Lab.

## Compatibility requirements

- `cyber-lab/app.py` should continue to import scanner and toy-network names through the legacy shims.
- `cyber-lab/cloud/train_tokenizer.py` and `cyber-lab/cloud/train_lm.py` should remain callable as wrappers.
- Root README should document both maintained package and legacy dashboard.

## Verification still required

The source and tests are committed on the rebuild branch, but this document does not claim they have already passed CI. Before merging, inspect the CI workflow result and manually validate the local dashboard and a tiny GPU training run. If compatibility tests fail, fix regressions before further moving files.

## Deferred migrations

The packaged Flask application and active template now live in `src/code_integrity_lab/web/`; `cyber-lab/app.py` remains a compatibility entry point. The former template remains as a legacy copy. Cloud orchestration, supervised vulnerability training, AST/data-flow analysis, and dashboard-triggered cloud training remain planned, not implemented.
