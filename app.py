import streamlit as st
import pandas as pd
from finance_engine import FinanceEngine


st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide"
)

st.title("Automated Personal Finance System")

uploaded_files = st.file_uploader(
    "Upload Bank Statements",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:

    all_dataframes = []

    for uploaded_file in uploaded_files:

        temp_file = uploaded_file.name

        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())

        engine = FinanceEngine(temp_file)

        df = engine.load_data()

        df = engine.process_transactions()

        account_name = uploaded_file.name.split(".")[0]

        df["Account"] = account_name

        all_dataframes.append(df)

    master_df = pd.concat(
        all_dataframes,
        ignore_index=True
    )
    selected_account = st.selectbox(
        "Select Account",
        ["All"] + list(master_df["Account"].unique())
    )

    if selected_account != "All":

        filtered_df = master_df[
            master_df["Account"] == selected_account
        ]

    else:

        filtered_df = master_df
    st.subheader("Combined Transactions")

    st.dataframe(filtered_df)
    total_income = filtered_df["Credit"].fillna(0).sum()

    total_expense = filtered_df["Debit"].fillna(0).sum()

    net_savings = total_income - total_expense

    if total_income > 0:

        savings_rate = (
            net_savings / total_income
        ) * 100

    else:

        savings_rate = 0


    st.subheader("Financial KPIs")
    st.subheader("Category Summary")

    category_summary = filtered_df.groupby(
        "Category"
    )["Debit"].sum()

    st.bar_chart(category_summary)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Income",
        f"₹{total_income:,.0f}"
    )

    col2.metric(
        "Expense",
        f"₹{total_expense:,.0f}"
    )

    col3.metric(
        "Savings",
        f"₹{net_savings:,.0f}"
    )

    col4.metric(
        "Savings Rate",
        f"{savings_rate:.2f}%"
    )
