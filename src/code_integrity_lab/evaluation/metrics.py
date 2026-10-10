"""Task-explicit metrics for binary classification experiments."""
from __future__ import annotations

from collections.abc import Sequence


def binary_classification_metrics(
    y_true: Sequence[int],
    y_pred: Sequence[int],
) -> dict[str, int | float]:
    """Compute common binary-classification metrics from 0/1 labels.

    Undefined ratios are reported as 0.0; callers must document the dataset and threshold.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("at least one example is required")

    truth = [int(value) for value in y_true]
    prediction = [int(value) for value in y_pred]
    if any(value not in (0, 1) for value in truth + prediction):
        raise ValueError("binary labels must be 0 or 1")

    tp = sum(actual == 1 and guess == 1 for actual, guess in zip(truth, prediction))
    tn = sum(actual == 0 and guess == 0 for actual, guess in zip(truth, prediction))
    fp = sum(actual == 0 and guess == 1 for actual, guess in zip(truth, prediction))
    fn = sum(actual == 1 and guess == 0 for actual, guess in zip(truth, prediction))

    def ratio(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    precision = ratio(tp, tp + fp)
    recall = ratio(tp, tp + fn)
    return {
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "accuracy": ratio(tp + tn, len(truth)),
        "precision": precision,
        "recall": recall,
        "f1": ratio(2 * precision * recall, precision + recall),
        "false_positive_rate": ratio(fp, fp + tn),
        "false_negative_rate": ratio(fn, fn + tp),
        "support": len(truth),
    }
