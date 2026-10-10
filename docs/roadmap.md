# Roadmap

Statuses reflect the code and documentation in this repository at the time of writing; they are not a promise of completion.

## Phase 0 — Baseline and safety

- [x] Audit repository file layout and major entry points.
- [x] Identify an unsafe auto-import workflow that overwrote repository contents.
- [x] Replace it on the rebuild branch with read-only CI validation.
- [x] Add professional working name and project documentation.
- [ ] Confirm CI is green after the branch changes.
- [ ] Validate the app and training pipeline in target environments.

## Phase 1 — Reproducible package

- [x] Add packaging metadata and optional dependency groups.
- [x] Move scanner implementation into the maintained package; retain a legacy shim.
- [x] Move the toy backpropagation demo into the package; retain a compatibility shim.
- [x] Move tokenizer and Transformer entry points into the package; keep old paths callable.
- [x] Add unit tests and environment diagnostics.
- [x] Move the dashboard and active template into the package, retaining the legacy runner.
- [x] Add binary-classification metric utilities.
- [x] Move the dashboard and active template into the package, retaining the legacy runner.
- [x] Add binary-classification metric utilities.
- [ ] Add broader integration tests.
- [ ] Validate editable installation on supported Python versions.

## Phase 2 — Reliable from-scratch pretraining

- [x] Implement tokenizer and random-initialized Transformer CLI entry points.
- [x] Add seed, dataset-size checks, and API compatibility handling.
- [ ] Run a real tiny model job on a GPU.
- [ ] Verify resume, final-model reload, and inference.
- [ ] Record measured throughput, memory use and costs on selected hardware.
- [ ] Add robust corpus manifests, deduplication and project-level splits.

## Phase 3 — Security dataset and supervised learning

- [ ] Build permitted, provenance-aware data ingestion.
- [ ] Add schema validation, secret filtering and deduplication.
- [ ] Add labeled vulnerability classification or structured prediction.
- [ ] Add vulnerable/fixed pairs and explanation/remediation objectives.
- [ ] Add project-level train/validation/test manifests.
- [ ] Add security benchmark adapters and false-positive analysis.

## Phase 4 — Evidence-backed analysis

- [ ] Add AST-aware findings and richer data-flow evidence.
- [ ] Integrate established local security tools where appropriate.
- [ ] Add JSON/SARIF report export.
- [ ] Add issue triage, manual verification and remediation review.
- [ ] Add tests on intentionally vulnerable lab projects.

## Phase 5 — Cloud operations and UI

- [ ] Add persistent job orchestration and explicit cancellation.
- [ ] Add experiment tracking and artifact registry.
- [ ] Add cloud budget safeguards and resource estimates.
- [ ] Add dashboard views backed only by real training/evaluation state.
- [ ] Build and validate a provider-compatible GPU container.

## Long-term research ambition

Improve the ability to detect subtle and potentially previously unknown weaknesses in authorized codebases. This goal is not guaranteed; each claimed discovery must be reproducible and independently reviewed.
