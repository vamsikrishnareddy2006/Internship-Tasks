import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score

# ==========================
# LOAD DATASET
# ==========================
script_dir = Path(__file__).resolve().parent
csv_path = script_dir / 'student-mat.csv'
df = pd.read_csv(csv_path, sep=';')
print(df.head())

# ==========================
# FUNCTION: ENCODE CATEGORICAL COLUMNS
# ==========================
def encode_categoricals(data):
    data_encoded = data.copy()
    encoders = {}
    for col in data_encoded.select_dtypes(include='object').columns:
        le = LabelEncoder()
        data_encoded[col] = le.fit_transform(data_encoded[col])
        encoders[col] = le
    return data_encoded, encoders

df_encoded, encoders = encode_categoricals(df)

# ==========================
# FUNCTION: BAR CHART
# ==========================
def plot_bar_chart(data):
    avg_by_study = data.groupby('studytime')['G3'].mean()
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

plot_bar_chart(df)

# ==========================
# FUNCTION: SCATTER PLOT
# ==========================
def plot_scatter_chart(data):
    plt.figure(figsize=(7,4))
    plt.scatter(
        data['absences'],
        data['G3'],
        alpha=0.5,
        color='#E8631A'
    )
    plt.title('Absences vs Final Grade')
    plt.xlabel('Absences')
    plt.ylabel('Final Grade (G3)')
    plt.savefig('chart2.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_scatter_chart(df)

# ==========================
# FUNCTION: HISTOGRAM
# ==========================
def plot_histogram(data):
    plt.figure(figsize=(7,4))
    plt.hist(
        data['G3'],
        bins=20,
        color='#0D9488',
        edgecolor='white'
    )
    plt.axvline(
        data['G3'].mean(),
        color='red',
        linestyle='--',
        label=f"Mean={data['G3'].mean():.1f}"
    )
    plt.title('Grade Distribution')
    plt.legend()
    plt.savefig('chart3.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_histogram(df)

# ==========================
# FUNCTION: BOXPLOT BY GENDER
# ==========================
def plot_boxplot_gender(data):
    plt.figure(figsize=(7,4))
    data.boxplot(column='G3', by='sex', grid=False,
                 patch_artist=True,
                 boxprops=dict(facecolor='#7C3AED'))
    plt.title('Grade Distribution by Gender')
    plt.suptitle('')
    plt.xlabel('Sex')
    plt.ylabel('Final Grade (G3)')
    plt.savefig('chart4.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_boxplot_gender(df)

# ==========================
# FUNCTION: CORRELATION HEATMAP
# ==========================
def plot_correlation_heatmap(data_encoded):
    plt.figure(figsize=(12,9))
    corr = data_encoded.corr(numeric_only=True)
    sns.heatmap(corr, cmap='coolwarm', center=0, annot=False)
    plt.title('Feature Correlation Heatmap')
    plt.savefig('chart5.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_correlation_heatmap(df_encoded)

# ==========================
# FUNCTION: STUDY TIME VS FAILURES HEATMAP
# ==========================
def plot_studytime_failures_pivot(data):
    pivot = data.pivot_table(values='G3', index='studytime', columns='failures', aggfunc='mean')
    plt.figure(figsize=(7,5))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd')
    plt.title('Average Grade by Study Time & Failures')
    plt.xlabel('Failures')
    plt.ylabel('Study Time')
    plt.savefig('chart6.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_studytime_failures_pivot(df)

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
# FUNCTION: TRAIN MODEL
# ==========================
def train_model(X_train, y_train, model_type='linear'):
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'ridge':
        model = Ridge(alpha=1.0, random_state=42)
    elif model_type == 'lasso':
        model = Lasso(alpha=0.1, random_state=42, max_iter=5000)
    elif model_type == 'tree':
        model = DecisionTreeRegressor(max_depth=5, random_state=42)
    elif model_type == 'forest':
        model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
    elif model_type == 'gboost':
        model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05,
                                           max_depth=3, random_state=42)
    else:
        raise ValueError("Unknown model_type")
    model.fit(X_train, y_train)
    return model

model_types = ['linear', 'ridge', 'lasso', 'tree', 'forest', 'gboost']
trained_models = {}
for m_type in model_types:
    trained_models[m_type] = train_model(X_train, y_train, model_type=m_type)

# ==========================
# FUNCTION: EVALUATE MODEL
# ==========================
def evaluate_model(model, X_test, y_test, name='Model'):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    y_pred_rounded = np.rint(y_pred).astype(int)
    accuracy = accuracy_score(y_test, y_pred_rounded)

    print(f"\n--- {name} ---")
    print(f"RMSE    : {rmse:.2f}")
    print(f"MAE     : {mae:.2f}")
    print(f"R²      : {r2:.3f}")
    print(f"Accuracy: {accuracy*100:.2f}%")
    return {'name': name, 'rmse': rmse, 'mae': mae, 'r2': r2, 'accuracy': accuracy}

results = []
for m_type, trained in trained_models.items():
    results.append(evaluate_model(trained, X_test, y_test, name=m_type))

# ==========================
# FUNCTION: CROSS VALIDATE MODEL
# ==========================
def cross_validate_model(model, X, y, cv=5):
    scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    print(f"Cross-val R² scores: {np.round(scores, 3)} | Mean: {scores.mean():.3f}")
    return scores.mean()

cross_validate_model(trained_models['forest'], X, y)

# ==========================
# FUNCTION: COMPARE MODELS
# ==========================
def compare_models(results):
    results_df = pd.DataFrame(results).sort_values(by='r2', ascending=False)
    print("\n=== Model Comparison (sorted by R²) ===")
    print(results_df.to_string(index=False))
    best_name = results_df.iloc[0]['name']
    print(f"\nBest model: {best_name}")
    return best_name

best_model_name = compare_models(results)
best_model = trained_models[best_model_name]

# ==========================
# FUNCTION: FEATURE IMPORTANCE
# ==========================
def plot_feature_importance(model, feature_names, name='model'):
    if not hasattr(model, 'feature_importances_'):
        print(f"{name} has no feature_importances_ (skipping plot)")
        return
    importances = model.feature_importances_
    order = np.argsort(importances)[::-1]
    plt.figure(figsize=(7,4))
    plt.bar(np.array(feature_names)[order], importances[order], color='#7C3AED')
    plt.title(f'Feature Importance ({name})')
    plt.savefig('chart7.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_feature_importance(best_model, X.columns, name=best_model_name)

# ==========================
# FUNCTION: PREDICT NEW STUDENT
# ==========================
def predict_new_student(model, columns, values):
    new_student = pd.DataFrame([values], columns=columns)
    predicted = model.predict(new_student)
    print(f"Predicted Grade: {predicted[0]:.1f}")
    return predicted[0]

predict_new_student(best_model, X.columns, [3, 0, 2, 17])
predict_new_student(best_model, X.columns, [2, 1, 5, 16])

# ==========================
# FUNCTION: SAVE MODEL
# ==========================
def save_model(model, filename='model.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print("Model Saved!")

save_model(best_model, 'model.pkl')

# ==========================
# FUNCTION: LOAD MODEL
# ==========================
def load_model(filename='model.pkl'):
    with open(filename, 'rb') as f:
        
        loaded_model = pickle.load(f)
    return loaded_model

loaded_model = load_model('model.pkl')
test_input = pd.DataFrame([[2, 1, 5, 16]], columns=X.columns)
test_pred = loaded_model.predict(test_input)
print(f"Loaded Model Prediction: {test_pred[0]:.1f}")