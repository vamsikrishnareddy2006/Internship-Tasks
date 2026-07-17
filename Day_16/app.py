"""
DevPulse - Developer Productivity & Code Quality Dashboard
Day 15: HTML + Flask + SQLite + ML model, fully integrated.

Loads the trained commit-risk classifier, serves the prediction form,
logs every prediction to a local SQLite database, and shows a
git-log-styled history of past predictions.
"""

from flask import Flask, render_template, request, g, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import joblib
import pandas as pd
import os
import re
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("DEVPULSE_SECRET_KEY", "dev-pulse-secret-key-change-in-production")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "predictions.db")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------------
# 2b. Auth helpers
# ---------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def create_user(username, email, password):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (username, email, generate_password_hash(password), datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    db.commit()


def find_user_by_username(username):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


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
# 3. Auth routes
# ---------------------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("signup.html", active="signup")

    try:
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm_password") or ""

        errors = []
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        elif not re.match(r"^[A-Za-z0-9_.]+$", username):
            errors.append("Username can only contain letters, numbers, underscores, and dots.")
        if not EMAIL_RE.match(email):
            errors.append("Please enter a valid email address.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        if password != confirm:
            errors.append("Passwords do not match.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("signup.html", active="signup", username=username, email=email)

        if find_user_by_username(username):
            flash("That username is already taken.", "error")
            return render_template("signup.html", active="signup", email=email)

        try:
            create_user(username, email, password)
        except sqlite3.IntegrityError:
            flash("That username or email is already registered.", "error")
            return render_template("signup.html", active="signup", email=email)

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    except Exception as e:
        flash(f"Something went wrong while creating your account: {e}", "error")
        return render_template("signup.html", active="signup")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("login.html", active="login")

    try:
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html", active="login", username=username)

        user = find_user_by_username(username)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html", active="login", username=username)

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash(f"Welcome back, {user['username']}!", "success")
        next_url = request.args.get("next")
        return redirect(next_url or url_for("home"))

    except Exception as e:
        flash(f"Something went wrong while logging in: {e}", "error")
        return render_template("login.html", active="login")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------------
# 4. App routes
# ---------------------------------------------------------------
@app.route("/")
@login_required
def home():
    return render_template("home.html", active="home")


@app.route("/about")
@login_required
def about():
    return render_template("about.html", active="about")


@app.route("/predict", methods=["GET"])
@login_required
def predict_form():
    return render_template("index.html", fields=FIELD_META, active="predict")


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    # ------------------------------------------------------------
    # Step 1: validate every field individually. Never let a bad
    # value reach the model — collect ALL problems and show them
    # together instead of crashing on the first one.
    # ------------------------------------------------------------
    errors = []
    input_values = []
    raw_inputs = {}
    submitted = {}

    for name, label, placeholder, min_v, max_v in FIELD_META:
        raw = request.form.get(name, "")
        submitted[name] = raw
        raw = raw.strip() if raw is not None else ""

        if raw == "":
            errors.append(f"{label} is required — please enter a value.")
            continue

        try:
            value = float(raw)
        except ValueError:
            errors.append(f"{label} must be a valid number (you entered '{raw}').")
            continue

        if value != value:  # NaN check
            errors.append(f"{label} must be a valid number.")
            continue

        if value < min_v or value > max_v:
            errors.append(f"{label} must be between {min_v} and {max_v} (you entered {value}).")
            continue

        raw_inputs[name] = value
        input_values.append(value)

    if errors:
        return render_template(
            "index.html", fields=FIELD_META, errors=errors,
            submitted=submitted, active="predict",
        )

    # ------------------------------------------------------------
    # Step 2: run the model. Any unexpected failure here is caught
    # and shown as a friendly message — the app must never 500.
    # ------------------------------------------------------------
    try:
        X = pd.DataFrame([input_values], columns=FEATURES)
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        confidence = round(max(probabilities) * 100, 2)

        prob_breakdown = {
            cls: round(prob * 100, 2)
            for cls, prob in zip(model.classes_, probabilities)
        }

        risk = RISK_INFO.get(prediction)
        if risk is None:
            raise ValueError(f"Unrecognized prediction class returned by the model: {prediction}")

        # positive/negative framing for the result box:
        # Low risk = healthy/positive (green), High risk = negative (red),
        # Medium risk = caution (amber)
        outcome = "positive" if prediction == "Low" else ("negative" if prediction == "High" else "neutral")

        save_prediction(raw_inputs, prediction, confidence)

        return render_template(
            "result.html",
            prediction=prediction,
            outcome=outcome,
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

    except ValueError as e:
        return render_template(
            "index.html", fields=FIELD_META,
            errors=[f"Invalid input for prediction: {e}"],
            submitted=submitted, active="predict",
        )
    except Exception as e:
        return render_template(
            "index.html", fields=FIELD_META,
            errors=[f"Something went wrong while generating the prediction. Please try again. ({e})"],
            submitted=submitted, active="predict",
        )


@app.route("/history")
@login_required
def history():
    try:
        records = fetch_history()
    except Exception:
        records = []
        flash("Could not load prediction history right now. Please try again shortly.", "error")
    return render_template(
        "history.html", records=records, class_colors=CLASS_COLORS, active="history"
    )


# ---------------------------------------------------------------
# 5. Error handlers — the app should never show a raw 500 page
# ---------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404,
                            message="That page doesn't exist."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500,
                            message="Something went wrong on our end. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
