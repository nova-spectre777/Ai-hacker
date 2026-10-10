from __future__ import annotations

import pytest

from code_integrity_lab.evaluation.metrics import binary_classification_metrics


def test_binary_metrics_include_false_positives_and_misses() -> None:
    result = binary_classification_metrics([1, 1, 0, 0], [1, 0, 1, 0])
    assert result["true_positive"] == 1
    assert result["true_negative"] == 1
    assert result["false_positive"] == 1
    assert result["false_negative"] == 1
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["false_positive_rate"] == 0.5
    assert result["false_negative_rate"] == 0.5


def test_undefined_ratios_are_zero_not_division_errors() -> None:
    result = binary_classification_metrics([0, 0], [0, 0])
    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1"] == 0.0


def test_invalid_metric_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        binary_classification_metrics([], [])
    with pytest.raises(ValueError):
        binary_classification_metrics([0], [0, 1])
    with pytest.raises(ValueError):
        binary_classification_metrics([2], [1])
