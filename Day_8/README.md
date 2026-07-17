# Day 8 — Hyperparameter Tuning: Developer Productivity & Commit Risk

## Overview
This project builds on the Day 7 model comparison by tuning a Logistic Regression classifier to predict **commit risk** (Low / Medium / High) from developer activity metrics, using GridSearchCV for hyperparameter optimization.

## Dataset
`developer_productivity.csv` — 2,000 records with features including:
- Commits per week, lines added/deleted, files changed
- Bugs reported, code review comments, average review time
- Test coverage %, deployment frequency, late-night commits
- Target: `commit_risk` (Low / Medium / High)

## Workflow
1. **Baseline comparison** — trained and evaluated 4 models:
   | Model | Accuracy | F1-Score (weighted) |
   |---|---|---|
   | Logistic Regression | 0.7825 | 0.7797 |
   | Decision Tree | 0.6925 | 0.6939 |
   | Random Forest | 0.7575 | 0.7456 |
   | Gradient Boosting | 0.7650 | 0.7612 |

2. **Cross-validation** — 5-fold CV on Logistic Regression gave a mean F1 of **0.7866** (± 0.0177).

3. **Hyperparameter tuning** — `GridSearchCV` over `C`, `max_iter`, and `solver`:
   - **Best parameters:** `C=0.1, max_iter=3000, solver='lbfgs'`
   - **Best CV F1 score:** 0.8033
   - **Tuned test F1 score:** 0.7929 (up from a baseline of 0.7797)

## Files
- `Hyperparameter_Turning_Day_8.ipynb` — full notebook (EDA, training, CV, tuning)
- `model_comparison.csv` — accuracy/precision/recall/F1 for all 4 baseline models
- `best_model.pkl` — baseline Logistic Regression model
- `tuned_model.pkl` — GridSearchCV-tuned Logistic Regression model
- `confusion_matrix.png` — confusion matrix for baseline Logistic Regression
- `validation_curve.png` — mean CV F1 score across grid search parameter combinations

## Key Takeaway
Hyperparameter tuning improved the Logistic Regression model's F1-score from 0.78 to 0.79 on the test set. Gradient Boosting remains competitive out-of-the-box, suggesting a good next step would be tuning the ensemble models as well.

## Note on a fixed bug
An earlier version of this notebook re-instantiated `LogisticRegression()` without calling `.fit()` before saving with `joblib.dump()`, resulting in an untrained model being persisted to `best_model.pkl`. This was corrected by re-fitting the model on `X_train`/`y_train` before saving.
