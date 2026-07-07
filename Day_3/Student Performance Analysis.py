"""
Student Performance Analysis
A function-based pandas/EDA script for student-mat.csv
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

script_dir = Path(__file__).resolve().parent
csv_path = script_dir / 'student-mat.csv'


# ----------------------------
# 1. DATA LOADING
# ----------------------------
def load_data(path):
    """Load the dataset and return a DataFrame."""
    df = pd.read_csv(path, sep=';')
    print(f"Loaded dataset with shape: {df.shape}")
    return df


# ----------------------------
# 2. BASIC INSPECTION
# ----------------------------
def inspect_data(df):
    """Print basic structural info about the dataset."""
    print("\n--- HEAD ---")
    print(df.head())
    print("\n--- INFO ---")
    print(df.info())
    print("\n--- SHAPE ---", df.shape)
    print("\n--- COLUMNS ---", list(df.columns))
    print("\n--- NULL VALUES ---")
    print(df.isnull().sum())
    print("\n--- DUPLICATES ---", df.duplicated().sum())


# ----------------------------
# 3. DESCRIPTIVE STATISTICS
# ----------------------------
def describe_data(df):
    """Print summary statistics for numeric and categorical columns."""
    print("\n--- NUMERIC SUMMARY ---")
    print(df.describe())
    print("\n--- CATEGORICAL SUMMARY ---")
    print(df.describe(include='object'))


# ----------------------------
# 4. CATEGORY ANALYSIS
# ----------------------------
def category_counts(df, columns):
    """Print value counts for a list of categorical columns."""
    for col in columns:
        print(f"\n--- {col.upper()} VALUE COUNTS ---")
        print(df[col].value_counts())
        print(f"--- {col.upper()} PERCENTAGE ---")
        print(df[col].value_counts(normalize=True).round(3) * 100)


# ----------------------------
# 5. FILTERING & SELECTION
# ----------------------------
def filter_hardworkers(df, min_studytime=2):
    """Return students with studytime greater than threshold."""
    hardworkers = df[df['studytime'] > min_studytime]
    print(f"\nHard workers (>{min_studytime}): {len(hardworkers)}")
    print("Their avg grade:", hardworkers['G3'].mean())
    return hardworkers


def top_bottom_scorers(df, n=5):
    """Return top and bottom N students by final grade."""
    top = df.nlargest(n, 'G3')[['age', 'studytime', 'G3']]
    bottom = df.nsmallest(n, 'G3')[['age', 'studytime', 'G3']]
    print(f"\n--- TOP {n} SCORERS ---\n", top)
    print(f"\n--- BOTTOM {n} SCORERS ---\n", bottom)
    return top, bottom


# ----------------------------
# 6. GROUPBY ANALYSIS
# ----------------------------
def groupby_analysis(df, group_col, target_col='G3'):
    """Group by a column and compute mean/min/max/count of target."""
    result = df.groupby(group_col)[target_col].agg(['mean', 'min', 'max', 'count'])
    print(f"\n--- {group_col.upper()} vs {target_col} ---")
    print(result)
    return result


def multi_groupby(df, group_cols, target_col='G3'):
    """Group by multiple columns and compute mean of target."""
    result = df.groupby(group_cols)[target_col].mean()
    print(f"\n--- {group_cols} vs {target_col} ---")
    print(result)
    return result


# ----------------------------
# 7. ABSENCE ANALYSIS
# ----------------------------
def absence_analysis(df, low_thresh=3, high_thresh=10):
    """Compare grades between low and high absence groups."""
    low = df[df['absences'] <= low_thresh]['G3'].mean()
    high = df[df['absences'] > high_thresh]['G3'].mean()
    print(f"\nLow absences (<= {low_thresh}) avg grade: {low:.1f}")
    print(f"High absences (> {high_thresh}) avg grade: {high:.1f}")
    return low, high


# ----------------------------
# 8. FEATURE ENGINEERING
# ----------------------------
def add_pass_fail_column(df, threshold=10):
    """Add a Pass/Fail column based on G3 threshold."""
    df['pass_fail'] = df['G3'].apply(lambda x: 'Pass' if x >= threshold else 'Fail')
    print("\nPass/Fail counts:\n", df['pass_fail'].value_counts())
    return df


def add_age_group(df):
    """Bin ages into groups."""
    df['age_group'] = pd.cut(df['age'], bins=[14, 16, 18, 22], labels=['15-16', '17-18', '19+'])
    print("\nAvg grade by age group:\n", df.groupby('age_group')['G3'].mean())
    return df


def encode_categoricals(df, columns):
    """One-hot encode selected categorical columns."""
    df_encoded = pd.get_dummies(df, columns=columns, drop_first=True)
    print(f"\nEncoded columns: {columns}")
    print("New shape:", df_encoded.shape)
    return df_encoded


# ----------------------------
# 9. CORRELATION
# ----------------------------
def correlation_with_target(df, target_col='G3'):
    """Print correlation of all numeric columns with target."""
    corr = df.corr(numeric_only=True)[target_col].sort_values(ascending=False)
    print(f"\n--- CORRELATION WITH {target_col} ---")
    print(corr)
    return corr


# ----------------------------
# 10. VISUALIZATION
# ----------------------------
def plot_studytime_vs_grade(df, save_path=None):
    """Bar plot of average grade by study time."""
    plt.figure(figsize=(6, 4))
    df.groupby('studytime')['G3'].mean().plot(kind='bar', color='steelblue')
    plt.title("Average Final Grade by Study Time")
    plt.xlabel("Study Time")
    plt.ylabel("Average G3")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.close()


def plot_correlation_heatmap(df, save_path=None):
    """Heatmap of correlations between numeric columns."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=False, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.close()


def plot_grade_distribution(df, save_path=None):
    """Histogram of final grades."""
    plt.figure(figsize=(6, 4))
    sns.histplot(df['G3'], bins=20, kde=True, color='seagreen')
    plt.title("Distribution of Final Grades (G3)")
    plt.xlabel("G3")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.close()


# ----------------------------
# 11. SIMPLE ML MODEL (bonus)
# ----------------------------
def train_simple_model(df):
    """Train a basic linear regression to predict G3 from study-related features."""
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, r2_score

    features = ['studytime', 'absences', 'failures', 'G1', 'G2']
    X = df[features]
    y = df['G3']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print("\n--- MODEL RESULTS ---")
    print("MAE:", mean_absolute_error(y_test, preds))
    print("R2 Score:", r2_score(y_test, preds))
    print("Coefficients:", dict(zip(features, model.coef_)))
    return model


# ----------------------------
# 12. EXPORT
# ----------------------------
def export_data(df, filename='student-mat-enhanced.csv'):
    """Save processed DataFrame to CSV."""
    output_path = script_dir / filename
    df.to_csv(output_path, index=False)
    print(f"\nSaved enhanced dataset to {output_path}")


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    df = load_data(csv_path)
    inspect_data(df)
    describe_data(df)
    category_counts(df, ['sex', 'internet', 'school', 'address'])

    filter_hardworkers(df)
    top_bottom_scorers(df)

    groupby_analysis(df, 'studytime')
    groupby_analysis(df, 'internet')
    multi_groupby(df, ['studytime', 'internet'])

    absence_analysis(df)

    df = add_pass_fail_column(df)
    df = add_age_group(df)

    correlation_with_target(df)

    plot_studytime_vs_grade(df, script_dir / 'studytime_vs_grade.png')
    plot_correlation_heatmap(df, script_dir / 'correlation_heatmap.png')
    plot_grade_distribution(df, script_dir / 'grade_distribution.png')

    df_encoded = encode_categoricals(df, ['sex', 'internet', 'school', 'address'])

    train_simple_model(df)

    export_data(df, 'student-mat-enhanced.csv')

    return df, df_encoded


if __name__ == "__main__":
    final_df, encoded_df = main()