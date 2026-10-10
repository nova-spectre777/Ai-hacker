"""Conservative regex-based Python source checks.

The scanner produces triage leads, not confirmed vulnerabilities. It never executes
scanned source or contacts a target. Regex checks can produce both false positives and
false negatives; findings require human validation.
"""
from __future__ import annotations

import ast
import re
from typing import Any

Rule = tuple[str, str, str, re.Pattern[str], str]

_RAW_RULES: tuple[tuple[str, str, str, str, int, str], ...] = (
    (
        "PY001", "Use of eval()", "high", r"\beval\s*\(", re.MULTILINE,
        "Avoid evaluating untrusted input dynamically. If expression evaluation is required, use a constrained parser.",
    ),
    (
        "PY002", "Use of exec()", "high", r"\bexec\s*\(", re.MULTILINE,
        "Avoid executing dynamically constructed code, especially when input may be untrusted.",
    ),
    (
        "PY003", "subprocess with shell=True", "high",
        r"subprocess\.(?:run|Popen|call|check_output)\s*\([\s\S]{0,500}?\bshell\s*=\s*True\b",
        re.MULTILINE,
        "Shell execution can create command-injection risk when arguments contain untrusted data. Prefer argument lists and shell=False.",
    ),
    (
        "PY004", "Possible hard-coded secret", "high",
        r"""(?i)\b(?:api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['"][^'"]{5,}['"]""",
        re.MULTILINE,
        "Move credentials to a secret manager or protected environment configuration; rotate any credential that was exposed.",
    ),
    (
        "PY005", "Potential unsafe YAML loading", "high", r"\byaml\.load\s*\(", re.MULTILINE,
        "For untrusted YAML, prefer yaml.safe_load() and verify the loader behavior for the installed library version.",
    ),
    (
        "PY006", "TLS verification disabled", "high", r"\bverify\s*=\s*False\b", re.MULTILINE,
        "Disabling certificate verification weakens TLS peer authentication. Keep verification enabled in production.",
    ),
    (
        "PY007", "MD5/SHA-1 use", "medium", r"\bhashlib\.(?:md5|sha1)\s*\(", re.MULTILINE,
        "MD5 and SHA-1 are unsuitable for many security-sensitive uses. Choose a primitive appropriate to the threat model.",
    ),
    (
        "PY008", "Pickle deserialization", "high", r"\bpickle\.loads?\s*\(", re.MULTILINE,
        "Never deserialize pickle data from untrusted sources; loading may execute attacker-controlled code.",
    ),
    (
        "PY009", "Debug mode enabled", "medium", r"(?i)\bdebug\s*=\s*True\b", re.MULTILINE,
        "Verify that debug mode is disabled in production deployments.",
    ),
    (
        "PY010", "Possible SQL string formatting", "medium",
        r"""(?is)(?:execute|executemany)\s*\(\s*(?:f['"]|['"][^'"]{0,200}%s)""",
        re.MULTILINE,
        "Use parameterized SQL queries rather than interpolation or string formatting.",
    ),
)

RULES: tuple[Rule, ...] = tuple(
    (rule_id, title, severity, re.compile(pattern, flags), description)
    for rule_id, title, severity, pattern, flags, description in _RAW_RULES
)


def _line_snippet(source_lines: list[str], line_number: int) -> str:
    if 1 <= line_number <= len(source_lines):
        return source_lines[line_number - 1].strip()[:240]
    return ""


def scan_python(source: str, filename: str = "pasted_code.py") -> list[dict[str, Any]]:
    """Scan Python source for a small set of suspicious patterns.

    The filename is report metadata only. Source code is parsed but never executed.
    Returned line numbers and snippets are evidence for review, not proof of exploitability.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")

    source_lines = source.splitlines()
    findings: list[dict[str, Any]] = []
    try:
        ast.parse(source, filename=filename)
    except SyntaxError as exc:
        line_number = exc.lineno or 1
        findings.append(
            {
                "rule_id": "PY000",
                "title": "Python syntax error",
                "severity": "info",
                "line": line_number,
                "snippet": _line_snippet(source_lines, line_number),
                "description": f"Python parsing stopped at this syntax error: {exc.msg}. Fix syntax to improve analysis.",
                "confidence": "high",
                "filename": filename,
            }
        )

    severity_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    for rule_id, title, severity, regex, description in RULES:
        for match in regex.finditer(source):
            line_number = source.count("\n", 0, match.start()) + 1
            findings.append(
                {
                    "rule_id": rule_id,
                    "title": title,
                    "severity": severity,
                    "line": line_number,
                    "snippet": _line_snippet(source_lines, line_number),
                    "description": description,
                    "confidence": "medium",
                    "filename": filename,
                }
            )

    return sorted(
        findings,
        key=lambda item: (
            severity_order.get(item["severity"], 4),
            item["line"],
            item["rule_id"],
        ),
    )
