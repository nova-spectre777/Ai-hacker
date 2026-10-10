# Changelog

All notable changes to this pre-alpha project are documented here. This is an engineering log, not a release guarantee.

## Unreleased — Professional rebuild branch

### Added
- Professional working name: Code Integrity Research Lab (CIRL); historical codename retained as AI Hacker.
- `pyproject.toml` with optional web, training, and development dependency groups.
- Maintained source package under `src/code_integrity_lab/`.
- Tests for the scanner and toy-network API contract.
- Environment diagnostic script and tiny-training reference configuration.
- Architecture, training, cloud, security, evaluation, roadmap, FAQ, model-card, and migration documentation.
- Read-only CI workflow for unit tests and Python syntax compilation.

### Changed
- Legacy scanner, toy-network, tokenizer, and language-model entry paths now forward to the package implementation.
- Dashboard branding updated to Code Integrity Research Lab.

### Security
- Removed the prior import workflow that cloned an unrelated external repository, removed tracked working-tree contents, and pushed replacement files to the default branch.

### Not yet verified
- GPU training, checkpoint recovery, final-model inference, and provider-specific cloud deployment remain unverified.
- CI results should be checked before merging this branch.
