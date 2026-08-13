import streamlit as st
import sqlite3 
import plotly.express as px 
from datetime import datetime
import base64 

pixel_colors = [
    "#F06BA8",  # pink
    "#C89BE8",  # lavender
    "#8FC7F1",  # baby blue
    "#F6A6C1",  # light pink
    "#A8DDB5",  # mint
    "#F4C66A",  # soft yellow
]

st.markdown("""
<style>

/* ---------- PAGE ---------- */

.stApp {
    background-color: #FFF9EE;
}


/* ---------- HEADINGS ---------- */

h1, h2, h3 {
    color: #332744;
}

h1 {
    font-weight: 800;
}


/* ---------- METRIC CARDS ---------- */

.metric-card {
    background: #FFFDF7;
    border: 2px solid #E56A9F;
    border-radius: 6px;

    height: 125px;
    box-sizing: border-box;

    padding: 18px 14px;

    display: flex;
    flex-direction: column;
    justify-content: center;

    box-shadow: 5px 5px 0px #C99BE8;
}

.metric-label {
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    font-family: "Trebuchet MS", sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #E54F91;
    white-space: nowrap;
}
.metric-header {
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 38px;
}

.metric-icon {
    width: 28px;
    height: 28px;
    object-fit: contain;
    image-rendering: pixelated;
}

/* ---------- STREAMLIT CONTAINERS ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2px solid #E56A9F !important;
    border-radius: 6px !important;
    background-color: #FFFDF7 !important;
}


/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    background-color: #F9E1EE;
    border: 1px solid #E56A9F;
    border-radius: 4px 4px 0 0;
    padding: 10px 20px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #E978AA;
    color: white;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    background-color: #F8D7E7;
    color: #403747;

    border: 2px solid #D95691;
    border-radius: 4px;

    box-shadow: 3px 3px 0px #C99BE8;

    font-weight: 600;
}

.stButton > button:hover {
    background-color: #F3BDD6;
    border-color: #C94E85;
    color: #403747;
}


/* ---------- INPUTS ---------- */

input {
    border-radius: 4px !important;
}
/* Numeric/date input values */
input[type="number"],
input[type="date"] {
    font-family: "Trebuchet MS", sans-serif !important;
}
input {
    font-family: "Trebuchet MS", sans-serif !important;
}


/* ---------- PIXEL DIVIDER ---------- */

.pixel-divider {
    color: #E56A9F;
    letter-spacing: 8px;
    text-align: center;
    margin: 10px 0 20px 0;
}


/* ---------- RETRO SECTION TITLE ---------- */

.retro-window-title {
    background: #F6C8DA;
    border: 2px solid #D95691;
    padding: 7px 10px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    font-weight: 700;
    color: #332744;

    border-radius: 4px 4px 0 0;
}

.window-controls {
    display: flex;
    gap: 5px;
}

.window-controls span {
    width: 18px;
    height: 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid #A94B78;
    background: #FFF9EE;

    font-size: 11px;
    line-height: 1;
}

.manager-icons {
    display: flex;
    gap: 18px;
    width: 100%;
}

.manager-link {
    flex: 1;
    text-decoration: none !important;
    color: inherit !important;
}

.manager-item {
    width: 100%;
    box-sizing: border-box;

    background: #FFFDF7;
    border: 2px solid #E56A9F;
    box-shadow: 5px 5px 0px #C99BE8;

    padding: 14px;

    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;

    cursor: pointer;
    transition: transform 0.1s ease;
}

.manager-item:hover {
    background: #FDECF3;
    transform: translate(-2px, -2px);
}

.manager-icon {
    width: 34px;
    height: 34px;
    object-fit: contain;
    image-rendering: pixelated;
}
.manager-item.active {
    background-color: #F7D5E5;
    border-color: #C94E85;
    box-shadow: 3px 3px 0px #B68AD8;
}

.manager-item.active span {
    color: #C94E85;
}

.form-title {
    display: flex;
    align-items: center;
    gap: 10px;

    font-size: 24px;
    font-weight: 700;
    color: #332744;

    margin-bottom: 18px;
}

.form-title-icon {
    width: 38px;
    height: 38px;
    object-fit: contain;
    image-rendering: pixelated;
}
.section-window {
    background: #FFFDF7;
    border: 2px solid #D95691;
    box-shadow: 5px 5px 0px #C99BE8;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 18px;
}

.section-title {
    background: #F7CADA;
    border-bottom: 2px solid #D95691;
    padding: 9px 12px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    font-weight: 700;
    color: #332744;
}

.section-body {
    padding: 18px;
}

.section-controls {
    display: flex;
    gap: 5px;
}

.section-controls span {
    border: 1px solid #A94B78;
    background: #FFF9EE;
    width: 17px;
    height: 17px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 10px;
}

.section-description {
    color: #756779;
    margin-bottom: 15px;
    font-size: 14px;
}

.mini-stat-card {
    background: #FFFDF7;
    border: 2px solid #E56A9F;
    border-radius: 5px;
    padding: 14px 16px;
    box-shadow: 3px 3px 0px #C99BE8;
    margin-bottom: 12px;
}

.mini-stat-label {
    font-family: "Pixelify Sans", sans-serif;
    font-size: 14px;
    color: #66556E;
    margin-bottom: 6px;
}

.mini-stat-value {
    font-family: "Trebuchet MS", sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #E54F91;
}
/* ---------- DATAFRAME ---------- */
[data-testid="stDataFrame"] [role="columnheader"] {
    background-color: #F7CADA !important;
    color: #332744 !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #D95691 !important;

</style>
""", unsafe_allow_html=True)
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.title("Expense Tracker")
    st.write("Track your spending ♡")

with header_col2:
    st.image(
        "assets/pixel_cat.jpg",
        width=120
    )
st.markdown(
    '<div class="pixel-divider">✦─── ───── ───── ♡ ───── ───── ───✦</div>',
    unsafe_allow_html=True
)

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

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    return encoded_image
    
expenses = get_expenses()
total = calculate_total()
current_month_total= get_current_month_total()


if expenses:
    average_expense = total / len(expenses)
else:
     average_expense = 0

money_icon = get_image_base64("assets/pixel_money.jpeg")
calendar_icon = get_image_base64("assets/calendar.jpeg")
coin_icon = get_image_base64("assets/pixel_mon.JPG")
hourglass_icon = get_image_base64("assets/pixel_hourglas.jpeg")

add_icon = get_image_base64("assets/Add.JPG")
expenses_icon = get_image_base64("assets/Expenses.JPG")
manage_icon = get_image_base64("assets/Manage.JPG")

st.markdown("✦ Dashboard Overview")


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.html(
        f"""
<div class="metric-card">

     <div class="metric-header">
          <img
               src="data:image/jpeg;base64,{money_icon}"
               class="metric-icon"
          >
          <span class="metric-label">
               Total Spent
          </span>
     </div>

     <div class="metric-value">
          ${total:.2f}
     </div>

</div>
"""
    )
with col2:
     st.html(
        f"""
<div class="metric-card">
    <div class="metric-header">
        <img
            src="data:image/jpeg;base64,{calendar_icon}"
            class="metric-icon"
        >
        <span class="metric-label">Number of Expenses</span>
    </div>

    <div class="metric-value">
        {len(expenses)}
    </div>
</div>
"""
    )

with col3:
     st.html(
        f"""
<div class="metric-card">
    <div class="metric-header">
        <img
            src="data:image/jpeg;base64,{coin_icon}"
            class="metric-icon"
        >
        <span class="metric-label">Average Expense</span>
    </div>

    <div class="metric-value">
        ${average_expense:.2f}
    </div>
</div>
"""
    )

with col4:
    st.html(
        f"""
<div class="metric-card">
    <div class="metric-header">
        <img
            src="data:image/jpeg;base64,{hourglass_icon}"
            class="metric-icon"
        >
        <span class="metric-label">This Month</span>
    </div>

    <div class="metric-value">
        ${current_month_total:.2f}
    </div>
</div>
"""
    )

category_totals = get_category_totals()

if category_totals:
     top_category = category_totals[0]
     for category in category_totals:
          if category[1] > top_category[1]:
               top_category = category
     
     st.markdown(
        f"""
        <div style="
            background-color:#F6E8F3;
            padding:14px 18px;
            border-radius:12px;
            border:2px solid #F06BA8;
            margin-top:10px;
            margin-bottom:20px;
        ">
            ✦ Your highest spending category is
            <b>{top_category[0]}</b> with
            <b>${top_category[1]:.2f}</b> spent.
        </div>
        """,
        unsafe_allow_html=True
    )
categories = ["Food", 
              "Transportation", 
              "Entertainment", 
              "Shopping",
              "Utilities", 
              "Health & Wellness",
              "Other"]

st.markdown("✦ Spending Insights")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
     st.html("""
<div class="retro-window-title">
    <span>✦ Spending by Category</span>

    <div class="window-controls">
        <span>─</span>
        <span>□</span>
        <span>×</span>
    </div>
</div>
""")
     with st.container(border =True, height=600):
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
                    hole=0.5,
                    color_discrete_sequence=pixel_colors
               )
               fig.update_traces(textinfo='percent', textposition="inside", textfont=dict(family="Trebuchet MS", size=14))
               fig.update_layout( height = 500,
                              margin=dict(t=10, b=50, l=10, r=10), 
                              showlegend=True,
                              legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                              annotations = [dict(text = f"<b>${total:.2f}</b><br>",
                                                       x=0.5, y=0.5, 
                                                       font_size=18,
                                                       font_color="black",
                                                       showarrow=False,
                                                       font=dict(
                                                       family="Trebuchet MS",
                                                                      size=18,
                                                                      color="#403747"
                                                                 ))]
               )

               st.plotly_chart(fig, use_container_width=True)
          else:
               st.info("No data found.")
with chart_col2:
     st.html("""
<div class="retro-window-title">
    <span>✦ Monthly Spending</span>

    <div class="window-controls">
        <span>─</span>
        <span>□</span>
        <span>×</span>
    </div>
</div>
""")
     with st.container(border =True, height = 600):
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
                    markers = True,
                    color_discrete_sequence=[pixel_colors[0]]
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

st.markdown("✦ Expense Manager")
active_section = st.query_params.get("section", "add")
add_class = "active" if active_section == "add" else ""
expenses_class = "active" if active_section == "expenses" else ""
manage_class = "active" if active_section == "manage" else ""
st.html(
    f"""
<div class="manager-icons">

    <a href="?section=add" target="_self" class="manager-link">
        <div class="manager-item {add_class}">
            <img
                src="data:image/jpeg;base64,{add_icon}"
                class="manager-icon"
            >
            <span>Add Expense</span>
        </div>
    </a>

    <a href="?section=expenses" target="_self" class="manager-link">
        <div class="manager-item {expenses_class}">
            <img
                src="data:image/jpeg;base64,{expenses_icon}"
                class="manager-icon"
            >
            <span>Expenses</span>
        </div>
    </a>

    <a href="?section=manage" target="_self" class="manager-link">
        <div class="manager-item {manage_class}">
            <img
                src="data:image/jpeg;base64,{manage_icon}"
                class="manager-icon"
            >
            <span>Manage</span>
        </div>
    </a>

</div>
"""
)


if active_section == "add":
    st.html("""
<div class="retro-window-title">
    <span>✦ Add New Expense</span>
    <div class="window-controls">
        <span>─</span>
        <span>□</span>
        <span>×</span>
    </div>
</div>
""")
    with st.container(border=True):
        st.caption("Add a new expense to your tracker ♡")
        expense_name = st.text_input("Expense Name",  placeholder="e.g. Groceries")
        expense_amount = st.number_input("Amount", 
                                        min_value=0.01, 
                                        step=0.01)
        expense_category = st.selectbox("Category", categories)
        expense_date = st.date_input("Date")
        if st.button("Add Expense", use_container_width=True):
          if not expense_name.strip():
               st.error("Please enter a valid expense name.")
          else:
               add_expense(expense_name, expense_amount, expense_category, expense_date)
               st.session_state["toast_message"] = (
                    "Expense added successfully!"
                ) 
               st.rerun()


elif active_section == "expenses":
     st.html("""
<div class="retro-window-title">
    <span>✦ Expenses</span>
    <div class="window-controls">
        <span>─</span>
        <span>□</span>
        <span>×</span>
    </div>
</div>
""")
     with st.container(border=True):

        st.caption("Search and explore your spending history ♡")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            search_term = st.text_input(
                "Search by expense name",
                key="expense_search",
                placeholder="Search..."
            )

        with filter_col2:
            filter_categories = ["All"] + categories

            selected_category = st.selectbox(
                "Filter by category",
                filter_categories,
                key="expenses_category_filter"
            )

        filtered_expenses = filter_expenses(
            search_term,
            selected_category
        )

        filtered_total = 0

        for expense in filtered_expenses:
            filtered_total += expense[2]

        if filtered_expenses:

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:
                 st.html(
        f"""
<div class="mini-stat-card">
    <div class="mini-stat-label">Filtered Total</div>
    <div class="mini-stat-value">${filtered_total:.2f}</div>
</div>
"""
    )

            with summary_col2:
              st.html(
        f"""
<div class="mini-stat-card">
    <div class="mini-stat-label">Results</div>
    <div class="mini-stat-value">{len(filtered_expenses)}</div>
</div>
"""
    )  

            expense_data = []

            for expense in filtered_expenses:
                expense_data.append({
                    "ID": expense[0],
                    "Name": expense[1],
                    "Amount": expense[2],
                    "Category": expense[3],
                    "Date": expense[4]
                })

            st.dataframe(
                expense_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn(
                         "ID",
                         width="small"
                    ),

                    "Name": st.column_config.TextColumn(
                         "Expense",
                         width="medium"
                    ),

                    "Amount": st.column_config.NumberColumn(
                         "Amount",
                         format="$%.2f"
                    ),

                    "Category": st.column_config.TextColumn(
                         "Category",
                         width="medium"
                    ),

                    "Date": st.column_config.DateColumn(
                         "Date",
                         format="MMM DD, YYYY"
                    )}
               )

        else:
            st.info("No expenses found.")

elif active_section == "manage":
    
    st.html("""
<div class="retro-window-title">
    <span>✦ Manage Expenses</span>
    <div class="window-controls">
        <span>─</span>
        <span>□</span>
        <span>×</span>
    </div>
</div>
""")

    with st.container(border=True):

        st.caption("Edit or remove an existing expense ♡")

        if "toast_message" in st.session_state:
            st.toast(st.session_state["toast_message"])
            del st.session_state["toast_message"]

        if expenses:

            expense_options = {
                expense[0]: f"{expense[1]} - ${expense[2]:.2f}"
                for expense in expenses
            }

            manage_col1, manage_col2 = st.columns(2)

            with manage_col1:
                selected_expense_id = st.selectbox(
                    "Select an expense",
                    options=expense_options.keys(),
                    format_func=lambda x: expense_options[x]
                )

            selected_expense = next(
                expense for expense in expenses
                if expense[0] == selected_expense_id
            )

            with manage_col2:
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
