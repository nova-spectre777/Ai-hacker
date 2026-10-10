# AI Hacker

Cybersecurity research and AI experiments.

## Projects

### Cyber Lab (local MVP)
The first runnable project lives in [`cyber-lab/`](./cyber-lab/). It contains a local browser UI, static Python source checks, a tiny NumPy backpropagation demo, and a toy genetic algorithm.

### Cloud Transformer training
The new [`cyber-lab/cloud/`](./cyber-lab/cloud/) path adds:
- tokenizer training from a user-provided code corpus;
- a decoder-only Transformer initialized with **random weights** (not a pretrained model);
- configurable tiny/small/medium/large/XL model presets;
- GPU training with mixed precision, gradient checkpointing, evaluation, checkpoints, and resume support;
- a cloud setup guide and commands.

Start with the [cloud training guide](./cyber-lab/cloud/README.md). It requires a CUDA GPU runtime and a licensed corpus; do a tiny smoke test before scaling.

**Important:** This is training infrastructure, not a frontier model or a proven vulnerability detector. Language-model loss/perplexity do not measure vulnerability detection. Any security detector needs a separate supervised training stage, held-out benchmarks, false-positive/false-negative measurement, and human validation. No zero-day discovery is guaranteed. Use only code and systems you own or are authorized to assess.
