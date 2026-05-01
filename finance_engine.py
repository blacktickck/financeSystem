import pandas as pd
import matplotlib.pyplot as plt
import os,re
from categories import CATEGORY_RULES




class FinanceEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
    def load_data(self):
        self.df = pd.read_excel(
            self.file_path,
            skiprows=21
        )
        self.df.columns = [
            str(col).strip()
            for col in self.df.columns
        ]
        print("\nDetected Columns:")
        print(self.df.columns)

        self.df = self.df.dropna(
            subset=["Transaction Date"]
        )

        return self.df


    def categorize_transaction(self, text):
        text = str(text).lower()
        for category, keywords in CATEGORY_RULES.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, text):
                    return category
        return "Others"


    def process_transactions(self):
        narration_column = "Particulars"
        self.df["Category"] = self.df[
            narration_column
        ].apply(
            self.categorize_transaction
        )
        return self.df
    
    def clean_amount_column(self, column_name):
        self.df[column_name] = (
            self.df[column_name]
            .astype(str)
            .str.replace(",", "")
            .replace("nan", "0")
        )
        self.df[column_name] = pd.to_numeric(
            self.df[column_name],
            errors="coerce"
        ).fillna(0)

    def calculate_summary(self):
        debit_col = "Debit"
        credit_col = "Credit"
        self.clean_amount_column(debit_col)
        self.clean_amount_column(credit_col)
        total_income = self.df[
            credit_col
        ].sum()
        total_expense = self.df[
            debit_col
        ].sum()
        savings = total_income - total_expense
        if total_income > 0:
            savings_rate = (
                savings / total_income
            ) * 100
        else:
            savings_rate = 0
        summary = {
            "Total Income": round(
                total_income,
                2
            ),
            "Total Expense": round(
                total_expense,
                2
            ),
            "Net Savings": round(
                savings,
                2
            ),
            "Savings Rate": round(
                savings_rate,
                2
            )
        }
        return summary

    def category_summary(self):
        category_data = self.df.groupby(
            "Category"
        )[
            ["Debit"]
        ].sum()
        category_data = category_data.sort_values(
            by="Debit",
            ascending=False
        )
        return category_data

    def create_charts(self):
        category_data = self.category_summary()
        plt.figure(figsize=(10, 6))
        plt.bar(
            category_data.index,
            category_data["Debit"]
        )
        plt.xticks(rotation=45)
        plt.title("Expense by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.tight_layout()
        os.makedirs(
            "output/charts",
            exist_ok=True
        )
        plt.savefig(
            "output/charts/expense_chart.png"
        )
        plt.close()

    def export_reports(self):
        os.makedirs(
            "output",
            exist_ok=True
        )
        self.df.to_excel(
            "output/categorized_transactions.xlsx",
            index=False
        )
        category_summary = self.category_summary()
        category_summary.to_excel(
            "output/dashboard_summary.xlsx"
        )

if __name__ == "__main__":
    engine = FinanceEngine(
        "data/bank_statement.xlsx"
    )
    engine.load_data()
    engine.process_transactions()
    summary = engine.calculate_summary()
    print("\nFinancial Summary")
    print("-" * 50)
    for key, value in summary.items():
        print(f"{key}: ₹{value:,.2f}")
    engine.create_charts()
    engine.export_reports()
    print("\nReports Generated Successfully")
    print("\nCheck output folder for reports and charts.")