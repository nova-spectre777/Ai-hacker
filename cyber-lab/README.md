# Code Integrity Research Lab — Local Cyber Lab

This folder contains the original local dashboard kept for compatibility while the Python package migration proceeds.

## Run the local dashboard on Windows

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Open this folder in File Explorer.
3. Double-click `run.bat`.
4. Open http://127.0.0.1:5000.

Or open Command Prompt in this folder and run:

```bat
py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Stop the server with Ctrl+C in the terminal.

## What this dashboard does

The scanner checks pasted Python source for a limited set of risky patterns. It reports line-based evidence and remediation guidance, but it does not execute pasted source or connect to remote systems. Findings are static-analysis leads, not proof.

The NumPy network learns a tiny synthetic teaching task using backpropagation. Its prediction is **not** a vulnerability probability. The genetic-algorithm component is a toy optimization demonstration, not a security detector.

## Maintained package

The actively maintained Python components now live in `../src/code_integrity_lab/`. The local `scanner.py`, `neural_net.py`, and `genetic.py` files are compatibility shims. The Flask app and active UI template now live in `../src/code_integrity_lab/web/`; the legacy `app.py` wrapper starts that packaged app.

## Cloud training

The package-level entry points are documented in [`../docs/training.md`](../docs/training.md) and [`../docs/cloud.md`](../docs/cloud.md). Existing wrapper scripts in `cloud/` remain available.

**Limits:** No trained large language model or validated vulnerability detector is included. Use only code you own or are authorized to assess.
