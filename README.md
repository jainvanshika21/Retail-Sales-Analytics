# 📊 Retail Sales Intelligence Dashboard

An end-to-end Data Analytics project that transforms raw retail sales data into actionable business insights using **Python, MySQL, Power BI, and Streamlit**.

The project demonstrates the complete analytics workflow, including data cleaning, exploratory data analysis (EDA), SQL-based business analysis, interactive dashboards, and web application development.

---

## 🚀 Project Overview

This project analyzes retail sales data to identify sales trends, customer behavior, regional performance, and product profitability through interactive visualizations and dashboards.

The project covers the complete data analytics lifecycle:

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- SQL Analysis
- Business Intelligence Dashboard
- Interactive Web Application

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data Cleaning & Analysis |
| Pandas | Data Manipulation |
| NumPy | Numerical Operations |
| Plotly | Interactive Visualizations |
| Matplotlib | Data Visualization |
| MySQL | Data Storage & SQL Analysis |
| SQLAlchemy | Python-MySQL Connection |
| Power BI | Interactive Dashboard |
| Streamlit | Web Application |
| Git & GitHub | Version Control |

---

## 📂 Project Structure

```
Retail-Sales-Analytics/
│
├── data/
│   ├── retail_sales.csv
│   └── cleaned_sales_data.csv
│
├── notebooks/
│   ├── 01_Data_Cleaning_EDA.ipynb
│   └── 02_SQL_Data_Export.ipynb
│
├── sql/
│   └── sales_analysis.sql
│
├── powerbi/
│   └── Retail_Sales_Dashboard.pbix
│
├── streamlit/
│   └── app.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📊 Dataset

The dataset contains retail sales transactions with information such as:

- Order Date
- Customer Details
- Product Details
- Sales Channel
- Region & State
- Revenue
- Profit
- Quantity Sold

---

# 🐍 Python Workflow

The Python notebook performs:

- Data Loading
- Data Cleaning
- Missing Value Handling
- Duplicate Removal
- Data Type Conversion
- Feature Engineering
- Exploratory Data Analysis
- Data Visualization
- Export Clean Dataset

### Feature Engineering

Created additional features including:

- Year
- Quarter
- Month
- Weekday
- Week Number

---

# 🗄️ SQL Analysis

The cleaned dataset is exported to MySQL for business analysis.

The SQL script includes **45 analytical queries**, covering:

- Revenue Analysis
- Profit Analysis
- Customer Analysis
- Product Analysis
- Regional Analysis
- Monthly Sales Trends
- Window Functions
- Ranking Functions
- Running Totals
- Common Table Expressions (CTEs)

---

# 📈 Power BI Dashboard

The Power BI report contains three interactive dashboards:

### Dashboard 1 – Executive Overview

- KPI Cards
- Monthly Revenue Trend
- Monthly Profit Trend
- Sales Overview

### Dashboard 2 – Regional Analysis

- Revenue by Region
- Revenue by State
- Sales Distribution Map

### Dashboard 3 – Customer & Product Analysis

- Top Customers
- Top Products
- Product Profitability
- Customer Insights

---

# 🌐 Streamlit Dashboard

The Streamlit application provides an interactive analytics dashboard with:

- KPI Metrics
- Revenue Analysis
- Profit Analysis
- Monthly Trends
- Region-wise Analysis
- Product Performance
- Customer Analysis
- Interactive Filters

The application first attempts to connect to the MySQL database. If the database is unavailable, it automatically loads the cleaned CSV dataset as a fallback.

---

# 📌 Key Insights

- Identified high-performing products based on revenue and profit.
- Compared regional sales performance across the United States.
- Analyzed customer purchasing behavior.
- Evaluated monthly sales and profit trends.
- Built interactive dashboards to support business decision-making.

---

# 💻 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Retail-Sales-Analytics.git
```

### Navigate to the project directory

```bash
cd Retail-Sales-Analytics
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit application

```bash
streamlit run streamlit/app.py
```

---

# 🎯 Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- SQL Query Writing
- Window Functions
- Common Table Expressions (CTEs)
- Power BI Dashboard Development
- Streamlit Application Development
- Data Visualization
- Git & GitHub

---

# 📬 Contact

**Vanshika Jain**

MCA Student | Aspiring Data Analyst

---

⭐ If you found this project helpful, consider giving it a star.