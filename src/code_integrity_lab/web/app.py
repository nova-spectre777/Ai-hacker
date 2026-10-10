"""Local Code Integrity Research Lab dashboard and JSON API."""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from code_integrity_lab import __version__
from code_integrity_lab.model.genetic_demo import evolve_threshold
from code_integrity_lab.model.toy_network import predict_demo, train_demo
from code_integrity_lab.security.scanner import scan_python

app = Flask(__name__, template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 1_000_000


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "project": "Code Integrity Research Lab",
            "version": __version__,
            "status": "available",
            "scope": "local demo APIs only; no GPU jobs are started by this dashboard",
        }
    )


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large; keep it under 1 MB."}), 413


@app.post("/api/scan")
def scan():
    body = request.get_json(silent=True) or {}
    source = body.get("source", "")
    filename = body.get("filename", "pasted_code.py")
    if not isinstance(source, str) or not source.strip():
        return jsonify({"error": "Paste Python source first."}), 400
    if len(source) > 200_000:
        return jsonify({"error": "Source exceeds the 200,000-character analysis limit."}), 413
    if not isinstance(filename, str):
        filename = "pasted_code.py"
    filename = filename[:120]
    findings = scan_python(source, filename)
    return jsonify(
        {
            "filename": filename,
            "count": len(findings),
            "findings": findings,
            "note": "Static-analysis leads only. Validate findings in an authorized environment.",
        }
    )


@app.post("/api/train")
def train():
    body = request.get_json(silent=True) or {}
    try:
        epochs = min(max(int(body.get("epochs", 80)), 1), 500)
        return jsonify(train_demo(epochs))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Toy-model training request failed")
        return jsonify({"error": "The toy training request failed; check the server log."}), 500


@app.post("/api/predict")
def predict():
    body = request.get_json(silent=True) or {}
    features = body.get("features", [])
    if not isinstance(features, list) or len(features) != 2:
        return jsonify({"error": "Provide exactly two numeric features."}), 400
    try:
        values = [float(value) for value in features]
        return jsonify(predict_demo(values))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/evolve")
def evolve():
    body = request.get_json(silent=True) or {}
    try:
        generations = min(max(int(body.get("generations", 30)), 1), 200)
        return jsonify(evolve_threshold(generations))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Toy genetic search request failed")
        return jsonify({"error": "The genetic demo failed; check the server log."}), 500


def main() -> None:
    """Run the local-only development dashboard."""
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
