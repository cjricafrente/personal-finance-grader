import streamlit as st
from src.finance_utils import evaluate_finance_grade

st.set_page_config(page_title="Personal Finance Grader", page_icon="💰")

# Title
st.title("💰 Personal Finance Grader")

st.write("Discover how well you're managing your finances!")

# Input fields (Bilingual)
monthly_income = st.number_input("Monthly Income (Buwanang Kita)", min_value=0.0, step=1000.0)
monthly_expenses = st.number_input("Monthly Expenses (Buwanang Gastos)", min_value=0.0, step=1000.0)
savings = st.number_input("Savings (Ipon)", min_value=0.0, step=1000.0)
loan_amount = st.number_input("Loan Amount (Halagang Hiniram)", min_value=0.0, step=1000.0)

education_level = st.selectbox(
    "Education Level (Antas ng Edukasyon)",
    ["None", "High School", "College", "Graduate"]
)

# When user clicks evaluate
if st.button("Evaluate My Finance Grade (Suriin ang Aking Antas sa Pananalapi)"):
    record = {
        "monthly_income_php_adj": monthly_income,
        "monthly_expenses_php_adj": monthly_expenses,
        "savings_php_adj": savings,
        "loan_amount_php_adj": loan_amount,
    }

    result = evaluate_finance_grade(record, education_level = education_level)

    st.subheader(f"🏅 Your Grade: {result['grade']}")
    st.write(f"**Score:** {result['score']:.2f}")

    st.write("### 💡 Recommendations")
    for rec in result["recommendations"]:
        st.write(f"- {rec}")

    # Show details
    st.write("### Financial Details (Mga Detalye ng Pananalapi)")
    st.json(result)
