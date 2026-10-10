"""Compatibility shim for the original toy network dashboard."""
from pathlib import Path
import sys

_SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(_SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SOURCE_ROOT))

from code_integrity_lab.model.toy_network import predict_demo, sigmoid, train_demo

__all__ = ["predict_demo", "sigmoid", "train_demo"]
