"""
generate_dataset.py
--------------------
Generates a synthetic "Developer Productivity & Code Quality" dataset.

Simulates weekly activity for a team of developers: commit activity,
code churn, review behaviour, bug counts and test coverage - then
derives a 'commit_risk' label (Low / Medium / High) that a model can
be trained to predict.

Run:
    python data/generate_dataset.py
Output:
    data/developer_productivity.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N_RECORDS = 2000
DEVELOPERS = [f"dev_{i:02d}" for i in range(1, 21)]  # 20 developers

rows = []
for _ in range(N_RECORDS):
    dev_id = np.random.choice(DEVELOPERS)

    commits_per_week = np.random.poisson(8)
    lines_added = int(np.random.gamma(shape=2.0, scale=80))
    lines_deleted = int(np.random.gamma(shape=1.5, scale=40))
    files_changed = np.random.poisson(4) + 1
    bugs_reported = np.random.poisson(1.2)
    code_review_comments = np.random.poisson(3)
    avg_review_time_hours = round(np.random.exponential(scale=6), 1)
    test_coverage_percent = round(np.clip(np.random.normal(75, 15), 10, 100), 1)
    deployment_frequency = np.random.poisson(2)          # deploys/week
    late_night_commits = np.random.poisson(1.0)           # commits after 10pm

    # ---- Derive a "risk score" from the underlying factors ----
    risk_score = (
        (lines_added + lines_deleted) / 50.0
        + bugs_reported * 4
        + late_night_commits * 3
        + max(0, 40 - test_coverage_percent) * 0.3
        + max(0, avg_review_time_hours - 10) * 0.5
        - code_review_comments * 1.2
        - deployment_frequency * 0.8
    )
    risk_score += np.random.normal(0, 3)  # noise

    if risk_score < 8:
        commit_risk = "Low"
    elif risk_score < 18:
        commit_risk = "Medium"
    else:
        commit_risk = "High"

    rows.append([
        dev_id, commits_per_week, lines_added, lines_deleted, files_changed,
        bugs_reported, code_review_comments, avg_review_time_hours,
        test_coverage_percent, deployment_frequency, late_night_commits,
        commit_risk
    ])

columns = [
    "developer_id", "commits_per_week", "lines_added", "lines_deleted",
    "files_changed", "bugs_reported", "code_review_comments",
    "avg_review_time_hours", "test_coverage_percent",
    "deployment_frequency", "late_night_commits", "commit_risk"
]

df = pd.DataFrame(rows, columns=columns)
df.to_csv("data/developer_productivity.csv", index=False)

print("Dataset created: data/developer_productivity.csv")
print("Shape:", df.shape)
print("\nRisk label distribution:")
print(df["commit_risk"].value_counts())
