import streamlit as st
import pandas as pd
from finance_engine import FinanceEngine


st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide"
)

st.title("Automated Personal Finance System")

uploaded_file = st.file_uploader(
    "Upload Bank Statement",
    type=["xlsx"]
)

if uploaded_file:

    with open("temp.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    engine = FinanceEngine("temp.xlsx")

    df = engine.load_data()

    df = engine.process_transactions()

    summary = engine.calculate_summary()

    st.subheader("Financial KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", f"₹{summary['Total Income']:,.0f}")
    col2.metric("Expense", f"₹{summary['Total Expense']:,.0f}")
    col3.metric("Savings", f"₹{summary['Net Savings']:,.0f}")
    col4.metric("Savings Rate", f"{summary['Savings Rate']}%")

    st.subheader("Categorized Transactions")

    st.dataframe(df)

    st.subheader("Category Summary")

    category_summary = engine.category_summary()

    st.bar_chart(category_summary)