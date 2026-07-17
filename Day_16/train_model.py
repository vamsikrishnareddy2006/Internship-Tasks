import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score

df = pd.read_csv("developer_productivity.csv")

FEATURES = [
    "commits_per_week", "lines_added", "lines_deleted", "files_changed",
    "bugs_reported", "code_review_comments", "avg_review_time_hours",
    "test_coverage_percent", "deployment_frequency", "late_night_commits"
]
TARGET = "commit_risk"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 8, 12],
    "min_samples_split": [2, 5],
    "class_weight": ["balanced"]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid, cv=5, scoring="f1_weighted", n_jobs=-1
)
grid.fit(X_train_scaled, y_train)

best_model = grid.best_estimator_
y_pred = best_model.predict(X_test_scaled)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print("Best params:", grid.best_params_)
print("Test Accuracy:", round(acc, 4))
print("Test Weighted F1:", round(f1, 4))
print(classification_report(y_test, y_pred))

joblib.dump(best_model, "best_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(FEATURES, "feature_names.pkl")

print("\nSaved: best_model.pkl, scaler.pkl, feature_names.pkl")
