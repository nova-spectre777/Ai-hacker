"""Report local Python and optional GPU-training environment without changing the system."""
from __future__ import annotations

import importlib.metadata
import importlib.util
import platform
import sys


def main() -> int:
    print("Code Integrity Research Lab — environment check")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    for package in ("numpy", "flask", "torch", "transformers", "datasets", "tokenizers", "accelerate"):
        if importlib.util.find_spec(package) is None:
            print(f"{package}: not installed")
            continue
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = "installed (version unavailable)"
        print(f"{package}: {version}")
    if importlib.util.find_spec("torch") is not None:
        import torch

        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU count: {torch.cuda.device_count()}")
            for index in range(torch.cuda.device_count()):
                print(f"GPU {index}: {torch.cuda.get_device_name(index)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
