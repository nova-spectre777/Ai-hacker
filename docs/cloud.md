# Cloud GPU Training

## Status

The repository includes a GPU-only Transformer training command, checkpoint/resume code and a tiny-model smoke-test path. Cloud jobs have not been verified on every provider. There is no built-in scheduler, autoscaler, cloud credential manager, or automatic budget enforcement yet.

## Choose a runtime

Use a cloud platform that provides a recent NVIDIA GPU, persistent disk, terminal access and enough VRAM for the selected configuration. The exact cost depends on provider, region, GPU, storage, machine uptime, and current pricing; verify current pricing before launch.

Install a PyTorch build compatible with the runtime's CUDA driver and Python version. Then install this project:

```bash
python -m pip install --upgrade pip
pip install -e ".[training,dev]"
python scripts/check_environment.py
```

If you use a clean cloud notebook or virtual machine, clone the repository and open a terminal at the repository root first.

## Data and artifacts

- Place authorized corpora on persistent storage.
- Keep datasets and model artifacts outside Git.
- Use separate train and validation inputs or manifests for larger experiments; the current CLI creates a simple row-level split.
- Save artifacts and checkpoints to a persistent volume.
- Keep access tokens in the provider's secret store, not in command history, source files, or logs.
- Monitor disk usage, runtime, and accumulated spend.

## First-run checklist

1. Verify the correct GPU and CUDA-compatible PyTorch installation.
2. Confirm the corpus has enough text to form both training and validation token blocks at the selected context length.
3. Inspect the corpus license and remove secrets and private data.
4. Train the tokenizer.
5. Run the tiny model with a small corpus and low step budget if appropriate.
6. Confirm finite training and validation loss.
7. Confirm checkpoints are created and resume works after interruption.
8. Reload the exported model and run an inference smoke test.
9. Estimate runtime and cost before increasing sequence length or model size.

## Scaling up

Scale one dimension at a time: corpus size, sequence length, batch size, or model preset. Record tokens/second and peak memory to inform the next decision. Multi-GPU launch examples should only be used after the single-GPU path has been verified and enough compatible GPUs are available.

A larger model is not automatically more capable. Training from random initialization is data- and compute-intensive, and a small poorly curated corpus can lead to expensive overfitting.

## Operational security

Do not run unknown training scripts from a downloaded corpus. Keep credentials out of the source tree. Use least-privilege cloud accounts, shut down idle resources, and verify whether storage continues to incur charges after an instance stops.
