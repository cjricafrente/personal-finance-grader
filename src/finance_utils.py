
# finance_utils.py
import boto3
import json
import datetime
import os

from pathlib import Path

def compute_metrics(monthly_income, monthly_expenses, savings, loan_amount, record_year=None):
    income = float(monthly_income) if monthly_income is not None else 0.0
    expenses = float(monthly_expenses) if monthly_expenses is not None else 0.0
    savings_val = float(savings) if savings is not None else 0.0
    loan = float(loan_amount) if loan_amount is not None else 0.0
    savings_rate = (savings_val / income * 100) if income > 0 else 0.0
    expense_ratio = (expenses / income * 100) if income > 0 else 0.0
    loan_to_income_ratio = (loan / income * 100) if income > 0 else 0.0
    net_balance = income - expenses
    return {
        "monthly_income": income,
        "monthly_expenses": expenses,
        "savings": savings_val,
        "loan_amount": loan,
        "savings_rate": round(savings_rate, 2),
        "expense_ratio": round(expense_ratio, 2),
        "loan_to_income_ratio": round(loan_to_income_ratio, 2),
        "net_balance": round(net_balance, 2),
        "record_year": record_year
    }

def compute_finance_score(metrics, education_level=None):
    """Compute a realistic personal finance score and grade."""

    # Extract key ratios
    sr = metrics.get("savings_rate", 0)               # % of income saved
    er = metrics.get("expense_ratio", 100)            # % of income spent
    lir = metrics.get("loan_to_income_ratio", 0)      # % of income borrowed

    # --- Weight components more fairly ---
    # Savings → Strongly rewarded
    comp_savings = min(sr, 50) * 0.5  # max 25 points

    # Expenses → Lower = better
    comp_expense = max(0, (100 - er)) * 0.3  # max 30 points

    # Loan → Lower = better
    comp_loan = max(0, (100 - min(lir, 100))) * 0.2  # max 20 points

    # Combine the three components
    base_score = comp_savings + comp_expense + comp_loan

    # Normalize score to stay within 0–100
    score = max(0, min(100, round(base_score * 1.2, 2)))

    # --- Education Level Bonus ---
    edu = (education_level or "").strip().lower()
    if edu in ("high school", "senior high", "hs"):
        score += 3
    elif edu in ("college", "undergrad", "bachelor"):
        score += 5
    elif edu in ("masters", "postgrad", "graduate"):
        score += 7

    # Cap to 100
    score = max(0, min(100, round(score, 2)))

    # --- Assign Grades ---
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 45:
        grade = "D"
    else:
        grade = "E"

    return {"score": score, "grade": grade}


def evaluate_finance_grade(record, education_level=None):
    metrics = compute_metrics(
        record.get("monthly_income"),
        record.get("monthly_expenses"),
        record.get("savings"),
        record.get("loan_amount"),
        record.get("record_year")
    )
    scoring = compute_finance_score(metrics, education_level=education_level)
    recs = []
    if metrics["savings_rate"] >= 20:
        recs.append("Great — your savings rate is above 20%. Keep it up!")
    if metrics["expense_ratio"] > 80:
        recs.append("Your expense ratio is >80% of income. Try to cut non-essential expenses.")
    if metrics["loan_to_income_ratio"] > 100:
        recs.append("Loan amount is >100% of monthly income. Consider debt repayment planning.")
    if metrics["savings"] < (0.1 * metrics["monthly_income"]):
        recs.append("Your savings is less than 10% of income — aim to increase it gradually.")
    if metrics["net_balance"] < 0:
        recs.append("Your expenses exceed income — track expenses and seek ways to reduce them.")
    if not recs:
        recs.append("Your finances look balanced based on provided inputs.")
    out = {
        "metrics": metrics,
        "score": scoring["score"],
        "grade": scoring["grade"],
        "recommendations": recs
    }
    return out

def save_to_s3(record, result, bucket_name, aws_access_key, aws_secret_key):
    """
    Uploads the finance evaluation result to AWS S3 as a JSON file.
    """
    try:
        # Create an S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        # Construct the object name (filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_key = f"finance_records/{timestamp}.json"

        # Combine record + result
        upload_data = {
            "record": record,
            "result": result
        }

        # Convert to JSON string
        json_data = json.dumps(upload_data, indent=4)

        # Upload to S3
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_data)

        return f"✅ Successfully uploaded to S3 bucket: {bucket_name}/{object_key}"

    except Exception as e:
        return f"❌ Failed to upload: {str(e)}"

