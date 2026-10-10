from __future__ import annotations

import math

import pytest

from code_integrity_lab.model.toy_network import predict_demo, train_demo


def test_training_returns_real_loss_history() -> None:
    result = train_demo(epochs=8)
    assert result["epochs"] == 8
    assert len(result["losses"]) == 8
    assert all(math.isfinite(loss) for loss in result["losses"])
    assert result["warning"].startswith("This toy model")


def test_prediction_is_explicitly_not_a_vulnerability_probability() -> None:
    result = predict_demo([0.2, 0.8])
    assert 0.0 <= result["score"] <= 1.0
    assert "not a vulnerability probability" in result["warning"].lower()


def test_prediction_rejects_wrong_feature_count() -> None:
    with pytest.raises(ValueError):
        predict_demo([0.1])
