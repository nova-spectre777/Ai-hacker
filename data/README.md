# Local Data

Do not commit raw or processed datasets, source archives, credentials, or model weights to this repository.

Recommended local-only layout:

- `data/raw/`: original datasets with source, license, and provenance notes.
- `data/processed/`: normalized, deduplicated and filtered corpus files.
- `data/splits/`: reproducible train/validation/test manifests.
- `artifacts/`: tokenizers, checkpoints, final models, and evaluation outputs.

Before training, verify permissions, remove secrets and personal data, and record preprocessing steps. Prefer project/repository-level train/test splits when measuring generalization to unseen codebases.
