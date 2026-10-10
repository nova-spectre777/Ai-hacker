from __future__ import annotations

from code_integrity_lab.web.app import app


def test_health_endpoint_reports_local_demo_scope() -> None:
    response = app.test_client().get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["project"] == "Code Integrity Research Lab"
    assert "no GPU jobs" in payload["scope"]


def test_dashboard_renders_packaged_template() -> None:
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Code Integrity Research Lab" in response.data


def test_scan_api_reports_evidence_without_executing_source() -> None:
    response = app.test_client().post(
        "/api/scan",
        json={"filename": "example.py", "source": "eval(user_value)\n"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] >= 1
    assert payload["findings"][0]["filename"] == "example.py"

    inert_response = app.test_client().post(
        "/api/scan",
        json={"source": "raise RuntimeError('source must never run')\n"},
    )
    assert inert_response.status_code == 200
    assert inert_response.get_json()["count"] == 0
