from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "expense-tracker-secret-key"

DB_NAME = "expense.db"

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Education", "Health", "Others"]
PAYMENT_MODES = ["Cash", "UPI", "Debit Card", "Credit Card", "Net Banking"]


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            payment_mode TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    total_expenses = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses").fetchone()["total"]
    total_count = conn.execute("SELECT COUNT(*) AS count FROM expenses").fetchone()["count"]
    category_count = conn.execute("SELECT COUNT(DISTINCT category) AS c FROM expenses").fetchone()["c"]
    recent_expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC LIMIT 5"
    ).fetchall()
    top_category_row = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC LIMIT 1"
    ).fetchone()
    top_category = top_category_row["category"] if top_category_row else "N/A"
    conn.close()
    return render_template(
        "index.html",
        total_expenses=total_expenses,
        total_count=total_count,
        category_count=category_count,
        recent_expenses=recent_expenses,
        top_category=top_category,
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        payment_mode = request.form.get("payment_mode", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not amount or not category or not payment_mode or not expense_date:
            flash("Please fill in all required fields.", "error")
            return render_template(
                "add_expense.html", categories=CATEGORIES, payment_modes=PAYMENT_MODES, form=request.form
            )

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number.", "error")
            return render_template(
                "add_expense.html", categories=CATEGORIES, payment_modes=PAYMENT_MODES, form=request.form
            )

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (title, amount, category, payment_mode, expense_date, description) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (title, amount, category, payment_mode, expense_date, description),
        )
        conn.commit()
        conn.close()
        flash("Expense added successfully!", "success")
        return redirect(url_for("expenses"))

    return render_template("add_expense.html", categories=CATEGORIES, payment_modes=PAYMENT_MODES, form={})


@app.route("/expenses")
def expenses():
    search_query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "").strip()

    conn = get_db_connection()
    sql = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if search_query:
        sql += " AND title LIKE ?"
        params.append(f"%{search_query}%")

    if category_filter:
        sql += " AND category = ?"
        params.append(category_filter)

    sql += " ORDER BY expense_date DESC, id DESC"

    all_expenses = conn.execute(sql, params).fetchall()
    conn.close()

    return render_template(
        "expenses.html",
        expenses=all_expenses,
        categories=CATEGORIES,
        search_query=search_query,
        category_filter=category_filter,
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    conn = get_db_connection()
    expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (id,)).fetchone()

    if expense is None:
        conn.close()
        flash("Expense not found.", "error")
        return redirect(url_for("expenses"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        payment_mode = request.form.get("payment_mode", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not amount or not category or not payment_mode or not expense_date:
            flash("Please fill in all required fields.", "error")
            conn.close()
            return render_template(
                "edit_expense.html", expense=expense, categories=CATEGORIES, payment_modes=PAYMENT_MODES
            )

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number.", "error")
            conn.close()
            return render_template(
                "edit_expense.html", expense=expense, categories=CATEGORIES, payment_modes=PAYMENT_MODES
            )

        conn.execute(
            "UPDATE expenses SET title = ?, amount = ?, category = ?, payment_mode = ?, "
            "expense_date = ?, description = ? WHERE id = ?",
            (title, amount, category, payment_mode, expense_date, description, id),
        )
        conn.commit()
        conn.close()
        flash("Expense updated successfully!", "success")
        return redirect(url_for("expenses"))

    conn.close()
    return render_template("edit_expense.html", expense=expense, categories=CATEGORIES, payment_modes=PAYMENT_MODES)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("expenses"))


@app.route("/summary")
def summary():
    conn = get_db_connection()

    total_expenses = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses").fetchone()["total"]

    category_summary = conn.execute(
        "SELECT category, COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total "
        "FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()

    highest_expense = conn.execute(
        "SELECT * FROM expenses ORDER BY amount DESC LIMIT 1"
    ).fetchone()

    recent_expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC LIMIT 5"
    ).fetchall()

    monthly_summary = conn.execute(
        "SELECT strftime('%Y-%m', expense_date) AS month, COALESCE(SUM(amount), 0) AS total "
        "FROM expenses GROUP BY month ORDER BY month"
    ).fetchall()

    conn.close()

    chart_labels = [row["category"] for row in category_summary]
    chart_values = [row["total"] for row in category_summary]
    month_labels = [row["month"] for row in monthly_summary]
    month_values = [row["total"] for row in monthly_summary]

    return render_template(
        "summary.html",
        total_expenses=total_expenses,
        category_summary=category_summary,
        highest_expense=highest_expense,
        recent_expenses=recent_expenses,
        chart_labels=chart_labels,
        chart_values=chart_values,
        month_labels=month_labels,
        month_values=month_values,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
