from flask import Flask, request, jsonify, render_template
from scanner import scan_python
from neural_net import train_demo, predict_demo
from genetic import evolve_threshold
app=Flask(__name__)
@app.get("/")
def home(): return render_template("index.html")
@app.post("/api/scan")
def scan():
    b=request.get_json(silent=True) or {}; src=str(b.get("source",""))[:200000]; name=str(b.get("filename","pasted_code.py"))[:120]
    if not src.strip(): return jsonify({"error":"Paste Python source first."}),400
    f=scan_python(src,name)
    return jsonify({"filename":name,"count":len(f),"findings":f,"note":"Static-analysis leads only. Validate findings in an authorized environment."})
@app.post("/api/train")
def train():
    b=request.get_json(silent=True) or {}
    try: return jsonify(train_demo(min(max(int(b.get("epochs",80)),1),500)))
    except Exception as e: return jsonify({"error":str(e)}),500
@app.post("/api/predict")
def predict():
    b=request.get_json(silent=True) or {}
    try:
        x=[float(v) for v in b.get("features",[])]
        if len(x)!=2: return jsonify({"error":"Provide exactly two numeric features."}),400
        return jsonify(predict_demo(x))
    except (TypeError,ValueError) as e: return jsonify({"error":str(e)}),400
@app.post("/api/evolve")
def evolve():
    b=request.get_json(silent=True) or {}
    try: return jsonify(evolve_threshold(min(max(int(b.get("generations",30)),1),200)))
    except Exception as e: return jsonify({"error":str(e)}),500
if __name__=="__main__":
    # Local only: does not expose the lab to your LAN.
    app.run(host="127.0.0.1",port=5000,debug=False)
