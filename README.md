## Personal Finance Grader
Data-Driven Financial Health Evaluator (Streamlit + AWS)

Author: Carl Joshua Ricafrente
Date: October 2025
Tech Stack: Python, Streamlit, AWS S3, boto3, JSON

## Overview

Personal Finance Grader is an interactive data app that evaluates an individual's financial health based on their income, expenses, savings, and loans.

It provides:

A data-driven financial score (0–100)

A grade (A–F) with bilingual recommendations (English + Filipino)

Optional AWS S3 integration for securely saving results to the cloud

This project demonstrates end-to-end data workflow skills — from user input and metric computation, to analysis, visualization, and cloud data engineering integration.

## Features
Category	Description
- Financial Analytics	Calculates savings rate, expense ratio, loan-to-income ratio, and net balance.
- Scoring Logic	Generates a financial health score and letter grade.
- Recommendations	Provides personalized insights in both English and Filipino.
- AWS Integration	Uploads user results to AWS S3 for cloud data storage.
- Modular Design	Python functions are modular and reusable for ML or dashboard extensions.
- Tech Stack

Frontend: Streamlit (interactive user interface)

Backend / Logic: Python

Cloud Storage: AWS S3 (via boto3)

Data Format: JSON

## How It Works

Input Financial Data

Monthly income, expenses, savings, and loans

Optional education level and record year

Evaluate

The app computes key metrics and a financial health score.

A bilingual financial grade and recommendations are shown.

Save to AWS

(Optional) Users can connect their AWS S3 credentials to save their financial record as a JSON file in their chosen bucket.

#Project Structure
personal-finance-grader/
│
├── app.py                     # Main Streamlit app
├── requirements.txt            # Project dependencies
│
└── src/
    ├── __init__.py
    └── finance_utils.py        # Core financial logic + AWS upload function

## Setup Instructions
1.  Clone the Repository
git clone https://github.com/cjricafrente/personal-finance-grader.git
cd personal-finance-grader

2️. Install Dependencies
pip install -r requirements.txt

3️. Run the App
streamlit run app.py

4️. (Optional) Connect AWS

If you want to store results in S3:

Create an S3 bucket in AWS

Get your Access Key ID and Secret Access Key

Enter them inside the Streamlit app when prompted

## Example Output

Input

Monthly Income: 10,000
Monthly Expenses: 1,000
Savings: 3,000
Loan Amount: 0
Education Level: College


Output

{
  "metrics": {
    "monthly_income": 10000,
    "monthly_expenses": 1000,
    "savings": 3000,
    "loan_amount": 0,
    "savings_rate": 30.0,
    "expense_ratio": 10.0,
    "loan_to_income_ratio": 0.0,
    "net_balance": 9000,
    "record_year": 2025
  },
  "score": 85,
  "grade": "A",
  "recommendations": [
    "Excellent — your savings rate is above 20%. Keep it up!"
  ]
}

## Cloud Integration

This project integrates with AWS S3 for secure and scalable data storage.
All records are uploaded as timestamped JSON files using the AWS SDK (boto3).
Example filename:

finance-record-2025-10-16-13-42-21.json

## Future Improvements

This project is designed for continuous enhancement. Planned updates include:

- Predictive modeling for financial trend analysis

- Integration with ML models for automated financial advice

- Streamlit dashboard for aggregated insights

- Enhanced AWS security using IAM roles and environment variables

- Athena integration for SQL-based analytics

## Links
GitHub Repository: https://github.com/cjricafrente/personal-finance-grader

Author: LinkedIn: Carl Joshua Ricafrente
