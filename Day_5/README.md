# Developer Productivity & Code Quality Dashboard

Predicts **commit risk** (Low / Medium / High) from developer activity
metrics using a `RandomForestClassifier`, and visualizes team productivity
and code quality trends on a Flask + Chart.js dashboard.

## Project Structure
```
dev-productivity-dashboard/
├── data/
│   ├── generate_dataset.py     # creates the synthetic dataset
│   └── developer_productivity.csv
├── templates/
│   └── dashboard.html          # Chart.js dashboard UI
├── train.py                    # trains & saves the model
├── app.py                      # Flask server (dashboard + API)
├── requirements.txt
├── model.pkl                   # generated after training
├── encoder.pkl                 # generated after training
└── feature_importance.png      # generated after training
```

## Setup (VS Code / PowerShell)

1. Open the project folder in VS Code.

2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Run Steps

**Step 1 — Generate the dataset**
```powershell
python data/generate_dataset.py
```
This creates `data/developer_productivity.csv` (2000 rows, 20 simulated developers).

**Step 2 — Train the model**
```powershell
python train.py
```
This trains a tuned `RandomForestClassifier` (via `GridSearchCV`), prints
accuracy/classification report, and saves `model.pkl`, `encoder.pkl`, and
`feature_importance.png`.

**Step 3 — Launch the dashboard**
```powershell
python app.py
```
Open your browser to:
```
http://127.0.0.1:5000
```

## Dashboard Features
- **Commit Risk Distribution** — doughnut chart of Low/Medium/High counts
- **Feature Importance** — which metrics drive risk predictions most
- **Top 10 Developers** — ranked by weekly commit volume
- **Live Prediction Form** — enter metrics for a new commit/week and get an
  instant risk prediction with class probabilities

## Dataset Columns
| Column | Description |
|---|---|
| developer_id | Simulated developer identifier |
| commits_per_week | Number of commits in the week |
| lines_added / lines_deleted | Code churn |
| files_changed | Number of files touched |
| bugs_reported | Bugs logged against the developer's code |
| code_review_comments | Review feedback received |
| avg_review_time_hours | Average time for PRs to be reviewed |
| test_coverage_percent | Test coverage of changed code |
| deployment_frequency | Deploys per week |
| late_night_commits | Commits made after 10pm (fatigue signal) |
| commit_risk | Target label — Low / Medium / High |

## Next Steps
- Swap the synthetic dataset for real Git history (via `GitPython` or the
  GitHub API) once available.
- Add SQLite storage to log predictions over time (matches the DevPulse
  pattern of persisting commit-risk history).
- Add authentication if deploying beyond localhost.
