# Day 14 – DevPulse: Final Model Integration & Testing

**Project:** Developer Productivity & Code Quality Dashboard (DevPulse)
**Track:** Track 3 – Deployment & Full-Stack Integration
**Focus of the day:** Wiring the trained `.pkl` machine learning model into the full-stack Flask application, end to end.

---

## 1. Summary

Today's task was to complete the final integration of DevPulse: connect the HTML frontend, the Flask backend, and the trained classification model so a user can submit developer activity metrics on a webpage and instantly get back a **commit risk prediction** (Low / Medium / High) with a confidence score.

While wiring this up, I found and fixed a serious bug carried over from Days 7–10: the notebooks had accidentally trained every model to predict `developer_id` (an identifier column) instead of the actual target column, `commit_risk`. That meant every "trained" model from earlier days was not learning anything meaningful. For today's integration to genuinely work, I retrained a clean model on the correct target before connecting it to Flask.

## 2. Current Implementation Status ✅

| Task | Status |
|---|---|
| Import and load trained `.pkl` model file | ✅ Done — `best_model.pkl` loaded via `joblib` at Flask startup |
| Test the model using sample input values | ✅ Done — verified via direct Python test and via `curl` against the running server |
| Connect HTML forms with Flask routes | ✅ Done — `index.html` form → `/predict` route |
| Pass user inputs from webpage to Flask backend | ✅ Done — `request.form` reads all 10 metric fields |
| Generate predictions using the integrated model | ✅ Done — `model.predict()` + `model.predict_proba()` |
| Display prediction results on the webpage | ✅ Done — `result.html` shows risk badge, confidence %, per-class probability bars |
| Full integration: HTML → Flask → Model → Prediction | ✅ Done and tested |
| Verify complete workflow functions correctly | ✅ Done — tested with Low-risk and High-risk sample inputs |
| Fix bugs found during testing | ✅ Done (see below) |
| Improve UI / professional look | ✅ Done — card-based layout, dark mode, probability bars, sample-fill button |

## 3. Steps Followed

1. Reviewed the existing `.pkl` models from Days 7–10 and inspected them with `joblib.load()`.
2. Discovered the target-column bug (`developer_id` used as `y` instead of `commit_risk`).
3. Retrained a clean **Random Forest classifier** on `developer_productivity.csv` using the correct target (`commit_risk`) and the 10 real feature columns (commits/week, lines added/deleted, files changed, bugs reported, review comments, avg review time, test coverage %, deployment frequency, late-night commits).
4. Tuned the model with `GridSearchCV` (5-fold CV, weighted F1) → best test accuracy **74.25%**, weighted F1 **0.74**.
5. Saved `best_model.pkl`, `scaler.pkl` (StandardScaler), and `feature_names.pkl` with `joblib.dump()`.
6. Built `app.py`:
   - Loads model, scaler, and feature list once at startup.
   - `/` route renders the input form (`index.html`).
   - `/predict` route (POST) reads form values, builds a labeled `pandas.DataFrame`, scales it, runs `model.predict()` / `predict_proba()`, and renders `result.html`.
7. Built the frontend (`templates/base.html`, `index.html`, `result.html`) with a shared nav bar, dark-mode toggle, and a visual "HTML → Flask → Model → Prediction" flow strip, styled consistently with the Day 13 expense tracker's design system (`static/css/style.css`).
8. Ran the Flask server locally and tested the full request/response cycle with `curl`, submitting both a "healthy" sample and a "risky" sample.
9. Fixed a `sklearn` "X does not have valid feature names" warning by passing a labeled DataFrame into the scaler instead of a raw NumPy array.

## 4. Testing Evidence

**Test 1 – Low-risk profile** (high commits, low bugs, high test coverage, no late-night commits)
→ Predicted **Low Risk**, confidence **98.33%**

**Test 2 – High-risk profile** (large diffs, many bugs, zero review comments, long review time, low coverage, many late-night commits)
→ Predicted **High Risk**, confidence **57.54%**

Both requests returned `HTTP 200` and rendered correctly, confirming the full pipeline — **HTML form → Flask route → model.predict() → webpage** — works end to end.

## 5. Screenshots

| Integration Flow | Input Form | Prediction Output |
|---|---|---|
| `screenshots/3_integration_flow.png` | `screenshots/1_input_form.png` | `screenshots/2_prediction_result.png` |

## 6. Bugs Found & Fixed

1. **Target leakage / wrong label (critical):** Days 7–10 trained on `developer_id` as `y` instead of `commit_risk`. Fixed by retraining on the correct target with a proper train/test split and `StandardScaler`.
2. **sklearn feature-name warning:** scaler was fit on a DataFrame but called at inference time with a raw NumPy array. Fixed by building a `pandas.DataFrame` with the exact training column order before calling `scaler.transform()`.
3. **Flask reloader killing the background process during testing:** `debug=True` reloader spawned a watchdog subprocess that didn't survive between shell sessions; switched to `debug=False` for stable testing.

## 7. Key Learnings

- A model can train, evaluate, and even report a "good" accuracy score while silently learning the wrong thing — always double-check `X`/`y` column selection before trusting a `.pkl` file for deployment.
- `joblib`-saved scalers and models must be fed data in the **exact same shape, column order, and type** they were fitted on; mismatches cause silent warnings or bad predictions rather than hard errors.
- Testing the full request/response cycle with `curl` (not just eyeballing the browser) makes it easy to catch integration bugs and prove the pipeline works.
- Keeping the UI's design tokens (colors, spacing, font) consistent across days makes each new page feel like part of the same product rather than a one-off.

## 8. Plan for Tomorrow

- Add input validation on the client side (range checks, inline error messages) to match the pattern used in the Day 13 expense tracker.
- Add a "prediction history" table (SQLite) so past predictions can be reviewed, similar to the expense tracker's list view.
- Write unit tests for the `/predict` route covering valid input, missing fields, and out-of-range values.
- Deploy the app (Render/Railway) so the Track 3 "Deployment & Full-Stack Integration" objective is fully complete.

---

## Project Structure

```
Day_14/
├── app.py                    # Flask app: loads model, form → predict route
├── train_model.py            # Clean retraining script (fixes target-leakage bug)
├── best_model.pkl            # Trained Random Forest classifier
├── scaler.pkl                # StandardScaler fitted on training features
├── feature_names.pkl         # Ordered list of the 10 feature columns
├── developer_productivity.csv
├── requirements.txt
├── make_screenshots.py       # Generates the mockup screenshots below
├── screenshots/
│   ├── 1_input_form.png
│   ├── 2_prediction_result.png
│   └── 3_integration_flow.png
├── templates/
│   ├── base.html
│   ├── index.html            # Input form
│   └── result.html           # Prediction output page
└── static/
    ├── css/style.css
    └── js/script.js           # Dark mode toggle
```

## Model Details

- **Algorithm:** Random Forest Classifier (`class_weight="balanced"`, tuned via `GridSearchCV`)
- **Target:** `commit_risk` — Low / Medium / High
- **Features (10):** `commits_per_week`, `lines_added`, `lines_deleted`, `files_changed`, `bugs_reported`, `code_review_comments`, `avg_review_time_hours`, `test_coverage_percent`, `deployment_frequency`, `late_night_commits`
- **Test Accuracy:** 74.25% | **Weighted F1:** 0.7405

## Running the Project

```bash
pip install -r requirements.txt
python train_model.py   # optional: regenerates best_model.pkl / scaler.pkl
python app.py
```

Then open: http://127.0.0.1:5000
