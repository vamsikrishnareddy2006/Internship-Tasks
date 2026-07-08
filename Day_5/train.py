"""
train.py
--------
Trains a RandomForestClassifier to predict 'commit_risk'
(Low / Medium / High) from developer activity metrics.

Run:
    python train.py
Output:
    model.pkl        - trained model
    encoder.pkl      - label encoder for the target
    feature_importance.png
"""

import pandas as pd
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# ---- Load dataset ----
data = pd.read_csv("data/developer_productivity.csv")

print("Dataset Shape:", data.shape)
print("\nColumns:")
print(data.columns.tolist())

# ---- Features & Target ----
feature_cols = [
    "commits_per_week", "lines_added", "lines_deleted", "files_changed",
    "bugs_reported", "code_review_comments", "avg_review_time_hours",
    "test_coverage_percent", "deployment_frequency", "late_night_commits"
]

X = data[feature_cols]
y = data["commit_risk"]

# Encode target labels (Low/Medium/High -> 0/1/2)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# ---- Train-Test Split ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ---- GridSearchCV tuning ----
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    n_jobs=-1
)
grid.fit(X_train, y_train)

model = grid.best_estimator_
print("\nBest Params:", grid.best_params_)

# ---- Evaluate ----
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# ---- Feature Importance Chart ----
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values()
plt.figure(figsize=(8, 6))
importances.plot(kind="barh", color="#4C6EF5")
plt.title("Feature Importance - Commit Risk Prediction")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png")
print("\nSaved feature_importance.png")

# ---- Save Model & Encoder ----
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Model saved as model.pkl")
print("Encoder saved as encoder.pkl")