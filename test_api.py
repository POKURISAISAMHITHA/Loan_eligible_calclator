#!/usr/bin/env python3
"""
Test Example Script
Demonstrates how to use the Loan Eligibility API
"""
import requests
import json


def test_loan_application():
    """Test the loan application endpoint"""
    
    url = "http://localhost:8000/loan/apply"
    
    # Test Case 1: Strong Applicant (Should be Approved)
    print("=" * 80)
    print("Test Case 1: Strong Applicant")
    print("=" * 80)
    
    strong_applicant = {
        "name": "Jane Smith",
        "income": 120000.0,
        "loan_amount": 250000.0,
        "existing_loans": 1,
        "repayment_score": 0.95,
        "employment_years": 8.0,
        "company_name": "Microsoft",
        "collateral_value": 350000.0
    }
    
    response = requests.post(url, json=strong_applicant)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # Test Case 2: Moderate Applicant (May be Conditional)
    print("=" * 80)
    print("Test Case 2: Moderate Applicant")
    print("=" * 80)
    
    moderate_applicant = {
        "name": "John Doe",
        "income": 60000.0,
        "loan_amount": 180000.0,
        "existing_loans": 3,
        "repayment_score": 0.72,
        "employment_years": 3.5,
        "company_name": "Tech Corp",
        "collateral_value": 200000.0
    }
    
    response = requests.post(url, json=moderate_applicant)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Decision: {result['decision']}")
    print(f"Risk Score: {result['risk_score']:.2%}")
    print(f"Application ID: {result['application_id']}")
    print()
    
    # Test Case 3: Weak Applicant (Likely Rejected)
    print("=" * 80)
    print("Test Case 3: Weak Applicant")
    print("=" * 80)
    
    weak_applicant = {
        "name": "Bob Johnson",
        "income": 35000.0,
        "loan_amount": 200000.0,
        "existing_loans": 5,
        "repayment_score": 0.45,
        "employment_years": 0.5,
        "company_name": "Small Startup",
        "collateral_value": 80000.0
    }
    
    response = requests.post(url, json=weak_applicant)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Decision: {result['decision']}")
    print(f"Risk Score: {result['risk_score']:.2%}")
    print()
    
    # Test Case 4: High Income, Good Collateral
    print("=" * 80)
    print("Test Case 4: High Income Professional")
    print("=" * 80)
    
    high_income = {
        "name": "Dr. Sarah Williams",
        "income": 250000.0,
        "loan_amount": 500000.0,
        "existing_loans": 2,
        "repayment_score": 0.88,
        "employment_years": 12.0,
        "company_name": "Google",
        "collateral_value": 700000.0
    }
    
    response = requests.post(url, json=high_income)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Decision: {result['decision']}")
    print(f"Risk Score: {result['risk_score']:.2%}")
    print(f"Credit Score: {result['agent_summary']['credit_history']['credit_score']:.0f}")
    print()


def test_health_check():
    """Test the health check endpoint"""
    print("=" * 80)
    print("Health Check")
    print("=" * 80)
    
    response = requests.get("http://localhost:8000/health")
    print(json.dumps(response.json(), indent=2))
    print()


def test_application_status(application_id: str):
    """Test getting application status"""
    print("=" * 80)
    print(f"Application Status: {application_id}")
    print("=" * 80)
    
    response = requests.get(f"http://localhost:8000/loan/status/{application_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.json())
    print()


if __name__ == "__main__":
    print("Agentic AI Loan Eligibility Verification System - Test Suite")
    print("=" * 80)
    print()
    
    # Run health check first
    test_health_check()
    
    # Run loan application tests
    test_loan_application()
    
    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)
