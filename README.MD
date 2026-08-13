#  Expense Tracker

A personal expense tracking dashboard built with **Python, Streamlit, SQLite, and Plotly**.

The application allows users to add, search, edit, and delete expenses while providing visual summaries of their spending through an interactive dashboard.

I originally started this project as a command-line Python application and gradually expanded it into a full Streamlit dashboard. The project helped me practice database management, CRUD operations, data visualization, application state, and UI design.

##  Features

- Add expenses with a name, amount, category, and date
- View and search expense history
- Filter expenses by category
- Edit existing expenses
- Delete expenses
- Track total spending
- View average expense amount
- Track current-month spending
- View spending by category with an interactive donut chart
- View monthly spending trends
- Interactive navigation between expense management sections
- Custom retro/pixel-inspired dashboard theme

##  Tech Tools

- **Python** — application logic
- **Streamlit** — web application and user interface
- **SQLite** — local expense storage
- **Plotly** — interactive data visualizations
- **HTML/CSS** — custom dashboard styling
- **Git & GitHub** — version control

##  Dashboard

The dashboard provides a quick overview of spending, including:

- Total amount spent
- Number of expenses
- Average expense
- Current month spending
- Spending distribution by category
- Monthly spending trends

##  Data Storage

The current version uses **SQLite** for local data storage.

This project is currently designed primarily as a personal/portfolio demo rather than a production multi-user financial application.

##  Demo & Privacy Notice

This application is a **portfolio and educational project**.

The deployed version should only be used with sample or non-sensitive data. It is not intended to store private, confidential, banking, or other sensitive financial information.

The current version does not provide individual user accounts or isolated storage for multiple users. Future versions may include authentication and per-user cloud database storage.

##  Run Locally

Clone the repository:

```bash
git clone https://github.com/alexia-nmm/expense-tracker.git
```

Move into the project directory:

```bash
cd expense-tracker
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

##  Future Improvements

Some features I would like to explore in future versions include:

- User authentication
- Individual user accounts
- Secure cloud database storage
- Per-user expense isolation
- Budget tracking
- Spending goals
- Additional spending analytics
- Exporting expense reports
- Improve UI/UX design

##  Project Purpose

I built this project to strengthen my Python development skills while learning how to take a simple command-line program and turn it into an interactive application.

Throughout the project, I worked with SQLite queries, CRUD operations, Streamlit session state, interactive Plotly charts, filtering, application navigation, and custom UI styling.

