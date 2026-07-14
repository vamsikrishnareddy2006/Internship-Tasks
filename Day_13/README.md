# Personal Expense Tracker

A full-stack expense tracking web app built with Flask, SQLite, and Jinja2, as part of Day 13 of the VelTech summer internship curriculum.

## Features

- **Full CRUD**: Add, view, edit, and delete expenses
- **Dashboard**: Quick stats — total spend, record count, categories used, top category
- **Expense list**: Search by title and filter by category
- **Summary page**: Category-wise breakdown, highest expense, monthly trend, and Chart.js visualizations (doughnut + line chart)
- **Client-side form validation** with inline error messages
- **Confirmation prompt before delete**
- **Responsive nav bar with hamburger menu on mobile**
- **Dark mode toggle** (persisted via localStorage)

## Challenge tasks implemented (3 of the required 2)

1. Search expenses by title
2. Filter expenses by category
3. Expense charts using Chart.js (category doughnut chart + monthly trend line chart)
4. Dark mode

## Project Structure

```
PersonalExpenseTracker/
├── app.py                  # Flask app: routes, DB logic
├── expense.db               # SQLite database (auto-created, pre-seeded with sample data)
├── requirements.txt
├── templates/
│   ├── base.html            # Shared nav bar + footer layout
│   ├── index.html           # Dashboard
│   ├── add_expense.html     # Add expense form
│   ├── expenses.html        # List + search/filter
│   ├── edit_expense.html    # Edit form
│   └── summary.html         # Summary + charts
└── static/
    ├── css/style.css
    ├── js/script.js
    └── images/
```

## Database Schema

Table `expenses`:

| Column       | Type    |
|--------------|---------|
| id           | INTEGER PRIMARY KEY AUTOINCREMENT |
| title        | TEXT |
| amount       | REAL |
| category     | TEXT |
| payment_mode | TEXT |
| expense_date | TEXT |
| description  | TEXT |

## Routes

| Route             | Method   | Purpose                     |
|--------------------|----------|------------------------------|
| `/`                | GET      | Dashboard                   |
| `/add-expense`     | GET/POST | Add a new expense           |
| `/expenses`        | GET      | List all expenses (supports `?q=` search and `?category=` filter) |
| `/edit/<id>`       | GET/POST | Edit an expense             |
| `/delete/<id>`     | POST     | Delete an expense           |
| `/summary`         | GET      | Summary + charts            |

## Running the Project

```bash
pip install -r requirements.txt
python app.py
```

Then open: http://127.0.0.1:5000

The database is created automatically on first run (`init_db()`), and comes pre-seeded with 8 sample expenses so the dashboard and charts aren't empty on first load. Delete `expense.db` and restart to begin with a clean slate.
