"""
DevPulse - Developer Productivity & Code Quality Dashboard
Day 15: HTML + Flask + SQLite + ML model, fully integrated.

Loads the trained commit-risk classifier, serves the prediction form,
logs every prediction to a local SQLite database, and shows a
git-log-styled history of past predictions.
"""

from flask import Flask, render_template, request, g
import joblib
import pandas as pd
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "predictions.db")

# ---------------------------------------------------------------
# 1. Load trained model, scaler, and feature list ONCE at startup
# ---------------------------------------------------------------
model = joblib.load(os.path.join(BASE_DIR, "best_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
FEATURES = joblib.load(os.path.join(BASE_DIR, "feature_names.pkl"))

RISK_INFO = {
    "Low": {
        "color": "#34D399",
        "message": "Healthy commit pattern. Keep up the good review discipline.",
        "ekg": "0,45 20,45 30,45 38,10 46,80 54,45 80,45 120,45 130,45 138,20 146,68 154,45 "
               "180,45 220,45 230,45 238,10 246,80 254,45 280,45 300,45",
    },
    "Medium": {
        "color": "#F5A623",
        "message": "Some risk indicators present. Consider more code review coverage.",
        "ekg": "0,45 15,45 24,45 30,55 36,20 42,70 48,30 54,45 66,45 90,45 99,45 105,55 111,20 "
               "117,70 123,30 129,45 141,45 165,45 174,45 180,55 186,20 192,70 198,30 204,45 216,45 240,45 300,45",
    },
    "High": {
        "color": "#F0554A",
        "message": "High risk detected. Recommend immediate code review and test coverage improvements.",
        "ekg": "0,45 8,45 14,60 18,8 22,82 26,25 30,68 34,40 38,45 50,45 58,45 64,60 68,8 72,82 76,25 80,68 "
               "84,40 88,45 100,45 108,45 114,60 118,8 122,82 126,25 130,68 134,40 138,45 150,45 "
               "158,45 164,60 168,8 172,82 176,25 180,68 184,40 188,45 200,45 220,45 240,45 260,45 280,45 300,45",
    },
}

CLASS_COLORS = {"Low": "#34D399", "Medium": "#F5A623", "High": "#F0554A"}

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


# ---------------------------------------------------------------
# 2. SQLite helpers
# ---------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    columns = ", ".join(f"{f} REAL" for f in FEATURES)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            {columns},
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


def save_prediction(raw_inputs, prediction, confidence):
    db = get_db()
    cols = ["ts"] + FEATURES + ["prediction", "confidence"]
    placeholders = ", ".join("?" for _ in cols)
    values = [datetime.now().strftime("%Y-%m-%d %H:%M")] + [raw_inputs[f] for f in FEATURES] + [prediction, confidence]
    db.execute(f"INSERT INTO predictions ({', '.join(cols)}) VALUES ({placeholders})", values)
    db.commit()


def fetch_history(limit=30):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------
# 3. Routes
# ---------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", fields=FIELD_META, active="home")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_values = []
        raw_inputs = {}
        for name, *_ in FIELD_META:
            value = float(request.form.get(name, 0))
            raw_inputs[name] = value
            input_values.append(value)

        # Prepare + scale using the exact training column order/labels
        X = pd.DataFrame([input_values], columns=FEATURES)
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        confidence = round(max(probabilities) * 100, 2)

        prob_breakdown = {
            cls: round(prob * 100, 2)
            for cls, prob in zip(model.classes_, probabilities)
        }

        risk = RISK_INFO[prediction]

        # Log every prediction to SQLite
        save_prediction(raw_inputs, prediction, confidence)

        return render_template(
            "result.html",
            prediction=prediction,
            confidence=confidence,
            color=risk["color"],
            message=risk["message"],
            ekg_points=risk["ekg"],
            prob_breakdown=prob_breakdown,
            class_colors=CLASS_COLORS,
            raw_inputs=raw_inputs,
            fields=FIELD_META,
            pulse_color=risk["color"],
        )

    except Exception as e:
        return render_template("index.html", fields=FIELD_META, error=str(e), active="home")


@app.route("/history")
def history():
    records = fetch_history()
    return render_template(
        "history.html", records=records, class_colors=CLASS_COLORS, active="history"
    )


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
