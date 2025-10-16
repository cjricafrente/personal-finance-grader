import streamlit as st
from src.finance_utils import evaluate_finance_grade, save_to_s3

st.set_page_config(page_title="Personal Finance Grader", page_icon="💰")

st.title("💰 Personal Finance Grader")
st.write("Discover how well you're managing your finances!")

# Input fields
monthly_income = st.number_input("Monthly Income (Buwanang Kita)", min_value=0.0, step=1000.0)
monthly_expenses = st.number_input("Monthly Expenses (Buwanang Gastos)", min_value=0.0, step=1000.0)
savings = st.number_input("Savings (Ipon)", min_value=0.0, step=1000.0)
loan_amount = st.number_input("Loan Amount (Halagang Hiniram)", min_value=0.0, step=1000.0)

education_level = st.selectbox(
    "Education Level (Antas ng Edukasyon)",
    ["None", "High School", "College", "Graduate"]
)
record_year = st.number_input("Record Year", min_value=2020, max_value=2030, value=2025)

# --- Evaluate button ---
if st.button("Evaluate My Finance Grade (Suriin ang Aking Antas sa Pananalapi)"):
    record = {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "savings": savings,
        "loan_amount": loan_amount,
        "record_year": record_year
    }
    result = evaluate_finance_grade(record, education_level)

    # store in session so it persists when interacting further
    st.session_state["record"] = record
    st.session_state["result"] = result

# --- If we already have a result stored ---
if "result" in st.session_state:
    result = st.session_state["result"]
    score = result["score"]

    # Feedback
    st.subheader("Your Finance Grade (Ang Iyong Antas sa Pananalapi):")
    if score >= 85:
        st.success("Excellent financial health! (Magandang kalagayang pinansyal!) 🌟")
    elif score >= 70:
        st.info("Good, but there’s room for improvement. (Maganda pero may puwang pa para umangat.) 💡")
    else:
        st.warning("Be careful — you might be overspending! (Mag-ingat — baka sobra ang gastos!) ⚠️")

    # Show details
    st.write("### Financial Details (Mga Detalye ng Pananalapi)")
    st.json(result)

    # --- AWS section ---
    st.subheader("💾 Save to AWS (optional)")
    use_aws = st.checkbox("Save my data to AWS S3")
    if use_aws:
        bucket_name = st.text_input("S3 Bucket Name", "finance-grader-data-cjdr")
        aws_access_key = st.text_input("AWS Access Key ID", type="password")
        aws_secret_key = st.text_input("AWS Secret Access Key", type="password")

        if st.button("Upload to S3"):
            status = save_to_s3(
                st.session_state["record"],
                st.session_state["result"],
                bucket_name,
                aws_access_key,
                aws_secret_key,
            )
            st.info(status)
