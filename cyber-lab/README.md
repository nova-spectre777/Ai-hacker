# Scratch Neural AI — Cyber Lab (MVP)

A local-first educational cybersecurity code-review app with:
- browser UI and visible analysis pipeline;
- static Python source checks with rule IDs, severity estimates, line numbers, snippets, and remediation guidance;
- a tiny NumPy neural network trained by real backpropagation;
- a separate genetic-algorithm toy experiment.

## Run on Windows

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Open Command Prompt in this folder.
3. Run these commands:

```bat
py -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.
5. Stop the server with Ctrl+C in Command Prompt.

## What it actually does

The scanner checks pasted Python code for selected patterns such as eval/exec, subprocess shell=True, likely hard-coded secrets, unsafe YAML loading, disabled TLS verification, weak hashes, pickle deserialization, debug=True, and possible SQL string formatting. Results are **static-analysis leads**, not proof of a vulnerability. It does not execute pasted code or connect to remote targets.

The NumPy network uses forward passes, loss calculation, gradients, and weight updates. It trains on a tiny synthetic toy dataset solely to demonstrate backpropagation. Its prediction is **not** a vulnerability probability. The genetic algorithm optimizes a toy threshold, not security findings.

## Limits and responsible use

This is an MVP, not a frontier model or a zero-day discovery engine. It cannot promise never-before-seen findings; that requires deeper analysis, careful validation, and independent review. Use it only on code you own or have explicit permission to assess. Do not treat a clean scan as proof that software is secure.

## Next development steps

- Add tests and a richer AST-based rule engine.
- Add SARIF/JSON report export and confidence/false-positive workflow.
- Add dependency audit and secret scanning.
- Add repository ingestion limited to explicitly authorized projects.
- Train/evaluate a model on licensed, curated vulnerability examples with held-out data before making claims about detection performance.
