"""
DevPulse - Developer Productivity & Code Quality Dashboard
Day 14: Final Model Integration & Testing

Loads the trained commit-risk classification model (best_model.pkl) and
scaler (scaler.pkl), serves an HTML form for developer activity metrics,
and returns a live risk prediction (Low / Medium / High) with confidence.
"""

from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# ---------------------------------------------------------------
# 1. Load trained model, scaler, and feature list ONCE at startup
# ---------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "best_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
FEATURES = joblib.load(os.path.join(BASE_DIR, "feature_names.pkl"))

RISK_INFO = {
    "Low": {
        "color": "#22c55e",
        "message": "Healthy commit pattern. Keep up the good review discipline."
    },
    "Medium": {
        "color": "#f59e0b",
        "message": "Some risk indicators present. Consider more code review coverage."
    },
    "High": {
        "color": "#ef4444",
        "message": "High risk detected. Recommend immediate code review and test coverage improvements."
    },
}

# Friendly labels + helper text shown next to each input field
FIELD_META = [
    ("commits_per_week", "Commits per Week", "e.g. 8", 0, 60),
    ("lines_added", "Lines Added", "e.g. 89", 0, 2000),
    ("lines_deleted", "Lines Deleted", "e.g. 54", 0, 2000),
    ("files_changed", "Files Changed", "e.g. 1", 0, 100),
    ("bugs_reported", "Bugs Reported", "e.g. 3", 0, 50),
    ("code_review_comments", "Code Review Comments", "e.g. 0", 0, 100),
    ("avg_review_time_hours", "Avg Review Time (hrs)", "e.g. 4.5", 0, 200),
    ("test_coverage_percent", "Test Coverage (%)", "e.g. 67.0", 0, 100),
    ("deployment_frequency", "Deployment Frequency", "e.g. 2", 0, 50),
    ("late_night_commits", "Late-Night Commits", "e.g. 1", 0, 60),
]


@app.route("/")
def home():
    """Render the input form."""
    return render_template("index.html", fields=FIELD_META)


@app.route("/predict", methods=["POST"])
def predict():
    """
    2. Receive form input from the webpage
    3. Prepare it for the model (order + scale)
    4. Generate a prediction
    5. Send the result back to the webpage
    """
    try:
        # --- Pass user inputs from the webpage to the backend ---
        input_values = []
        raw_inputs = {}
        for name, *_ in FIELD_META:
            value = float(request.form.get(name, 0))
            raw_inputs[name] = value
            input_values.append(value)

        # --- Prepare + scale exactly as done during training ---
        # Built as a DataFrame (not a raw array) so column names match what
        # the scaler/model were fitted on -- avoids sklearn's
        # "X does not have valid feature names" warning.
        X = pd.DataFrame([input_values], columns=FEATURES)
        X_scaled = scaler.transform(X)

        # --- Generate prediction using the integrated .pkl model ---
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        confidence = round(max(probabilities) * 100, 2)

        prob_breakdown = {
            cls: round(prob * 100, 2)
            for cls, prob in zip(model.classes_, probabilities)
        }

        risk = RISK_INFO.get(prediction, {"color": "#64748b", "message": ""})

        return render_template(
            "result.html",
            prediction=prediction,
            confidence=confidence,
            color=risk["color"],
            message=risk["message"],
            prob_breakdown=prob_breakdown,
            raw_inputs=raw_inputs,
            fields=FIELD_META,
        )

    except Exception as e:
        return render_template("index.html", fields=FIELD_META, error=str(e))


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
