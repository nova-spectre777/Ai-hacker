# Cloud Transformer Training

This folder retains the original command paths as compatibility wrappers. The maintained code is in `../../src/code_integrity_lab/`.

The tokenizer trainer learns a byte-level BPE vocabulary from a user-provided corpus. The language-model trainer initializes a decoder-only Transformer with **random weights** and trains next-token prediction on a GPU. It does not download pretrained weights.

> This is a base language-model training pipeline, not a validated vulnerability detector. No zero-day discovery is guaranteed. GPU execution, checkpoint recovery, and final inference must be verified in the chosen cloud environment before reporting results.

## Before launching a cloud instance

Read the root [cloud guide](../../docs/cloud.md) and [training guide](../../docs/training.md). Check current provider pricing, persistent storage, GPU memory, compatible CUDA/PyTorch versions, dataset permissions, and spend limits.

## Install requirements

From this directory on the GPU machine:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`, but a Linux GPU runtime is generally simpler for cloud training.

## Prepare the corpus

Create a UTF-8 text file containing code and documentation you are permitted to use, e.g. `/data/code_corpus.txt`. Remove credentials and private data. The current script makes a simple row-level validation split; it is not a substitute for repository-level holdout manifests or thorough deduplication.

## Train tokenizer from scratch

```bash
python train_tokenizer.py --corpus /data/code_corpus.txt --out artifacts/tokenizer --vocab-size 32000
```

## Run the tiny smoke test

```bash
python train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-tiny --size tiny --epochs 1 --batch-size 2 --grad-accum 8 --save-steps 100 --seed 42
```

The run should produce finite training/validation losses, checkpoint folders, and a final artifact directory. These are checks to perform, not results claimed by this documentation.

Resume from the latest checkpoint:

```bash
python train_lm.py --corpus /data/code_corpus.txt --tokenizer artifacts/tokenizer --out artifacts/run-tiny --size tiny --epochs 1 --batch-size 2 --grad-accum 8 --save-steps 100 --resume
```

The command requires compatible GPU memory. Start with the tiny preset and only scale after measuring throughput, memory and costs. Language-model perplexity is not vulnerability-detection accuracy.

## Security data specialization

The current trainer only performs next-token language-model pretraining. The separate supervised vulnerability-training pipeline and held-out security benchmark are not implemented yet. See [evaluation requirements](../../docs/evaluation.md).

Use permitted datasets and test only software you own or are authorized to assess.
