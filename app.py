import streamlit as st
from src.finance_utils import evaluate_finance_grade

st.set_page_config(page_title="Personal Finance Grader", layout="centered")

st.title("💰 Personal Finance Grader (Philippines)")
st.write("Get your financial health grade based on your income, expenses, and loans.")

# Input fields
monthly_income = st.number_input("Monthly Income (PHP)", min_value=0.0, step=1000.0)
monthly_expenses = st.number_input("Monthly Expenses (PHP)", min_value=0.0, step=500.0)
savings = st.number_input("Current Savings (PHP)", min_value=0.0, step=500.0)
loan_amount = st.number_input("Total Loan Amount (PHP)", min_value=0.0, step=1000.0)
education_level = st.selectbox(
    "Education Level",
    ["High School", "College", "Graduate", "Vocational", "None"]
)
record_year = st.number_input("Record Year", min_value=2020, max_value=2030, value=2025)

if st.button("Evaluate My Finance Grade"):
    record = {
        "monthly_income_php_adj": monthly_income,
        "monthly_expenses_php_adj": monthly_expenses,
        "savings_php_adj": savings,
        "loan_amount_php_adj": loan_amount,
        "education_level": education_level,
        "record_year": record_year
    }

    result = evaluate_finance_grade(record)
    st.subheader(f"🏅 Your Grade: {result['grade']}")
    st.write(f"**Score:** {result['score']:.2f}")

    st.write("### 💡 Recommendations")
    for rec in result["recommendations"]:
        st.write(f"- {rec}")

    st.write("### 📊 Details")
    st.json(result["metrics"])
