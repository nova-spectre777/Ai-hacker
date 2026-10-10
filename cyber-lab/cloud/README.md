# Cloud Transformer Training

This is the cloud-training path for Ai-hacker. It creates a **decoder-only Transformer with random weights**, trains a tokenizer from your corpus, and trains the model on a GPU. It does not use or download pretrained model weights.

> Important: increasing model size does not automatically make a strong cybersecurity model. Data quality, compute, evaluation, and safety review matter. This is a language-model pretraining foundation, not a validated vulnerability detector or a zero-day discovery guarantee.

## 1. Pick a GPU instance

Use a cloud GPU runtime with a recent NVIDIA GPU, enough disk for the corpus and checkpoints, and Python 3.10 or 3.11. Install CUDA-compatible PyTorch as recommended by https://pytorch.org/get-started/locally/ . The exact GPU memory requirement depends on model size, context length, batch size, optimizer, and precision.

Suggested progression:
- `tiny`: pipeline smoke test; use a small sample first.
- `small`: initial experiments.
- `medium`: needs substantially more VRAM and storage.
- `large` / `xl`: expensive experiments; do not launch without checking the provider's GPU memory and budget.

Start with `small` or `tiny`, confirm checkpoints and evaluation work, then scale up. Training from random initialization requires far more compute and data than fine-tuning an existing model.

## 2. Prepare a licensed corpus

Create a UTF-8 text file such as `data/code_corpus.txt`. Put code and documentation you have permission to use in it. Use a clean train/validation split; avoid leaking duplicated repositories or near-identical examples across the split. Remove credentials, API keys, personal data, malware payloads, and other secrets before training.

For security specialization, build a separate, carefully labeled dataset with fields such as:
```json
{"code":"def example(x):\n    return x","label":"safe","language":"python","cwe":"CWE-000","source":"owned-or-permitted"}
{"code":"...","label":"vulnerable","language":"python","cwe":"CWE-XXX","source":"owned-or-permitted"}
```
These JSONL records are an example schema, not a ready-made training set. The current `train_lm.py` pretrains on text; it does **not** train a vulnerability classifier from those labels. A separate supervised fine-tuning/classification stage and held-out benchmark are needed before making detector claims.

## 3. Install dependencies

From this folder on the GPU machine:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate with `.venv\\Scripts\\activate`; cloud GPU Linux is generally simpler.

## 4. Train a tokenizer from scratch

```bash
python train_tokenizer.py --corpus /data/code_corpus.txt --out artifacts/tokenizer --vocab-size 32000
```

The tokenizer training pass reads the corpus. Make sure the machine has enough RAM and disk for the tokenizer pass and dataset cache.

## 5. Start a small training run first

```bash
python train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-small --size tiny --epochs 1 --batch-size 2 --grad-accum 8 --save-steps 100
```

Check that the loss is finite, evaluation completes, and a `checkpoint-*` folder is created. Then try the small preset:

```bash
python train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-small --size small --epochs 1 --batch-size 2 --grad-accum 16 --save-steps 500
```

Resume after interruption:

```bash
python train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-small --size small --epochs 1 --batch-size 2 --grad-accum 16 --resume
```

For multi-GPU training, launch with PyTorch distributed, for example:
```bash
torchrun --nproc_per_node=4 train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-multi --size medium --epochs 1 --batch-size 1 --grad-accum 16
```
Replace `4` with the number of GPUs actually allocated. Do not assume the example fits every GPU.

## 6. How to know it is learning

- Training loss should trend down; validation loss should not steadily rise while training loss falls.
- Perplexity is reported as a language-model metric, **not** vulnerability-detection accuracy.
- Preserve held-out projects and test them after every change.
- A useful security evaluation needs precision, recall, false-positive rate, false negatives, performance by vulnerability class, and manual verification of findings.
- A model that completes pretraining is not automatically a useful or safe security tool.

## Limits and authorized use

Use only licensed/publicly permitted datasets and code you own or have explicit authorization to assess. This pipeline trains a base code language model; it does not automatically discover unknown vulnerabilities. Novel findings require evidence, reproducibility, and independent validation.
