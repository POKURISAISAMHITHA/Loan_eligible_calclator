# Quick Start Guide - Agentic AI Loan Eligibility Verification System

## 🚀 Getting Started in 5 Minutes

### Step 1: Navigate to Project Directory
```bash
cd /home/labuser/loan_approval
```

### Step 2: Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Step 3: Start the Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### Step 4: Access API Documentation
Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 5: Test the API

#### Using cURL:
```bash
curl -X POST "http://localhost:8000/loan/apply" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "income": 90000,
    "loan_amount": 300000,
    "existing_loans": 1,
    "repayment_score": 0.92,
    "employment_years": 7.5,
    "company_name": "Microsoft",
    "collateral_value": 400000
  }'
```

#### Using Python:
```python
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

print(response.json())
```

#### Using the Test Script:
```bash
# Make sure the server is running, then in another terminal:
python test_api.py
```

## 📊 Understanding the Response

### Sample Response:
```json
{
  "decision": "Approved",
  "risk_score": 0.23,
  "reasoning": "After comprehensive multi-agent analysis...",
  "agent_summary": {
    "credit_history": {
      "credit_score": 750,
      "risk_category": "Low",
      "debt_to_income_ratio": 0.35,
      "passed": true
    },
    "employment": {
      "employment_verified": true,
      "company_verified": true,
      "stability": "Excellent (5+ years)",
      "passed": true
    },
    "collateral": {
      "collateral_sufficient": true,
      "ltv_ratio": 0.75,
      "effective_coverage": 1.07,
      "passed": true
    },
    "critique": {
      "inconsistencies_count": 0,
      "confidence_score": 0.95
    }
  },
  "application_id": "APP-20260211-ABC12345",
  "timestamp": "2026-02-11T10:30:00"
}
```

## 🎯 Test Scenarios

### Scenario 1: Strong Applicant (Approved)
```json
{
  "name": "Jane Smith",
  "income": 120000,
  "loan_amount": 250000,
  "existing_loans": 1,
  "repayment_score": 0.95,
  "employment_years": 8.0,
  "company_name": "Microsoft",
  "collateral_value": 350000
}
```
**Expected**: Approved, Low Risk

### Scenario 2: Moderate Applicant (Conditional)
```json
{
  "name": "John Doe",
  "income": 60000,
  "loan_amount": 180000,
  "existing_loans": 3,
  "repayment_score": 0.72,
  "employment_years": 3.5,
  "company_name": "Tech Corp",
  "collateral_value": 200000
}
```
**Expected**: Conditional, Medium Risk

### Scenario 3: Weak Applicant (Rejected)
```json
{
  "name": "Bob Johnson",
  "income": 35000,
  "loan_amount": 200000,
  "existing_loans": 5,
  "repayment_score": 0.45,
  "employment_years": 0.5,
  "company_name": "Small Startup",
  "collateral_value": 80000
}
```
**Expected**: Rejected, High Risk

## 🔧 Configuration

### Environment Variables (.env file)
```bash
# API Keys
SERPER_API_KEY=db9ed35c9262af6e3e4bada7fbfb1102d5565564
GEMINI_API_KEY=your_gemini_api_key_here

# Database
DATABASE_URL=sqlite:///./loan_approval.db

# Application Settings
LOG_LEVEL=INFO
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and API info |
| `/health` | GET | Detailed system health status |
| `/loan/apply` | POST | Submit loan application |
| `/loan/status/{id}` | GET | Get application status |
| `/docs` | GET | Interactive API documentation |

## 🤖 Agent Architecture

The system uses 7 specialized agents:

1. **Greeting Agent** - Welcomes applicant
2. **Planner Agent** - Creates verification strategy
3. **Credit History Agent** - Analyzes credit (deterministic)
4. **Employment Agent** - Verifies employment (simulated)
5. **Collateral Agent** - Assesses collateral value
6. **Critique Agent** - Cross-validates all outputs
7. **Final Decision Agent** - Makes approval decision

## 📈 Risk Scoring

Risk scores range from 0 (lowest) to 1 (highest):
- **0.00 - 0.30**: Low Risk → Likely Approved
- **0.31 - 0.50**: Medium Risk → Conditional Approval
- **0.51 - 1.00**: High Risk → Likely Rejected

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn main:app --port 8001
```

### Database issues
```bash
# Remove and recreate database
rm loan_approval.db
# Restart server - database will be recreated
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 🎓 Understanding the Code

### Project Structure:
```
loan_approval/
├── main.py              # FastAPI app & endpoints
├── orchestrator.py      # Coordinates all agents
├── database.py          # SQLite operations
├── models.py            # Pydantic data models
├── agents/              # Individual agent modules
│   ├── greeting_agent.py
│   ├── planner_agent.py
│   ├── credit_history_agent.py
│   ├── employment_agent.py
│   ├── collateral_agent.py
│   ├── critique_agent.py
│   └── final_decision_agent.py
├── requirements.txt     # Python dependencies
├── .env                 # Configuration
└── README.md           # Full documentation
```

## 🔐 Security Best Practices

1. **Never commit `.env`** to version control
2. **Use HTTPS** in production
3. **Add authentication** for production use
4. **Rate limiting** to prevent abuse
5. **Input validation** (already implemented)
6. **Secure database** access

## 📞 Next Steps

1. ✅ Review the code structure
2. ✅ Test all endpoints using `/docs`
3. ✅ Run test_api.py script
4. ✅ Customize agent logic as needed
5. ✅ Add authentication for production
6. ✅ Deploy to cloud (AWS, GCP, Azure)

## 💡 Tips

- Check logs for detailed agent processing
- Use `/docs` for interactive testing
- Monitor the database for all applications
- Adjust risk thresholds in agents as needed
- Extend with real API integrations when ready

---

**System Status**: ✅ Ready for Testing

**API Documentation**: http://localhost:8000/docs

**Support**: Check logs and README.md for details
