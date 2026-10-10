"""Conservative static checks for Python source; findings are leads, not proof."""
import ast
import re

RULES = [
    ("PY001", "Use of eval()", "high", r"\beval\s*\(",
     "Avoid eval() on untrusted input; it evaluates expressions dynamically."),
    ("PY002", "Use of exec()", "high", r"\bexec\s*\(",
     "Avoid exec() on untrusted input; it executes dynamically constructed code."),
    ("PY003", "subprocess with shell=True", "high",
     r"subprocess\.(?:run|Popen|call|check_output)\s*\([\s\S]{0,500}?shell\s*=\s*True",
     "Shell execution with constructed or untrusted strings may permit command injection. Prefer argument lists and shell=False."),
    ("PY004", "Possible hard-coded secret", "high",
     r"""(?i)\b(?:api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['"][^'"]{5,}['"]""",
     "Move credentials to a secret manager or environment variable; rotate any exposed secret."),
    ("PY005", "Potential unsafe YAML loading", "high", r"yaml\.load\s*\(",
     "For untrusted YAML, prefer yaml.safe_load() and review loader behavior."),
    ("PY006", "TLS verification disabled", "high", r"verify\s*=\s*False",
     "Disabling certificate verification weakens TLS protection."),
    ("PY007", "MD5/SHA-1 use", "medium", r"hashlib\.(?:md5|sha1)\s*\(",
     "MD5/SHA-1 are unsuitable for many security-sensitive uses; select an appropriate modern primitive."),
    ("PY008", "Pickle deserialization", "high", r"\bpickle\.loads?\s*\(",
     "Never unpickle data from untrusted sources; deserialization may execute code."),
    ("PY009", "Debug mode enabled", "medium", r"(?i)\bdebug\s*=\s*True\b",
     "Ensure debug mode is disabled in production."),
    ("PY010", "Possible SQL string formatting", "medium",
     r"""(?i)(?:execute|executemany)\s*\(\s*(?:f['"]|['"][^'"]{0,200}%s)""",
     "Use parameterized SQL queries rather than string formatting."),
]

def scan_python(source, filename="pasted_code.py"):
    lines = source.splitlines()
    findings = []
    try:
        ast.parse(source)
        syntax = None
    except SyntaxError as exc:
        line_no = exc.lineno or 1
        syntax = {
            "rule_id": "PY000", "title": "Python syntax error", "severity": "info",
            "line": line_no,
            "snippet": lines[line_no - 1][:240] if line_no <= len(lines) else "",
            "description": f"Parser could not analyze this file: {exc.msg}. Fix syntax to improve analysis.",
            "filename": filename,
        }
    for rule_id, title, severity, pattern, description in RULES:
        regex = re.compile(pattern)
        for line_no, line in enumerate(lines, 1):
            if regex.search(line):
                findings.append({
                    "rule_id": rule_id, "title": title, "severity": severity,
                    "line": line_no, "snippet": line.strip()[:240],
                    "description": description, "confidence": "medium",
                    "filename": filename,
                })
    if syntax:
        findings.insert(0, syntax)
    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    return sorted(findings, key=lambda item: (order.get(item["severity"], 4), item["line"]))
