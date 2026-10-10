# FAQ

## Is this a trained cybersecurity AI already?

No. The current web dashboard includes a static scanner and a tiny model that learns a synthetic teaching task. The Transformer code is a training pipeline; no trained checkpoint is included.

## Does “from scratch” mean every component is written from first principles?

No. The model weights are randomly initialized, while PyTorch and Transformers provide implementation primitives such as tensors, attention blocks, backpropagation and optimizer integration. This is from-scratch model initialization, not a reinvention of the entire deep-learning stack.

## Does pretraining make the model a vulnerability detector?

No. Next-token prediction teaches statistical code/text patterns. Security detection requires its own labeled training objective, separate evaluation, and evidence-producing analysis tools.

## Can it find zero-days nobody has seen?

That is a long-term research ambition, not a guaranteed ability. Suspicious patterns must be validated. Novelty needs additional research and responsible disclosure.

## Why not train the largest preset immediately?

Large randomly initialized models can be expensive and need enough quality data and compute. First verify the tiny pipeline, checkpoints, evaluation and inference. Then use measured throughput and memory to decide whether scaling makes sense.

## Is the YAML file used automatically?

No. `configs/training-tiny.yaml` is a reference example. The current CLI is configured through command-line arguments.

## Why does the trainer require a GPU?

The current training entry point exits when CUDA is unavailable. Use a compatible GPU cloud runtime; CPU testing of static-analysis and unit-test code is separate.

## Which license applies?

A permissive open-source license has not been selected. See the repository's LICENSE notice before reusing or redistributing files.

## What is the first meaningful success milestone?

A reproducible tiny run that demonstrates finite loss, completed evaluation, a saved checkpoint, successful resume, and a reloadable final model on an identified GPU environment.
