#!/bin/bash
#
# Command Reference - Agentic AI Loan Eligibility Verification System
# =====================================================================

echo "==================================================================="
echo "Agentic AI Loan Eligibility Verification System - Command Reference"
echo "==================================================================="
echo ""

echo "📁 PROJECT LOCATION:"
echo "   /home/labuser/loan_approval"
echo ""

echo "🔧 SETUP COMMANDS:"
echo "   cd /home/labuser/loan_approval"
echo "   source .venv/bin/activate"
echo ""

echo "🚀 START SERVER:"
echo "   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "   Alternative (background):"
echo "   nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 &"
echo ""

echo "🌐 ACCESS API:"
echo "   Swagger UI:  http://localhost:8000/docs"
echo "   ReDoc:       http://localhost:8000/redoc"
echo "   Health:      http://localhost:8000/health"
echo "   Root:        http://localhost:8000/"
echo ""

echo "🧪 TESTING:"
echo "   python test_api.py"
echo ""

echo "📋 EXAMPLE CURL COMMANDS:"
echo ""
echo "1. Health Check:"
echo "   curl http://localhost:8000/health"
echo ""

echo "2. Submit Strong Application (Should be Approved):"
cat << 'EOF'
   curl -X POST "http://localhost:8000/loan/apply" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith",
       "income": 120000,
       "loan_amount": 250000,
       "existing_loans": 1,
       "repayment_score": 0.95,
       "employment_years": 8.0,
       "company_name": "Microsoft",
       "collateral_value": 350000
     }'
EOF
echo ""

echo "3. Submit Moderate Application (May be Conditional):"
cat << 'EOF'
   curl -X POST "http://localhost:8000/loan/apply" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "income": 60000,
       "loan_amount": 180000,
       "existing_loans": 3,
       "repayment_score": 0.72,
       "employment_years": 3.5,
       "company_name": "Tech Corp",
       "collateral_value": 200000
     }'
EOF
echo ""

echo "4. Check Application Status:"
echo "   curl http://localhost:8000/loan/status/APP-20260211-ABC12345"
echo ""

echo "📊 PYTHON EXAMPLE:"
cat << 'EOF'
   import requests
   
   response = requests.post(
       "http://localhost:8000/loan/apply",
       json={
           "name": "Jane Smith",
           "income": 90000,
           "loan_amount": 300000,
           "existing_loans": 1,
           "repayment_score": 0.92,
           "employment_years": 7.5,
           "company_name": "Microsoft",
           "collateral_value": 400000
       }
   )
   
   result = response.json()
   print(f"Decision: {result['decision']}")
   print(f"Risk Score: {result['risk_score']:.2%}")
   print(f"Application ID: {result['application_id']}")
EOF
echo ""

echo "🗄️ DATABASE COMMANDS:"
echo "   View database:"
echo "   sqlite3 loan_approval.db"
echo ""
echo "   Query applications:"
echo "   sqlite3 loan_approval.db 'SELECT application_id, applicant_name, status FROM applications;'"
echo ""
echo "   Count applications:"
echo "   sqlite3 loan_approval.db 'SELECT COUNT(*) FROM applications;'"
echo ""
echo "   Clear database:"
echo "   rm loan_approval.db"
echo "   # Database will be recreated on next server start"
echo ""

echo "📝 LOG COMMANDS:"
echo "   View logs (if server running in background):"
echo "   tail -f nohup.out"
echo ""

echo "🔍 DEBUGGING:"
echo "   Check if server is running:"
echo "   ps aux | grep uvicorn"
echo ""
echo "   Check port 8000:"
echo "   lsof -i :8000"
echo ""
echo "   Kill server on port 8000:"
echo "   lsof -ti :8000 | xargs kill -9"
echo ""

echo "📦 PACKAGE MANAGEMENT:"
echo "   Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "   Update packages:"
echo "   pip install -r requirements.txt --upgrade"
echo ""
echo "   List installed packages:"
echo "   pip list"
echo ""

echo "🔧 ENVIRONMENT CONFIGURATION:"
echo "   Edit configuration:"
echo "   nano .env"
echo ""
echo "   View current config:"
echo "   cat .env"
echo ""

echo "📚 DOCUMENTATION:"
echo "   Full documentation:    README.md"
echo "   Quick start guide:     QUICKSTART.md"
echo "   Project summary:       PROJECT_SUMMARY.txt"
echo "   API documentation:     http://localhost:8000/docs"
echo ""

echo "🎯 QUICK TEST SEQUENCE:"
echo "   1. source .venv/bin/activate"
echo "   2. python -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo "   3. (In another terminal) python test_api.py"
echo ""

echo "==================================================================="
echo "✅ System is READY FOR TESTING"
echo "==================================================================="
echo ""
echo "Server is currently running on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the server: Press CTRL+C or run: lsof -ti :8000 | xargs kill -9"
echo ""
