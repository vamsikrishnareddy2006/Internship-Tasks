# Day 15 – DevPulse: SQLite Integration & UI/UX Redesign

**Project:** Developer Productivity & Code Quality Dashboard (DevPulse)
**Focus:** Full integration of HTML + Flask + SQLite + ML model, with a complete visual redesign.

---

## 1. What's New Today

- **SQLite integration** — every prediction is now logged to a local `predictions.db` (table `predictions`), and a new **History** page shows past predictions in a git-log style feed.
- **Full redesign** — moved from a generic card-based light UI to a distinctive "developer vitals monitor" identity that fits DevPulse's own name and audience.
- **Verified end-to-end**: form → Flask → model → SQLite → result → history, all tested live.

## 2. Design Direction

DevPulse reads a developer's commit activity the way a heart-rate monitor reads vitals — so the whole UI leans into that metaphor instead of a generic dashboard look.

- **Palette:** deep navy-black (`#0A0F1E`) rather than pure black, with an indigo primary (`#6366F1`) for actions and three semantic "vitals" colors carried through everywhere — emerald `#34D399` (Low), amber `#F5A623` (Medium), coral `#F0554A` (High).
- **Type:** `JetBrains Mono` for headings, data, and labels (a real developer's typeface), paired with `Inter` for body copy — the same pairing feels native to tools like GitHub or Linear rather than a generic AI-app default.
- **Signature element:** an animated EKG pulse line built into the nav bar, and a matching EKG waveform on the result page whose shape gets more jagged as risk increases — Low is a calm, evenly-spaced beat; High is sharp and erratic. This is the one deliberate visual risk, directly justified by the product's name.
- **Form as terminal window:** the input form is styled like a code editor / `.env` file, with `$`-prefixed field labels and a three-dot terminal title bar, reinforcing that this is a developer tool.
- **History as git log:** past predictions are shown as rows styled like `git log --oneline`, with a colored commit dot per risk level.
- Dark-only by design (no light/dark toggle) — a deliberate choice consistent with the "always-on monitor" feel, not an oversight.

## 3. What Was Integrated

| Piece | Detail |
|---|---|
| HTML | `index.html` (form), `result.html` (EKG + probabilities), `history.html` (git-log feed), shared `base.html` |
| Flask | `app.py` — `/` (form), `/predict` (POST → model → DB write → result), `/history` (DB read → feed) |
| SQLite | `predictions.db`, table `predictions(id, ts, <10 feature columns>, prediction, confidence)`, created automatically on first run via `init_db()` |
| ML model | `best_model.pkl` (Random Forest) + `scaler.pkl`, loaded once at startup |

## 4. Testing Evidence

Ran the server locally and tested every route with `curl`:

| Test | Result |
|---|---|
| `GET /` | `HTTP 200` — form renders |
| `POST /predict` (healthy metrics) | `HTTP 200` → **Low**, 98.33% confidence |
| `POST /predict` (risky metrics) | `HTTP 200` → **High**, 57.54% confidence |
| `POST /predict` (mixed metrics) | `HTTP 200` → **High**, 65.79% confidence |
| `GET /history` | `HTTP 200` — shows all 3 logged predictions, most recent first, correct colors |
| SQLite check | `SELECT * FROM predictions` returned all 3 rows with correct timestamps, predictions, and confidence values |

No errors or warnings in the Flask log during any of these requests.

## 5. Screenshots

| Input Form | Prediction Result | History |
|---|---|---|
| `screenshots/1_input_form.png` | `screenshots/2_prediction_result.png` | `screenshots/3_history.png` |

## 6. Project Structure

```
Day_15/
├── app.py                    # Flask app + SQLite logging + history route
├── train_model.py            # Retraining script (reused from Day 14)
├── best_model.pkl / scaler.pkl / feature_names.pkl
├── developer_productivity.csv
├── requirements.txt
├── make_screenshots.py
├── screenshots/
├── templates/
│   ├── base.html             # Nav + animated pulse signature element
│   ├── index.html            # Terminal-styled input form
│   ├── result.html           # EKG-style risk visualization
│   └── history.html          # Git-log styled prediction history
└── static/
    ├── css/style.css         # Full design-token system
    └── js/script.js
```

## 7. Running the Project

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 — `predictions.db` is created automatically on first run.
