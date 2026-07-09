# Day 9 – Developer Productivity & Code Quality Dashboard Improvement

## Overview
This project analyzes a developer productivity dataset and builds classification models to predict developer identity/category based on coding activity metrics. Four models are trained and compared, followed by hyperparameter tuning and feature importance analysis on the top-performing linear model.

## Dataset
- File: `developer_productivity.csv`
- Features include coding activity metrics such as commits, lines added/deleted, and other productivity indicators
- Categorical features encoded using one-hot encoding (`pd.get_dummies`)
- Split: 80% train / 20% test (`random_state=42`)

## Models Compared
| Model | Accuracy |
|---|---|
| Logistic Regression | 0.6551 |
| Decision Tree | 0.5720 |
| Random Forest | 0.6495 |
| **Gradient Boosting** | **0.6581** |

Precision, recall, and F1-score (weighted) were also computed for each model. Results saved to `model_comparison.csv`.

## Model Tuning
Logistic Regression was selected for deeper analysis and tuned using `GridSearchCV` (5-fold CV, scoring = weighted F1):

- **Parameter grid:** `C`, `max_iter`, `solver`
- **Baseline F1:** 0.6284
- **Tuned F1:** 0.6314

The tuned model is saved as `tuned_model.pkl`.

## Evaluation & Visualizations
- **Confusion Matrix** (`confusion_matrix.png`) – Logistic Regression predictions vs actual labels
- **Validation Curve** (`validation_curve.png`) – Mean CV F1-score across GridSearchCV parameter combinations
- **Feature Importance** (`feature_importance.png`) – Top features ranked by absolute Logistic Regression coefficients

## Files in this Folder
| File | Description |
|---|---|
| `Day_9_Developer_Productivity_&_Code_Quality_Dashboard.ipynb` | Main notebook with full workflow |
| `developer_productivity.csv` | Source dataset |
| `model_compariso.csv` | Model comparison metrics |
| `best_model.pkl` | Saved baseline model |
| `tuned_model.pkl` | GridSearchCV-tuned Logistic Regression model |
| `confusion_matrix.png` | Confusion matrix visualization |
| `validation_curve.png` | GridSearchCV validation curve |
| `feature_importance.png` | Feature importance chart |

## Tech Stack
- Python, Pandas, NumPy
- Scikit-learn (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, GridSearchCV)
- Matplotlib, Seaborn
- Joblib (model persistence)

## How to Run
1. Open the notebook in Jupyter or Google Colab
2. Ensure `developer_productivity.csv` is available in the working directory
3. Run all cells sequentially to reproduce training, evaluation, and saved artifacts

## Key Takeaway
Gradient Boosting achieved the highest raw accuracy among the four baseline models, while Logistic Regression was selected for tuning due to its interpretability. GridSearchCV tuning produced a modest F1-score improvement (0.6284 → 0.6314) over the baseline.
