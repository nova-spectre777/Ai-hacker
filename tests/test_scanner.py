from __future__ import annotations

import pytest

from code_integrity_lab.security.scanner import scan_python


def test_safe_source_has_no_findings() -> None:
    source = "def add(left, right):\n    return left + right\n"
    assert scan_python(source) == []


def test_eval_is_reported_with_line_and_filename() -> None:
    findings = scan_python("value = 1\nresult = eval(value)\n", "example.py")
    finding = next(item for item in findings if item["rule_id"] == "PY001")
    assert finding["line"] == 2
    assert finding["filename"] == "example.py"
    assert finding["severity"] == "high"
    assert "not proof" in finding["description"].lower() or "evaluating" in finding["description"].lower()


def test_multiline_subprocess_pattern_is_reported() -> None:
    source = "import subprocess\nsubprocess.run(\n    user_input,\n    shell=True,\n)\n"
    findings = scan_python(source)
    finding = next(item for item in findings if item["rule_id"] == "PY003")
    assert finding["line"] == 2
    assert finding["snippet"].startswith("subprocess.run")


def test_syntax_error_is_reported_but_source_is_not_executed() -> None:
    findings = scan_python("def broken(:\n    raise RuntimeError('should not run')\n")
    assert findings[0]["rule_id"] == "PY000"
    assert findings[0]["line"] == 1


def test_non_string_source_is_rejected() -> None:
    with pytest.raises(TypeError):
        scan_python(None)  # type: ignore[arg-type]
