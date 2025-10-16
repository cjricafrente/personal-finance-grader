
# finance_utils.py
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
    sr = metrics.get("savings_rate", 0)
    er = metrics.get("expense_ratio", 100)
    lir = metrics.get("loan_to_income_ratio", 0)
    comp_savings = sr * 0.4
    comp_expense = (100 - er) * 0.3
    loan_component_raw = max(0, 100 - (lir * 0.5))
    comp_loan = loan_component_raw * 0.3
    base_score = comp_savings + comp_expense + comp_loan
    score = max(0, min(100, round(base_score, 2)))
    edu = (education_level or "").strip().lower()
    if edu in ("high school", "senior high", "hs"):
        score += 3
    elif edu in ("college", "undergrad", "bachelor"):
        score += 0
    elif edu in ("masters", "postgrad", "graduate"):
        score += 2
    score = max(0, min(100, round(score,2)))
    if score >= 85:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    elif score >= 40:
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
