"""
day6_algorithm_comparison.py
------------------------------
Day 6: Algorithm Comparison — Developer Productivity & Code Quality Dashboard

Follows the Day 6 task structure:
 1. Load the cleaned dataset (developer_productivity.csv) + sanity checks
 2. Separate features/target, train-test split (random_state=42)
 3. Preprocessing — encode target labels, scale numeric features
 4. Train primary algorithm + additional models for comparison
 5. Run predictions, print raw results, save trained models

Deliverable (per Algorithm Comparison deck):
    - Comparison DataFrame with Accuracy, Precision, Recall, F1
    - Best model identified with justification
    - Exported to CSV + pushed to GitHub /day6/ folder

Run:
    python day6_algorithm_comparison.py
"""

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# =========================================================
# STEP 1: Load your M1 cleaned dataset (Universal)
# =========================================================
data = pd.read_csv("data/developer_productivity.csv")

print("=" * 60)
print("STEP 1: DATASET OVERVIEW")
print("=" * 60)
print("Shape:", data.shape)
print("\nData types:\n", data.dtypes)
print("\nMissing values per column:\n", data.isnull().sum())

if data.isnull().sum().sum() > 0:
    data = data.dropna()
    print("\nDropped rows with missing values. New shape:", data.shape)

# =========================================================
# STEP 2: Separate features and target, then split (Universal)
# =========================================================
FEATURE_COLS = [
    "commits_per_week", "lines_added", "lines_deleted", "files_changed",
    "bugs_reported", "code_review_comments", "avg_review_time_hours",
    "test_coverage_percent", "deployment_frequency", "late_night_commits"
]
TARGET_COL = "commit_risk"

X = data[FEATURE_COLS].copy()
y_raw = data[TARGET_COL]

# Encode target (Low/Medium/High -> 0/1/2)
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y_raw)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n" + "=" * 60)
print("STEP 2: TRAIN-TEST SPLIT")
print("=" * 60)
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

# =========================================================
# STEP 3: Apply required preprocessing (Project-specific)
# =========================================================
# All features here are already numeric, but they're on very different
# scales (e.g. lines_added ~100s vs test_coverage_percent ~0-100 vs
# late_night_commits ~0-5), so we scale them for the distance/margin-based
# models (KNN, SVM, Logistic Regression).
numeric_cols = FEATURE_COLS  # every feature is numeric in this dataset

scaler = StandardScaler()
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

print("\n" + "=" * 60)
print("STEP 3: PREPROCESSING COMPLETE")
print("=" * 60)
print("Scaled columns:", numeric_cols)
print("Target classes:", list(target_encoder.classes_))

# Save preprocessing tools immediately
joblib.dump(scaler, "scaler.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")
print("Saved scaler.pkl and target_encoder.pkl")

# =========================================================
# STEP 4: Train primary algorithm + comparison models
# =========================================================
print("\n" + "=" * 60)
print("STEP 4: TRAINING MODELS")
print("=" * 60)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(random_state=42),   # <- primary algorithm
    "SVM": SVC(probability=True, random_state=42),
}

trained_models = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    trained_models[name] = model
    print(f"Trained: {name}")

# =========================================================
# STEP 5: Run predictions, print raw results, compare metrics
# =========================================================
print("\n" + "=" * 60)
print("STEP 5: PREDICTIONS & COMPARISON")
print("=" * 60)

results = {"Model": [], "Accuracy": [], "Precision": [], "Recall": [], "F1": []}

for name, model in trained_models.items():
    y_pred = model.predict(X_test)

    # 'weighted' average is used since this is a 3-class (Low/Medium/High)
    # problem with imbalanced classes (High risk is rare).
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    results["Model"].append(name)
    results["Accuracy"].append(round(acc, 4))
    results["Precision"].append(round(prec, 4))
    results["Recall"].append(round(rec, 4))
    results["F1"].append(round(f1, 4))

    pred_labels = target_encoder.inverse_transform(y_pred[:10])
    actual_labels = target_encoder.inverse_transform(y_test[:10])

    print(f"\n--- {name} ---")
    print("First 10 predictions:", list(pred_labels))
    print("First 10 actual:     ", list(actual_labels))
    print(f"Accuracy={acc:.4f}  Precision={prec:.4f}  Recall={rec:.4f}  F1={f1:.4f}")

    if name == "Random Forest":
        proba = model.predict_proba(X_test)
        print("Predict_proba (first 5 rows, columns =", list(target_encoder.classes_), "):\n", proba[:5])

    assert len(y_pred) == len(y_test), "Prediction count doesn't match actual count!"

# Comparison DataFrame
comparison_df = pd.DataFrame(results).sort_values("F1", ascending=False).reset_index(drop=True)

print("\n" + "=" * 60)
print("MODEL COMPARISON TABLE")
print("=" * 60)
print(comparison_df.to_string(index=False))

best_model_name = comparison_df.iloc[0]["Model"]
print(f"\nBest model based on F1-score: {best_model_name}")
print("Justification: F1-score balances precision and recall across all three "
      "risk classes, which matters here since 'High' risk commits are rare "
      "compared to 'Low' and 'Medium' — plain accuracy would hide poor "
      "performance on the minority class.")

# Save comparison table for the GitHub deliverable
comparison_df.to_csv("model_comparison.csv", index=False)
print("\nSaved model_comparison.csv")

# Save the best model
joblib.dump(trained_models[best_model_name], "best_model.pkl")
print(f"Saved best_model.pkl ({best_model_name})")

# Also save Random Forest specifically as first_model.pkl per task instructions
joblib.dump(trained_models["Random Forest"], "first_model.pkl")
print("Saved first_model.pkl (Random Forest baseline)")
