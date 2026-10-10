"""Small NumPy backpropagation demonstration.

This module trains a tiny neural network on synthetic teaching data to demonstrate
weight updates and loss tracking. It is not trained for, calibrated for, or suitable
for vulnerability detection.
"""
from __future__ import annotations

from typing import Any

import numpy as np

_X = np.array(
    [
        [0, 0], [0, 1], [1, 0], [1, 1], [.1, .2], [.2, .9],
        [.9, .2], [.9, .9], [.05, .95], [.95, .05], [.8, .8], [.1, .1],
    ],
    dtype=float,
)
_Y = np.array([[0], [1], [0], [1], [0], [1], [0], [1], [1], [0], [1], [0]], dtype=float)
_MODEL: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None = None


def sigmoid(value: np.ndarray) -> np.ndarray:
    """Numerically bounded sigmoid."""
    return 1.0 / (1.0 + np.exp(-np.clip(value, -40, 40)))


def train_demo(epochs: int = 80) -> dict[str, Any]:
    """Run actual backpropagation on the tiny synthetic teaching set."""
    global _MODEL
    if not isinstance(epochs, int) or not 1 <= epochs <= 500:
        raise ValueError("epochs must be an integer between 1 and 500")

    rng = np.random.default_rng(7)
    w1 = rng.normal(0, 0.7, (2, 4))
    b1 = np.zeros((1, 4))
    w2 = rng.normal(0, 0.7, (4, 1))
    b2 = np.zeros((1, 1))
    losses: list[float] = []

    for _ in range(epochs):
        hidden = np.tanh(_X @ w1 + b1)
        prediction = sigmoid(hidden @ w2 + b2)
        epsilon = 1e-7
        loss = -np.mean(
            _Y * np.log(prediction + epsilon)
            + (1 - _Y) * np.log(1 - prediction + epsilon)
        )
        losses.append(round(float(loss), 6))

        output_gradient = (prediction - _Y) / len(_X)
        dw2 = hidden.T @ output_gradient
        db2 = output_gradient.sum(axis=0, keepdims=True)
        hidden_gradient = (output_gradient @ w2.T) * (1 - hidden * hidden)
        dw1 = _X.T @ hidden_gradient
        db1 = hidden_gradient.sum(axis=0, keepdims=True)

        learning_rate = 0.8
        w2 -= learning_rate * dw2
        b2 -= learning_rate * db2
        w1 -= learning_rate * dw1
        b1 -= learning_rate * db1

    _MODEL = (w1, b1, w2, b2)
    return {
        "message": "Backpropagation completed on synthetic teaching data.",
        "epochs": epochs,
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "losses": losses,
        "warning": "This toy model is not a cybersecurity classifier and must not guide security decisions.",
    }


def predict_demo(features: list[float]) -> dict[str, Any]:
    """Return a toy score for two numeric features, never a vulnerability probability."""
    global _MODEL
    if len(features) != 2:
        raise ValueError("features must contain exactly two numbers")
    try:
        vector = np.asarray(features, dtype=float).reshape(1, 2)
    except (TypeError, ValueError) as exc:
        raise ValueError("features must contain numeric values") from exc
    if not np.all(np.isfinite(vector)):
        raise ValueError("features must be finite numbers")

    if _MODEL is None:
        train_demo(80)
    assert _MODEL is not None
    w1, b1, w2, b2 = _MODEL
    score = float(sigmoid(np.tanh(vector @ w1 + b1) @ w2 + b2)[0, 0])
    return {
        "score": round(score, 4),
        "label": "higher toy score" if score >= 0.5 else "lower toy score",
        "warning": "This is not a vulnerability probability. Do not use it for security decisions.",
    }
