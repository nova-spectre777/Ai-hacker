# Training Guide

## Two different learning objectives

### 1. Base language-model pretraining

The cloud trainer initializes a GPT-2-style decoder-only Transformer from a new configuration, so model parameters begin randomly initialized. The objective is causal next-token prediction: use earlier tokens to predict the next token.

This is actual gradient-based training when run on a suitable GPU. It is not, by itself, a vulnerability detector.

### 2. Supervised security specialization

A separate stage is required for vulnerability analysis. That stage is planned and is **not implemented yet**. It will need carefully labeled examples, repository-level data splits, a suitable classification or structured-output objective, and independent evaluation.

## Requirements

- A UTF-8 text corpus that you have permission to use.
- A GPU runtime with a compatible CUDA/PyTorch installation.
- Sufficient persistent disk for source corpus, tokenized cache, and checkpoints.
- A tokenizer produced by this repository's tokenizer trainer.
- Enough corpus lines and tokens to create both training and validation blocks.

Install CUDA-compatible PyTorch using the guidance for your chosen runtime, then install the training extra:

```bash
pip install -e ".[training]"
python scripts/check_environment.py
```

Do not assume that a model preset fits a particular GPU. VRAM depends on hidden size, layer count, context length, batch size, optimizer state, precision and runtime overhead.

## Train the tokenizer

```bash
cil-train-tokenizer --corpus /data/code_corpus.txt --out artifacts/tokenizer --vocab-size 32000
```

The tokenizer should be trained using the intended permitted corpus. Keep a record of corpus hashes, source manifests, vocabulary size and preprocessing settings.

## Run a tiny model first

```bash
cil-train-lm --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-tiny --size tiny --max-steps 20 --batch-size 2 --grad-accum 8 --save-steps 10 --logging-steps 1 --seed 42
```

The trainer reports the preset, parameter count, GPU names and seed. It saves checkpoints and a final artifact directory when training completes. Inspect the run for finite loss values, completed validation, checkpoint files, and a reloadable final model.

If the context length does not fit the corpus, use a larger corpus or a smaller `--block-size` (minimum 16). The simple line-based validation split is a smoke-test mechanism, not a scientifically robust security benchmark.

## Resume training

Use the same corpus, tokenizer, configuration, output directory and seed:

```bash
cil-train-lm --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-tiny --size tiny --max-steps 20 --batch-size 2 --grad-accum 8 --save-steps 10 --logging-steps 1 --resume --seed 42
```

Changing model architecture or tokenizer while resuming from an old checkpoint is not a valid continuation; start a new output directory for a new experiment.

## Presets

| Preset | Layers | Heads | Width | Default context |
|---|---:|---:|---:|---:|
| tiny | 4 | 4 | 256 | 512 |
| small | 8 | 8 | 512 | 1,024 |
| medium | 12 | 12 | 768 | 1,024 |
| large | 24 | 16 | 1,024 | 2,048 |
| xl | 32 | 20 | 1,280 | 2,048 |

These are configuration presets, not tested hardware guarantees. Start with tiny. Do not rent or launch expensive hardware until you have measured a small run and set a cost limit.

## What to record

For every run, preserve:
- repository commit or source revision;
- dataset provenance, license, hash, and split manifest;
- tokenizer version and vocabulary size;
- model configuration and parameter count;
- software versions, GPU model, seed, and optimizer settings;
- wall-clock duration, tokens/second, peak memory, training/validation loss;
- checkpoint paths and whether resume and reload succeeded.

## Interpretation

A lower training loss alone can reflect memorization. Validation loss and perplexity measure language modeling, not vulnerability detection. Do not publish detection claims until a separate supervised pipeline is evaluated using precision, recall, false positives, false negatives and held-out repositories.
