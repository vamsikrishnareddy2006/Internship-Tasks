# Student Grade Predictor 🎓📊

A machine learning project that analyzes student performance data and predicts final grades (G3) using multiple regression models. Built as part of an internship data science task.

## 📋 Overview

This project explores the relationship between student habits (study time, absences, failures, etc.) and their final academic grades, then trains and compares several machine learning models to predict grades for new students.

## ✨ Features

- **Exploratory Data Analysis** — visualizes grade trends across study time, absences, gender, and more
- **Multiple ML Models** — trains and compares Linear Regression, Ridge, Lasso, Decision Tree, Random Forest, and Gradient Boosting
- **Model Evaluation** — reports RMSE, MAE, R², and accuracy for each model
- **Automatic Best Model Selection** — picks the top-performing model based on R² score
- **Feature Importance** — visualizes which factors matter most for predicting grades
- **Model Persistence** — saves the trained model with `pickle` for reuse
- **New Student Prediction** — predicts a grade for a custom student profile

## 🛠️ Tech Stack

- **Python 3**
- **pandas** & **numpy** — data handling
- **matplotlib** & **seaborn** — visualizations
- **scikit-learn** — machine learning models and evaluation

## 📁 Project Structure

```
Internship-Tasks/
├── student-mat.csv              # Dataset (student performance data)
├── student grade predictor.py   # Main analysis & prediction script
├── model.pkl                    # Saved trained model
├── chart1.png                   # Study Time vs Final Grade
├── chart2.png                   # Absences vs Final Grade
├── chart3.png                   # Grade Distribution
├── chart4.png                   # Grade Distribution by Gender
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas matplotlib seaborn numpy scikit-learn
```

### Running the Script

```bash
python "student grade predictor.py"
```

Make sure `student-mat.csv` is in the same folder as the script.

## 📊 Dataset

The dataset (`student-mat.csv`) contains student attributes such as:

| Column | Description |
|---|---|
| `studytime` | Weekly study time (1 = low, 4 = high) |
| `failures` | Number of past class failures |
| `absences` | Number of school absences |
| `age` | Student age |
| `sex` | Student gender |
| `G3` | Final grade (target variable) |

## 📈 Sample Output

The script prints model evaluation metrics for each model, e.g.:

```
--- Random Forest ---
RMSE     : 2.15
R²       : 0.78
Accuracy : 34.50%

Best model: Random Forest
```

Charts generated:
- Study time vs average final grade
- Absences vs final grade (scatter)
- Grade distribution (histogram)
- Grade distribution by gender (boxplot)

## 🔮 Predicting a New Student

The script includes a helper function to predict grades for a new student profile:

```python
predict_new_student(model, columns, [3, 0, 2, 17])
# studytime=3, failures=0, absences=2, age=17
```

## 📝 Notes

- The trained model is saved as `model.pkl` and reloaded to verify predictions stay consistent after saving/loading.
- Accuracy here is measured as an exact-match on rounded grade values — RMSE and R² are more meaningful metrics for this regression task.

## 👤 Author

**Vamsi Krishna Reddy Vemireddy**
📧 vamsikrishnareddy.sde@outlook.com

## 📄 License

This project is open source and available for educational purposes.
