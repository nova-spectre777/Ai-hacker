"""Compatibility entry point for the packaged language-model trainer."""
from pathlib import Path
import sys

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src"
if str(_SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SOURCE_ROOT))

from code_integrity_lab.training.train_lm import main

if __name__ == "__main__":
    main()
