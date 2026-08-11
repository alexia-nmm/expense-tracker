import streamlit as st
import sqlite3 

st.title("Expense Tracker")
st.write("Welcome to the Expense Tracker app!")


def connect_db():
     return sqlite3.connect("expenses.db")

def get_expenses():
     connection = connect_db()
     cursor = connection.cursor()   

     cursor.execute("SELECT * FROM expenses")

     expenses = cursor.fetchall()
     connection.close()
    
     return expenses

def calculate_total():
     connection = connect_db()
     cursor = connection.cursor()

     cursor.execute("SELECT SUM(amount) FROM expenses")
     total = cursor.fetchone()[0]
     connection.close()

     return total if total else 0.0

def add_expense(name, amount, category, date):
     connection = connect_db()
     cursor = connection.cursor()

     cursor.execute("""
          INSERT INTO expenses (name, amount, category, date)
          VALUES (?, ?, ?, ?)
     """, (name, amount, category, date))
     connection.commit()
     connection.close()

def update_expense(expense_id, name, amount, category, date):
     connection = connect_db()
     cursor = connection.cursor()
     cursor.execute("""
          UPDATE expenses
          SET name =?, amount =?, category =?, date =?
          WHERE id =?
          """, (name, amount, category, date, expense_id))
     connection.commit()
     connection.close()

def delete_expense(expense_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE id =?", (expense_id,))
    connection.commit()
    connection.close()

def filter_expenses(search_term, category):
     connection = connect_db()
     cursor = connection.cursor()

     query = """
        SELECT * FROM expenses
        WHERE name LIKE ? """
     parameters = [f"%{search_term}%"]
     if category != "All":
          query += "AND category =?"
          parameters.append(category)
     cursor.execute(query, parameters)
     expenses = cursor.fetchall()
     connection.close()
     return expenses
    
expenses = get_expenses()
total = calculate_total()

col1, col2 = st.columns(2)
with col1:
    st.metric(
     label="Total Spent",
     value =f"${total:.2f}  "
    )
with col2:
    st.metric(
         label="Number of Expenses",
         value = len(expenses)
    )

categories = ["Food", 
              "Transportation", 
              "Entertainment", 
              "Shopping",
              "Utilities", 
              "Health & Wellness",
              "Other"]


st.subheader("Add New Expense")
expense_name = st.text_input("Expense Name")
expense_amount = st.number_input("Amount", 
                                 min_value=0.01, 
                                 step=0.01)

expense_category = st.selectbox("Category", categories)
expense_date = st.date_input("Date")

if st.button("Add Expense"):
     if not expense_name.strip():
          st.error("Please enter a valid expense name.")
     else:
          add_expense(expense_name, expense_amount, expense_category, expense_date)
          st.success("Expense added successfully!")
          st.rerun()


st.subheader("Search & Filter")
search_term = st.text_input("Search by Name")
filter_categories = ["All"] + categories
selected_category = st.selectbox("Filter by category", filter_categories)


if search_term.strip() or selected_category != "All":
    filtered_expenses = filter_expenses(search_term, selected_category)

    if filtered_expenses:
        expense_data = []
        for expense in filtered_expenses:
            expense_data.append({
               "ID": expense[0],
               "Name": expense[1],  
               "Amount": expense[2],
               "Category": expense[3],
               "Date": expense[4]
            })
        st.subheader("Search Results")
        st.dataframe(expense_data, use_container_width=True)
    else:
        st.info("No expenses found.")


st.subheader("Your Expenses")
if expenses:
     expense_data = []
     for expense in expenses:
          expense_data.append({
               "ID": expense[0],
               "Name": expense[1],  
               "Amount": expense[2],
               "Category": expense[3],
               "Date": expense[4]
          })
     st.dataframe(expense_data, use_container_width=True)

else:
     st.info("No expenses found.")

st.subheader("Manage Expenses")

if "toast_message" in st.session_state:
    st.toast(st.session_state["toast_message"])
    del st.session_state["toast_message"]


if expenses:
    
    expense_options= {
         expense[0]: f"{expense[1]} - ${expense[2]:.2f}"
         for expense in expenses
    }
    selected_expense_id = st.selectbox(
         "Select an expense",
         options=expense_options.keys(), 
         format_func = lambda x: expense_options[x] )

    selected_expense = next(
         expense for expense in expenses 
         if expense[0] == selected_expense_id
    )
    action = st.selectbox(
         "Choose an action",
         ["Edit", "Delete"]
    )

    if action == "Edit":
         edit_name = st.text_input(
              "Expense Name",
              value=selected_expense[1])
         edit_amount = st.number_input(
              "Amount",
               min_value=0.01,
               value = float(selected_expense[2]),
               step=0.01,)
         edit_category = st.selectbox(
              "Category", 
              categories, 
              index=categories.index(selected_expense[3]),
              key = "edit_category")
         edit_date = st.date_input(
             "Date",
             value=selected_expense[4])
         if st.button("Update Expense"):
            if not edit_name.strip():
               st.error("Please enter a valid expense name.")
            else:
                update_expense(
                   selected_expense_id, 
                   edit_name, 
                   edit_amount, 
                   edit_category, 
                   edit_date)
                st.session_state["toast_message"] = ("Expense updated successfully!")
                st.rerun()

    elif action == "Delete":
        st.warning("You are about to delete: "f"{selected_expense[1]} - ${selected_expense[2]:.2f}")
        st.write("Are you sure you want to proceed?")

        if st.button("Delete Expense"):
            delete_expense(selected_expense_id)
            st.session_state["toast_message"] = ("Expense deleted successfully!")
            st.rerun()
            
else:
    st.info("No expenses available to manage.")
