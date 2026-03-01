import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("expenses.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_expense():
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date = datetime.now().strftime("%Y-%m-%d")

        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        conn.commit()
        conn.close()

        print("Expense added successfully!")

    except ValueError:
        print("Invalid amount entered.")

def view_expenses():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No expenses found.")

def delete_expense():
    expense_id = input("Enter expense ID to delete: ")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    print("Expense deleted (if ID existed).")

def total_expenses():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()

    print("Total spending:", total if total else 0)

def category_summary():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"{row[0]}: {row[1]}")
    else:
        print("No data available.")

def main():
    create_table()

    while True:
        print("\n1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Total Spending")
        print("5. Category Summary")
        print("6. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            total_expenses()
        elif choice == "5":
            category_summary()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()