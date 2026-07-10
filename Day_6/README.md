# Day 6 — Algorithm Comparison: Developer Productivity & Code Quality Dashboard

Compares multiple classification algorithms to predict **commit risk**
(Low / Medium / High) from developer activity metrics, building on the
Day 5 dataset and baseline Random Forest model.

## Objective

Given weekly developer activity data (commits, code churn, bug reports,
review time, test coverage, etc.), predict whether a developer's commit
pattern falls into a **Low**, **Medium**, or **High** risk category —
then compare several algorithms to find the best performer.

## Dataset

`developer_productivity.csv` — synthetic dataset of 2000 records across
20 simulated developers.

| Column | Description |
|---|---|
| developer_id | Developer identifier |
| commits_per_week | Commits made in the week |
| lines_added / lines_deleted | Code churn |
| files_changed | Number of files touched |
| bugs_reported | Bugs logged against the developer's code |
| code_review_comments | Review feedback received |
| avg_review_time_hours | Average time for PRs to be reviewed |
| test_coverage_percent | Test coverage of changed code |
| deployment_frequency | Deploys per week |
| late_night_commits | Commits made after 10pm (fatigue signal) |
| commit_risk | Target label — Low / Medium / High |

## Workflow

1. **Load & inspect** — checked shape, dtypes, and missing values
2. **Split** — `train_test_split(test_size=0.2, random_state=42)`, stratified on the target
3. **Preprocess** — scaled all numeric features with `StandardScaler` (features are on very different scales — e.g. `lines_added` in the hundreds vs `test_coverage_percent` 0–100); encoded the target labels with `LabelEncoder`
4. **Train & compare models**:
   - Logistic Regression
   - Decision Tree
   - K-Nearest Neighbors (KNN)
   - Random Forest (primary/baseline algorithm)
   - Support Vector Machine (SVM)
5. **Evaluate** — compared Accuracy, Precision, Recall, and F1-score (weighted, to account for class imbalance since High-risk cases are rare)

## Results

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| **SVM** | 0.7825 | 0.7860 | 0.7825 | **0.7791** |
| Logistic Regression | 0.7800 | 0.7778 | 0.7800 | 0.7774 |
| Random Forest | 0.7575 | 0.7659 | 0.7575 | 0.7537 |
| Decision Tree | 0.6775 | 0.6727 | 0.6775 | 0.6745 |
| KNN | 0.6775 | 0.6658 | 0.6775 | 0.6636 |

**Best model: SVM**, selected using F1-score rather than raw accuracy —
F1 balances precision and recall across all three classes, which
matters here since `High` risk commits are underrepresented compared to
`Low` and `Medium`. Accuracy alone would mask poor performance on that
minority class.

## Project Structure
```
Day_6/
├── data/
│   ├── generate_dataset.py         # creates the synthetic dataset
│   └── developer_productivity.csv
├── day6_algorithm_comparison.py    # main script (or Day_6.ipynb notebook version)
├── model_comparison.csv            # exported comparison table
├── scaler.pkl                      # fitted StandardScaler
├── target_encoder.pkl              # fitted LabelEncoder for commit_risk
├── best_model.pkl                  # best-performing model (SVM)
├── first_model.pkl                 # baseline Random Forest model
└── README.md
```

## How to Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy scikit-learn joblib

python data/generate_dataset.py
python day6_algorithm_comparison.py
```

## Key Takeaways

- No single algorithm wins by default — SVM and Logistic Regression
  outperformed Random Forest and Decision Tree on this dataset, showing
  that simpler, margin/probability-based models can beat ensemble
  methods depending on the data's structure.
- Feature scaling matters for distance- and margin-based models (KNN,
  SVM, Logistic Regression) since raw features here span very different
  ranges.
- Accuracy alone is misleading on imbalanced classes — F1-score gave a
  more honest signal for choosing the best model.

## Next Steps

- Apply `GridSearchCV` to tune the top-performing models (SVM, Logistic
  Regression) for further improvement
- Replace the synthetic dataset with real Git commit history
- Integrate the best model into the Day 5 Flask dashboard for live predictions
