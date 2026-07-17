import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score

# ==========================
# LOAD DATASET
# ==========================

script_dir = Path(__file__).resolve().parent
csv_path = script_dir / 'student-mat.csv'
df = pd.read_csv(csv_path, sep=';')

print(df.head())

# ==========================
# BAR CHART
# ==========================

avg_by_study = df.groupby('studytime')['G3'].mean()

plt.figure(figsize=(7,4))

plt.bar(
    avg_by_study.index,
    avg_by_study.values,
    color=['#E8631A','#0D9488','#7C3AED','#16A34A']
)

plt.title('Study Time vs Final Grade')
plt.xlabel('Study Time (1=low, 4=high)')
plt.ylabel('Average Grade')

plt.savefig('chart1.png', dpi=150, bbox_inches='tight')

plt.show()

# ==========================
# SCATTER PLOT
# ==========================

plt.figure(figsize=(7,4))

plt.scatter(
    df['absences'],
    df['G3'],
    alpha=0.5,
    color='#E8631A'
)

plt.title('Absences vs Final Grade')
plt.xlabel('Absences')
plt.ylabel('Final Grade (G3)')

plt.savefig('chart2.png', dpi=150, bbox_inches='tight')

plt.show()

# ==========================
# HISTOGRAM
# ==========================

plt.figure(figsize=(7,4))

plt.hist(
    df['G3'],
    bins=20,
    color='#0D9488',
    edgecolor='white'
)

plt.axvline(
    df['G3'].mean(),
    color='red',
    linestyle='--',
    label=f"Mean={df['G3'].mean():.1f}"
)

plt.title('Grade Distribution')
plt.legend()

plt.savefig('chart3.png', dpi=150, bbox_inches='tight')

plt.show()

# ==========================
# TRAIN TEST SPLIT
# ==========================

X = df[['studytime','failures','absences','age']]
y = df['G3']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# ==========================
# MACHINE LEARNING MODEL
# ==========================

model = LinearRegression()

model.fit(X_train, y_train)

# ==========================
# EVALUATION
# ==========================

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.3f}")

# Convert continuous predictions to nearest integer grades for a simple "accuracy" measure
y_pred_rounded = np.rint(y_pred).astype(int)

accuracy = accuracy_score(y_test, y_pred_rounded)

print(f"Accuracy: {accuracy*100:.2f}%")

# ==========================
# NEW STUDENT PREDICTION
# ==========================

# Create a DataFrame with the same feature names used for training to avoid
# sklearn warnings about feature names when predicting.
new_student = pd.DataFrame([[3, 0, 2, 17]], columns=X.columns)

predicted = model.predict(new_student)

print(f"Predicted Grade: {predicted[0]:.1f}")

# ==========================
# SAVE MODEL
# ==========================

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model Saved!")

# ==========================
# LOAD MODEL
# ==========================

with open('model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Use DataFrame with feature names for loaded model prediction as well
test_input = pd.DataFrame([[2, 1, 5, 16]], columns=X.columns)
test_pred = loaded_model.predict(test_input)

print(f"Loaded Model Prediction: {test_pred[0]:.1f}")