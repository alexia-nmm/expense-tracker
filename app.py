import streamlit as st
import sqlite3 
import plotly.express as px 
from datetime import datetime
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

def get_category_totals():
     connection = connect_db()
     cursor = connection.cursor()

     cursor.execute("""
          SELECT category, SUM(amount) 
          FROM expenses 
          GROUP BY category
     """)
     category_totals = cursor.fetchall()
     connection.close()

     return category_totals

def get_monthly_totals():
     connection = connect_db()
     cursor = connection.cursor()

     cursor.execute("""
          SELECT strftime('%Y-%m', date) AS month, SUM(amount) 
          FROM expenses 
          GROUP BY month
          ORDER BY month
     """)
     monthly_totals = cursor.fetchall()
     connection.close()

     return monthly_totals

def get_current_month_total():
     connection = connect_db()
     cursor = connection.cursor()

     cursor.execute("""
     SELECT SUM(amount)
     FROM expenses
     WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
     """)

     current_month_total = cursor.fetchone()[0]
     connection.close()

     return current_month_total if current_month_total else 0.0

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
current_month_total= get_current_month_total()


if expenses:
    average_expense = total / len(expenses)
else:
     average_expense = 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
     label="Total Spent",
     value =f"${total:.2f}  ",
     border=True
    )
with col2:
    st.metric(
         label="Number of Expenses",
         value = len(expenses),
         border=True
    )
with col3:
    st.metric(
         label="Average Expense",
         value =f"${average_expense:.2f}",
         border=True
    )
with col4:
     st.metric(
          label= "This Month",
          value=f"${current_month_total:.2f}",
          border= True  
     )

category_totals = get_category_totals()

if category_totals:
     top_category = category_totals[0]
     for category in category_totals:
          if category[1] > top_category[1]:
               top_category = category
     st.info(
          f"Highest Spending Category: " 
          f"**{top_category[0]}** with $"
          f"**{top_category[1]}**"
     )
categories = ["Food", 
              "Transportation", 
              "Entertainment", 
              "Shopping",
              "Utilities", 
              "Health & Wellness",
              "Other"]

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
     with st.container(border =True, height=600):
          st.subheader("Spending by Category")
          category_totals = get_category_totals()
          if category_totals:
               category_chart = []
               amount_chart = []

               for category, total_amount in category_totals:
                    category_chart.append(category)
                    amount_chart.append(total_amount)

               fig = px.pie(
                    names=category_chart,
                    values=amount_chart,
                    hole=0.5
               )
               fig.update_traces(textinfo='percent', textposition="inside")
               fig.update_layout( height = 500,
                              margin=dict(t=10, b=50, l=10, r=10), 
                              showlegend=True,
                              legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                              annotations = [dict(text = f"<b>${total:.2f}</b><br>",
                                                       x=0.5, y=0.5, 
                                                       font_size=18,
                                                       font_color="black",
                                                       showarrow=False)]
               )

               st.plotly_chart(fig, use_container_width=True)
          else:
               st.info("No data found.")
with chart_col2:
    with st.container(border =True, height = 600):
          st.subheader("Monthly Spending")
          monthly_totals = get_monthly_totals()
          if monthly_totals:
               month_chart = []
               amount_chart = []

               for month, total_amount in monthly_totals:
                    formatted_month = datetime.strptime(month, "%Y-%m").strftime("%b %Y")
                    month_chart.append(formatted_month)
                    amount_chart.append(total_amount)

               monthly_fig = px.line(
                    x=month_chart,
                    y=amount_chart,
                    markers = True
               )
               monthly_fig.update_traces(marker=dict(size=8, color='blue'), line=dict(width=3))
               monthly_fig.update_layout(
                    height=500,
                    margin=dict(t=10, b=10, l=10, r=10),
                    xaxis_title="Month",
                    yaxis_title="Amount ($)",
               )
               st.plotly_chart(monthly_fig, use_container_width=True)
          else:
               st.info("No data found.")

tab1, tab2, tab3 = st.tabs(
    [" Add Expense", " Expenses",  " Manage Expenses"]
)
with tab1:
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

with tab2:
   st.subheader("Expenses")

   search_term = st.text_input(
   "Search by expense name",
   key="expense_search")  

   filter_categories =["All"]+categories

   selected_category = st.selectbox(
        "Filter by category",
        filter_categories,
        key ="expenses_category_filter"
   )
   filtered_expenses = filter_expenses(
        search_term,
        selected_category
     )
   
   filtered_total = 0
   for expense in filtered_expenses:
    filtered_total += expense[2]

   if filtered_expenses:
        expense_data=[]

        for expense in filtered_expenses:
             expense_data.append({
                  "ID": expense[0],
                  "Name": expense[1],
                  "Amount": expense[2],
                  "Category": expense[3],
                  "Date": expense[4]
             })
        st.metric(
          label="Filtered Total",
          value=f"${filtered_total:.2f}",
          border=True
          )
        st.dataframe(expense_data, use_container_width=True)
        st.caption(f"Showing {len(filtered_expenses)} expenses")
   else:
     st.info("No expenses found")


     


with tab3: 
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
