
from multiprocessing import connection
import os
import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("expenses.db")
def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def add_expense_to_db(expense):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses(name,amount,category,date)
        Values (?,?,?,?)
        """,(
            expense["name"],
            expense["amount"],
            expense["category"],    
            expense["date"]
        ))
    connection.commit()
    connection.close()


categories={
    "1": "Food",
    "2": "Transportation",
    "3": "Entertainment",
    "4": "Shopping",
    "5": "Other"
}

def add_expense():
    expense_name = input("Enter expense name: ")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                print("Expense amount cannot be zero or negative. Please enter a valid amount.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        print("\n Select expense category:")
        for key, value in categories.items():
            print(f"{key}. {value}")
        category_choice = input("Enter your choice (1-5): ")  

        if category_choice in categories:
            expense_category = categories[category_choice]
            break
        print("Invalid choice. Please try again.")      

    expense_date= datetime.now().strftime("%Y-%m-%d")
    expense ={
        "name" : expense_name,
        "amount": expense_amount,
        "category": expense_category,
        "date": expense_date
    }
    add_expense_to_db(expense)
    print(f"Expense '{expense_name}' of ${expense_amount: .2f}' added successfully.")

def view_expenses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses_from_db = cursor.fetchall()
    connection.close()
    if not expenses_from_db:
        print("No records found.")
    else:
        print("Expenses:")
        for expense in expenses_from_db:
            print(
                f"- {expense[1]} : ${expense[2]:.2f}"
                f"| Category: {expense[3]}"
                f"| Date: {expense[4]}"
            )

def calculate_total_expenses():
    connection = connect_db()
    cursor= connection.cursor()

    cursor.execute("SELECT SUM (amount) FROM expenses")
    total_expenses = cursor.fetchone()[0]
    connection.close()

    if total_expenses is None:
        total_expenses = 0
    print(f"Total expenses: ${total_expenses: .2f}")
    

def view_by_category():
    
    while True:
        print("Choose a category:")
        for key, value in categories.items():
            print(f"{key}. {value}")

        category_choice = input("category(1-5):")
        if category_choice in categories:
            selected_category = categories[category_choice]
            break
        print("Invalid choice. Please try again.")

    connection = connect_db()
    cursor = connection.cursor()
        
    cursor.execute("" \
        "SELECT * " \
        "FROM expenses " \
        "WHERE category = ?", (selected_category,))
    expenses_from_db = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (selected_category,))
    category_total = cursor.fetchone()[0]

    connection.close()
    print(f"\n{selected_category} Expenses:")
    if not expenses_from_db:
        print(f"No expenses found for this category.")  
        category_total = 0
    else:
        for expense in expenses_from_db:
            print(
                f"\n- {expense[1]} : ${expense[2]:.2f}"
                f"| Date: {expense[4]}"
            )

    print(f"\nTotal {selected_category} expenses: ${category_total:.2f}")

     

def view_by_date():
    selected_date = input("Enter date(YYYY-MM-DD):")

    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name, amount, category, date FROM expenses WHERE date = ?", (selected_date,))

    expenses_from_db = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date = ?", (selected_date,))
    date_total = cursor.fetchone()[0]
    connection.close()

    print(f"\nExpenses on {selected_date}:")
    if not expenses_from_db:
        print(f"No expenses found for this date.")
        date_total = 0
    else:
        for expense in expenses_from_db:
            print(
                f"\n- {expense[0]} : ${expense[1]:.2f}"
                f"| Category: {expense[2]}"
            )
    print(f"\nTotal expenses for {selected_date}: ${date_total:.2f}")


def view_by_month():
    while True:
        selected_month = input("Enter month(YYYY-MM):")
        try:
            datetime.strptime(selected_month, "%Y-%m")
            break
        except ValueError:
            print("Invalid month format. Please enter in YYYY-MM format.")

    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name, amount, category, date FROM expenses WHERE date LIKE ?", (f"{selected_month}%",))
    expenses_from_db = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (f"{selected_month}%",))
    month_total = cursor.fetchone()[0]
    connection.close()

    print(f"\nExpenses for {selected_month}:")

    if not expenses_from_db:
        print(f"No expenses found for this month.")
        month_total = 0
    else:
        for expense in expenses_from_db:
            print(
                f"\n- {expense[0]} : ${expense[1]:.2f}"
                f"| Category: {expense[2]}"
                f"| Date: {expense[3]}"
            )
    print(f"\nTotal expenses for {selected_month}: ${month_total:.2f}")

    

def search_expenses():
    search_term = input("Enter expense name to search: ")
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name, amount, category, date FROM expenses WHERE name LIKE ?", (f"%{search_term}%",))
    expenses_from_db = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE name LIKE ?", (f"%{search_term}%",))
    search_total = cursor.fetchone()[0]

    connection.close()

    print(f"\nSearch results for '{search_term}':")

    if not expenses_from_db:
        print(f"No expenses found matching '{search_term}'.")
        search_total = 0
    else:
        for expense in expenses_from_db:
            print(
                f"\n- {expense[0]} : ${expense[1]:.2f}"
                f"| Category: {expense[2]}"
                f"| Date: {expense[3]}"
            )
    print(f"\nTotal : ${search_total:.2f}")

def expense_summary():

    conection = connect_db()
    cursor = conection.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY category")
    category_totals = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    overall_total = cursor.fetchone()[0]
    conection.close()
    print("\nExpense Summary")
    print("-------------------------")
    if not category_totals:
        print("No expenses found.")
        overall_total = 0
    else:
        for category, total in category_totals:
            print(f"{category}: ${total:.2f}")
    print("-------------------------")
    print(f"Total: ${overall_total:.2f}")

def edit_expense():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, amount, category, date FROM expenses")
    expenses_from_db = cursor.fetchall()

    if not expenses_from_db:
        print("No expenses found to edit.")
        connection.close()
        return

    print("Expenses:")
    for expense in expenses_from_db:
        print(
            f"ID: {expense[0]} | Name: {expense[1]} | Amount: ${expense[2]:.2f} | "
            f"Category: {expense[3]} | Date: {expense[4]}"
        )

    try:
        expense_id = int(input("Enter the ID of the expense to edit: "))  
    except ValueError:
        print("Invalid ID. Please enter a valid number.")
        connection.close()
        return

    cursor.execute("SELECT name, amount, category, date FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()

    if expense is None:
        print(f"No expense found with ID {expense_id}.")
        connection.close()
        return

    print("\n Editing Expense: ")
    new_name = input(f"Enter expense name [{expense[0]}]: ")

    while True:
        try:
            new_amount = float(input(f"Enter expense amount [{expense[1]}]: "))
            if new_amount < 0:
                print("Expense amount cannot be negative. Please enter a valid amount.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        print("\n Select expense category:")
        for key, value in categories.items():
            print(f"{key}. {value}")
        new_category = input(f"Enter your choice (1-5) [{expense[2]}]: ")  

        if new_category in categories:
            new_category = categories[new_category]
            break
        elif new_category == "":
            new_category = expense[2]  # Keep the existing category if no input is provided
            break
        print("Invalid choice. Please try again.")

    

    cursor.execute("""
        UPDATE expenses
        SET name = ?, amount = ?, category = ?
        WHERE id = ?
    """, (new_name, new_amount, new_category, expense_id))
    connection.commit()
    connection.close()
    print("Expense updated successfully!")


def delete_expense():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, amount, category, date FROM expenses")
    expenses_from_db = cursor.fetchall()

    if not expenses_from_db:
        print("No expenses found to delete.")
        connection.close()
        return

    print("Expenses:")
    for expense in expenses_from_db:
        print(
            f"ID: {expense[0]} | Name: {expense[1]} | Amount: ${expense[2]:.2f} | "
            f"Category: {expense[3]} | Date: {expense[4]}"
        )

    while True:
        try:
            expense_id = int(input("Enter the ID of the expense to delete: "))
            break
        except ValueError:
            print("Invalid ID. Please enter a valid number.")

    cursor.execute("SELECT name, amount, category, date FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()

    if expense is None:
        print(f"No expense found with ID {expense_id}.")
        connection.close()
        return

    print("\nDeleting Expense:")
    print(f"Name: {expense[0]} | Amount: ${expense[1]:.2f} | Category: {expense[2]} | Date: {expense[3]}")

    while True:
        confirmation = input("Are you sure you want to delete this expense? (y/n): ").lower()
        if confirmation == "y":
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            connection.commit()
            print("Expense deleted successfully!")
            break
        elif confirmation == "n":
            print("Deletion canceled.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    connection.close()


create_table()
while True:
    print("================================")
    print("         Expense tracker")
    print("================================")

    print("1. Add expense")
    print("2. View expenses")
    print("3. Calculate total expenses")
    print("4. View by Category")
    print("5. View by Date")
    print("6. View by Month")
    print("7. Search expenses")
    print("8. Expense summary")
    print("9. Edit Expense")
    print("10. Delete Expense")
    print("11. Exit")

    choice = input("Enter your choice (1-11): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        calculate_total_expenses()
    elif choice == "4":
        view_by_category()
    elif choice == "5":
        view_by_date()
    elif choice == "6":
        view_by_month()
    elif choice == "7":
        search_expenses()
    elif choice == "8":
        expense_summary()
    elif choice == "9":
        edit_expense()
    elif choice == "10":
        delete_expense()
    elif choice == "11":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
