# Developer Productivity — Model Comparison (Day 6)

Internship Day 6 task: training and comparing multiple classification models on a developer productivity dataset to predict `developer_id` from behavioral/productivity features.

## Overview

This notebook loads a developer productivity dataset, prepares it for modeling, and trains four different classifiers to compare their performance:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Each model is evaluated on accuracy, precision, recall, and F1-score, and the best-performing model is saved for reuse.

## Dataset

- **File**: `developer_productivity.csv`
- **Target**: `developer_id`
- **Features**: remaining columns, one-hot encoded with `pd.get_dummies()`
- **Split**: 80% train / 20% test (`random_state=42`)

## Workflow

1. Load and inspect the dataset with pandas
2. Separate features (`X`) and target (`y`)
3. One-hot encode categorical features
4. Split into train/test sets
5. Train each of the four models
6. Evaluate with accuracy, precision, recall, and F1-score
7. Compare all models in a single results table
8. Visualize results with a confusion matrix (Logistic Regression)
9. Save the comparison table and the best model to disk

## Results

| Model                | Accuracy |
|-----------------------|----------|
| Gradient Boosting      | 0.658075 |
| Logistic Regression    | 0.655125 |
| Random Forest          | 0.649450 |
| Decision Tree          | 0.571975 |

Gradient Boosting had the highest accuracy, closely followed by Logistic Regression. Decision Tree performed noticeably worse, likely due to overfitting without depth/parameter tuning.

## Outputs

- `model_comparison.csv` — accuracy, precision, recall, and F1-score for all four models
- `confusion_matrix.png` — confusion matrix for the Logistic Regression model
- `best_model.pkl` — saved model (via `joblib`)

## Tech Stack

- Python
- pandas
- scikit-learn
- seaborn / matplotlib
- joblib

## How to Run

1. Place `developer_productivity.csv` in the working directory (update the path if not using Google Colab's `/content/` structure).
2. Install dependencies:
   ```bash
   pip install pandas scikit-learn seaborn matplotlib joblib
   ```
3. Run the notebook cells in order.

## Notes / Learnings

- Comparing multiple models side by side highlights trade-offs between simplicity (Logistic Regression) and flexibility (ensemble methods like Random Forest and Gradient Boosting).
- Weighted precision/recall/F1 were used since this is a multi-class classification problem.
- Next steps could include hyperparameter tuning (e.g., `GridSearchCV`) and feature importance analysis for the tree-based models.
