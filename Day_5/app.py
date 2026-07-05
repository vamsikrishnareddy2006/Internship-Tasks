"""
app.py
------
Flask backend for the Developer Productivity & Code Quality Dashboard.

Serves:
    GET  /                -> dashboard UI (Chart.js visualizations)
    GET  /api/summary      -> aggregated stats for charts
    POST /api/predict      -> commit risk prediction for new input

Run:
    python app.py
Then open:
    http://127.0.0.1:5000
"""

import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ---- Load model, encoder, and dataset ----
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

data = pd.read_csv("data/developer_productivity.csv")

FEATURE_COLS = [
    "commits_per_week", "lines_added", "lines_deleted", "files_changed",
    "bugs_reported", "code_review_comments", "avg_review_time_hours",
    "test_coverage_percent", "deployment_frequency", "late_night_commits"
]


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/summary")
def summary():
    """Aggregated data for the dashboard charts."""
    risk_counts = data["commit_risk"].value_counts().reindex(
        ["Low", "Medium", "High"], fill_value=0
    ).to_dict()

    per_dev = (
        data.groupby("developer_id")
        .agg(
            avg_commits=("commits_per_week", "mean"),
            avg_bugs=("bugs_reported", "mean"),
            avg_coverage=("test_coverage_percent", "mean"),
        )
        .round(1)
        .reset_index()
        .sort_values("avg_commits", ascending=False)
        .head(10)
    )

    importances = pd.Series(
        model.feature_importances_, index=FEATURE_COLS
    ).sort_values(ascending=False).round(3)

    return jsonify({
        "risk_counts": risk_counts,
        "top_developers": per_dev.to_dict(orient="records"),
        "feature_importance": importances.to_dict(),
        "avg_test_coverage": round(data["test_coverage_percent"].mean(), 1),
        "avg_bugs_per_week": round(data["bugs_reported"].mean(), 2),
        "total_records": len(data),
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    try:
        features = np.array([[payload[col] for col in FEATURE_COLS]])
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

    pred_encoded = model.predict(features)[0]
    pred_label = encoder.inverse_transform([pred_encoded])[0]
    probabilities = model.predict_proba(features)[0]
    prob_dict = {
        cls: round(float(p), 3)
        for cls, p in zip(encoder.classes_, probabilities)
    }

    return jsonify({
        "commit_risk": pred_label,
        "probabilities": prob_dict
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
