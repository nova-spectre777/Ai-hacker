# Scratch Neural AI — Cyber Lab (MVP)

A local-first educational cybersecurity code-review app with a browser UI, static Python checks, a tiny NumPy backpropagation demo, and a toy genetic-algorithm experiment.

## Run the local MVP on Windows

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Open Command Prompt in this folder.
3. Run:

```bat
py -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:5000.

## What it actually does

The scanner checks pasted Python code for selected risky patterns and returns static-analysis leads with evidence. It does not execute pasted code or connect to remote targets. The NumPy network learns a tiny synthetic teaching task; its output is **not** a vulnerability probability. The genetic algorithm optimizes a toy threshold, not security findings.

## Cloud training path

For a configurable Transformer trained from random initialization on a GPU, see [`cloud/README.md`](./cloud/README.md). That path trains a tokenizer and decoder-only language model, with checkpoints and evaluation. It is separate from this small web demo.

**Important:** The cloud language model is not automatically a vulnerability detector. Security detection requires labeled, licensed examples, a separate supervised training/evaluation stage, held-out projects, false-positive/false-negative measurement, and independent review. No model can guarantee discovery of unknown vulnerabilities.

Use only datasets and code you have permission to use, and assess only systems you own or are explicitly authorized to test.
