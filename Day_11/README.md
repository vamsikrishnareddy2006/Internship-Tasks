# DevPulse

**Developer Productivity & Code Quality Dashboard**

DevPulse is a self-contained Flask web application that turns raw commit-level activity into actionable, visual insight. It engineers features from commit data (lines changed, commit frequency, complexity signals, bug-fix ratios), runs them through a trained machine learning classifier, and renders the results on an interactive, chart-driven dashboard.

Built as the Track 3 (Deployment & Full-Stack Integration) deliverable for a 20-Day Summer Internship.

---

## Problem Statement

Software teams generate a constant stream of commits and code changes, but most lack a lightweight, data-driven way to track developer productivity and code quality over time. Engineering managers often rely on subjective impressions, spreadsheets, or expensive enterprise tools. Small teams, students, and open-source maintainers have no accessible way to turn raw commit history into meaningful insight.

**DevPulse answers:** how can raw version-control activity be automatically transformed into a meaningful, visual, and predictive measure of developer productivity and code quality — using an accessible, self-hostable web app?

## Why DevPulse

| Existing Approach | Limitation |
|---|---|
| Enterprise analytics suites | Expensive, org-level integration only, inaccessible to students/small teams |
| Static analyzers (linters, SonarQube-style) | Measure code quality in isolation, no productivity correlation |
| Manual/spreadsheet reporting | Time-consuming, error-prone, doesn't scale |
| Native Git host insights | Purely descriptive counts/graphs, no predictive or quality-risk layer |

DevPulse combines a trained classifier, a relational data store, and an interactive dashboard in a single deployable Flask application — open, self-hostable, and customizable.

## Features

- **ML-powered classification** — predicts a developer productivity / code-quality category from commit features via a live `/predict` endpoint
- **Interactive dashboard** — Chart.js trend lines, bar/pie charts, summary cards, and status badges
- **Persistent history** — all commits, computed metrics, and predictions stored in SQLite
- **Polished UX** — loading spinners, toast notifications, and accessible (ARIA-labeled) markup
- **Production-ready deployment** — served via Gunicorn on Render.com

## Tech Stack

- **Backend:** Flask (Python), Jinja2 templating, Werkzeug
- **Machine Learning:** scikit-learn (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM — compared via weighted F1-score and tuned with GridSearchCV), joblib for persistence
- **Database:** SQLite
- **Frontend:** HTML5, CSS3 (Flexbox/Grid, responsive design), vanilla JavaScript (Fetch API)
- **Visualization:** Chart.js
- **Deployment:** Gunicorn + Render.com

## Architecture

```
Browser (HTML/CSS/JS, Chart.js)
        │  fetch() → /predict
        ▼
Flask Application (app.py)
   ├── Routing & Templating (Jinja2)
   ├── ML Engine (joblib: model, scaler, label encoder)
   └── Database Layer (SQLite)
        │
        ▼
Persisted commit metrics & prediction history
```

**Workflow:**
1. Commit-level data is collected (structured records: lines added/removed, frequency, complexity, bug-fix indicators)
2. Features are scaled/preprocessed with the persisted scaler artifact
3. The trained classifier predicts a productivity/quality category
4. Results are stored in SQLite
5. Flask renders the dashboard via Jinja2, pulling live data from the database
6. Chart.js visualizes trends for the developer/team lead

## Project Structure

```
DevPulse/
├── app.py                     # Entry point, routes, /predict endpoint
├── templates/                 # Jinja2 HTML templates (dashboard, history, base layout)
├── static/                    # CSS, JS, images
│   ├── css/
│   └── js/
├── models/                    # Persisted ML artifacts
│   ├── final_model.joblib
│   ├── final_scaler.joblib
│   └── final_label_encoder.joblib
├── database/                  # SQLite DB + schema/migration scripts
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/vamsikrishnareddy2006/Internship-Tasks.git
cd Internship-Tasks
pip install -r requirements.txt
```

### Run locally

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

### Production deployment

DevPulse is configured for deployment on [Render](https://render.com) using Gunicorn as the WSGI server:

```bash
gunicorn app:app
```

## API

### `POST /predict`

Accepts commit-level feature input and returns a predicted productivity/quality class with confidence score.

**Example response:**
```json
{
  "prediction": "High Productivity / Good Quality",
  "confidence": 0.91
}
```

## Model Training

Multiple classifiers were trained and compared using weighted F1-score:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)

Hyperparameters were tuned with `GridSearchCV`, and the best-performing model was persisted with `joblib` (`final_model.joblib`, `final_scaler.joblib`, `final_label_encoder.joblib`) for use in the live Flask app.

## Future Enhancements

- Direct GitHub/GitLab API or webhook integration for live commit ingestion
- Team- and organization-level dashboards with role-based access control
- Migration from SQLite to PostgreSQL for multi-user, production-scale deployments
- Deep learning / NLP analysis of commit messages and diffs for richer quality signals
- Email/Slack notifications for quality-risk flags
- Authenticated REST API for third-party integrations

## Author

**Vamsi Krishna Reddy Vemireddy**
Department of Computer Science and Engineering, Vel Tech University
20-Day Summer Internship — Track 3: Deployment & Full-Stack Integration

## License

This project was developed as part of an academic internship. Add a license of your choice (e.g., MIT) if you plan to open-source it.
