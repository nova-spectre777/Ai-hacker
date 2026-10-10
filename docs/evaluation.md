# Evaluation Plan

## Never mix evaluation objectives

Language-model pretraining and vulnerability detection are different tasks. Results must be reported separately.

## Base language-model evaluation

Required measurements:
- training loss;
- validation loss;
- perplexity derived from validation loss;
- tokens processed and training throughput;
- runtime, GPU memory and training configuration;
- reload and inference smoke-test status.

A decrease in training loss is not enough: validation behavior matters, and duplicated or leaked evaluation data invalidates generalization claims.

## Vulnerability-analysis evaluation

The supervised security pipeline is not yet implemented. When it exists, evaluations should include:
- precision and recall;
- false-positive and false-negative rates;
- per-vulnerability-class results;
- per-language results;
- code-location and evidence accuracy;
- remediation correctness;
- inference latency and resource use;
- results on repositories excluded from training and tuning.

Use established tools and benchmark datasets as baselines, with each benchmark's license and intended purpose reviewed first. Keep a fixed held-out test set that is not used for model or threshold selection.

## Splitting data correctly

When the research question is performance on unseen repositories, split by repository/project, not by random snippets. Deduplicate and check near-duplicates before assigning splits. Keep dataset version and split manifests so evaluation can be reproduced.

## Review and evidence

Classify each output as a heuristic lead, model hypothesis, tool-confirmed observation, or human-verified issue. Only report a vulnerability as confirmed after appropriate verification. Any claim that a finding is novel requires additional checks against existing advisories and known fixes.

## Honest reporting template

Every evaluation report should state:
- model and source revision;
- whether weights were randomly initialized or adapted from a pretrained checkpoint;
- dataset names, versions, licenses, and splits;
- task and metric definitions;
- hardware/software environment;
- results and uncertainty;
- common failure modes;
- what has not been tested.

No fabricated benchmark results or performance claims are permitted.
