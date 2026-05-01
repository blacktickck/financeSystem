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

    st.subheader("Combined Transactions")

    st.dataframe(master_df)
