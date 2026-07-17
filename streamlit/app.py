from pathlib import Path
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

hide_streamlit = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background-color:#f8f9fa;
}

[data-testid="stMetricValue"]{
    font-size:30px;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:12px;
    padding:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,.08);
}

h1,h2,h3{
    color:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATABASE
# ==========================================================

@st.cache_data
def load_data():

    try:
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_name = os.getenv("DB_NAME", "sales_project")

        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )

        df = pd.read_sql(
            "SELECT * FROM sales_data",
            engine
        )

        source = "MySQL Database"

    except Exception:

        BASE_DIR = Path(__file__).resolve().parent.parent
        csv_path = BASE_DIR / "data" / "cleaned_sales_data.csv"

        df = pd.read_csv(csv_path)

        source = "CSV File"

    df["order_date"] = pd.to_datetime(df["order_date"])

    return df, source

df, data_source = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📌 Dashboard Filters")
if data_source == "MySQL Database":
    st.sidebar.success("✅ Connected to MySQL Database")
else:
    st.sidebar.info("📄 Running from CSV (Cloud Mode)")

# Date Filter

min_date = df["order_date"].min()
max_date = df["order_date"].max()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region

selected_region = st.sidebar.multiselect(
    "Region",
    sorted(df["us_region"].unique()),
    default=sorted(df["us_region"].unique())
)

# State

selected_state = st.sidebar.multiselect(
    "State",
    sorted(df["State_Name"].unique()),
    default=sorted(df["State_Name"].unique())
)

# Channel

selected_channel = st.sidebar.multiselect(
    "Sales Channel",
    sorted(df["channel"].unique()),
    default=sorted(df["channel"].unique())
)

# Product

selected_product = st.sidebar.multiselect(
    "Product",
    sorted(df["Product_Name"].unique()),
    default=[]
)

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = df.copy()

# Date

if len(date_range)==2:

    start_date,end_date=date_range

    filtered_df=filtered_df[
        (filtered_df["order_date"]>=pd.to_datetime(start_date))&
        (filtered_df["order_date"]<=pd.to_datetime(end_date))
    ]

# Region

filtered_df=filtered_df[
    filtered_df["us_region"].isin(selected_region)
]

# State

filtered_df=filtered_df[
    filtered_df["State_Name"].isin(selected_state)
]

# Channel

filtered_df=filtered_df[
    filtered_df["channel"].isin(selected_channel)
]

# Product

if selected_product:

    filtered_df=filtered_df[
        filtered_df["Product_Name"].isin(selected_product)
    ]

# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Retail Sales Analytics Dashboard")

st.markdown(
"""
Analyze sales performance across regions, customers,
products and sales channels using interactive visualizations.
"""
)

# ==========================================================
# KPI SECTION
# ==========================================================

def money(x):

    if x>=1_000_000:
        return f"${x/1_000_000:.2f} M"

    elif x>=1000:
        return f"${x/1000:.1f} K"

    return f"${x:.0f}"


revenue = filtered_df["revenue"].sum()

profit = filtered_df["profit"].sum()

orders = filtered_df["Order_Number"].nunique()

customers = filtered_df["Customer_Name"].nunique()

quantity = filtered_df["quantity"].sum()

avg_order = revenue/orders if orders else 0

profit_margin = (
    profit/revenue*100
    if revenue else 0
)

avg_customer = (
    revenue/customers
    if customers else 0
)

c1,c2,c3,c4 = st.columns(4)

c1.metric("💰 Revenue", money(revenue))

c2.metric("📈 Profit", money(profit))

c3.metric("🛒 Orders", f"{orders:,}")

c4.metric("👥 Customers", f"{customers:,}")

c5,c6,c7,c8 = st.columns(4)

c5.metric("📦 Quantity", f"{quantity:,}")

c6.metric("💵 Avg Order", money(avg_order))

c7.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

c8.metric("⭐ Avg Revenue / Customer", money(avg_customer))

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Overview",
        "📦 Products",
        "🌍 Regions",
        "📋 Data"
    ]
)

# ==========================================================
# OVERVIEW TAB
# ==========================================================

with tab1:

    monthly = (
        filtered_df
        .groupby(["order_month_num", "order_month_name"])[["revenue", "profit"]]
        .sum()
        .reset_index()
        .sort_values("order_month_num")
    )

    fig = px.line(
        monthly,
        x="order_month_name",
        y=["revenue", "profit"],
        markers=True,
        title="Monthly Revenue & Profit Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            filtered_df,
            x="revenue",
            y="profit",
            color="channel",
            size="quantity",
            hover_name="Product_Name",
            title="Revenue vs Profit"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        monthly_qty = (
            filtered_df.groupby(
                ["order_month_num", "order_month_name"]
            )["quantity"]
            .sum()
            .reset_index()
            .sort_values("order_month_num")
        )

        fig = px.bar(
            monthly_qty,
            x="order_month_name",
            y="quantity",
            color="quantity",
            title="Monthly Quantity Sold"
        )

        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# PRODUCTS TAB
# ==========================================================

with tab2:

    choice = st.radio(
        "Product Performance",
        ["Top 10 Products", "Bottom 10 Products"],
        horizontal=True
    )

    product_sales = (
        filtered_df.groupby("Product_Name")
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Quantity=("quantity", "sum")
        )
    )

    if choice == "Top 10 Products":
        product_sales = product_sales.sort_values(
            "Revenue",
            ascending=False
        ).head(10)

    else:
        product_sales = product_sales.sort_values(
            "Revenue",
            ascending=True
        ).head(10)

    product_sales = product_sales.reset_index()

    fig = px.bar(
        product_sales,
        x="Revenue",
        y="Product_Name",
        orientation="h",
        color="Profit",
        hover_data=["Quantity"],
        title=choice
    )

    st.plotly_chart(fig, use_container_width=True)

    customer = (
        filtered_df.groupby("Customer_Name")
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        customer,
        x="Revenue",
        y="Customer_Name",
        orientation="h",
        color="Profit",
        title="Top 10 Customers"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# REGIONS TAB
# ==========================================================

with tab3:

    left, right = st.columns(2)

    region = (
        filtered_df.groupby("us_region")
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum")
        )
        .reset_index()
    )

    with left:

        fig = px.bar(
            region,
            x="us_region",
            y="Revenue",
            color="Revenue",
            title="Revenue by Region"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.bar(
            region,
            x="us_region",
            y="Profit",
            color="Profit",
            title="Profit by Region"
        )

        st.plotly_chart(fig, use_container_width=True)

    channel = (
        filtered_df.groupby("channel")["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        channel,
        names="channel",
        values="revenue",
        hole=0.5,
        title="Revenue by Sales Channel"
    )

    st.plotly_chart(fig, use_container_width=True)

    state = (
        filtered_df.groupby("State_Name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        state,
        x="revenue",
        y="State_Name",
        orientation="h",
        title="Top States by Revenue",
        color="revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

    state_map = (
        filtered_df.groupby(
            ["State_Name", "lat", "lon"]
        )["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.scatter_mapbox(
        state_map,
        lat="lat",
        lon="lon",
        size="revenue",
        color="revenue",
        hover_name="State_Name",
        zoom=3,
        mapbox_style="carto-positron",
        title="Revenue Distribution Across US States"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# DATA TAB
# ==========================================================

with tab4:

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        "📥 Download Filtered CSV",
        csv,
        file_name="filtered_sales.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.metric("Records", len(filtered_df))