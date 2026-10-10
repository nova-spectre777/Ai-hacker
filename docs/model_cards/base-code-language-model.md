# Model Card: Base Code Language Model Recipe

## Identity

- Project: Code Integrity Research Lab
- Historical/internal codename: AI Hacker
- Artifact: training recipe, not a distributed trained model
- Model family: GPT-2-style decoder-only Transformer configuration
- Initialization: random
- Status: pre-alpha; GPU execution and resulting artifacts have not yet been verified in this repository

## Intended purpose

The recipe is intended for controlled experiments in code/text next-token prediction and as a foundation for later security-task research.

## Not intended for

- Automated decisions that code is safe or vulnerable.
- Production security guarantees.
- Autonomous exploitation of systems.
- Claims of zero-day discovery or frontier-level capability.
- High-stakes decisions without independent human review.

## Training method

The tokenizer is trained from a provided text corpus. Transformer parameters are initialized from configuration rather than loaded from a pretrained checkpoint. The model is trained with causal next-token prediction on line-oriented text data packed into fixed-length token blocks.

## Data

The repository does not ship a training corpus. The operator must provide data with appropriate permissions and record provenance and license information. Secret filtering, high-quality deduplication, and repository-level holdout splitting remain important requirements for larger experiments.

## Evaluation

No model-quality metrics are provided because no cloud training run has been verified. When trained, language-model loss and perplexity should be reported separately from any security evaluation.

## Limitations

- Random initialization requires substantial data and compute for useful language-model capability.
- The current corpus split is a simple row-level split and is not a complete solution for repository-level leakage prevention.
- The recipe has not been certified on a matrix of cloud GPUs or Transformers versions.
- This artifact is not a vulnerability detector and provides no guarantee of discovering unknown flaws.

## Updates

After a verified run, update this card with the exact code revision, data manifest, tokenizer, training configuration, hardware, completed metrics, known failures and artifact hashes.
