# Agentic AI Loan Eligibility Verification System

A sophisticated multi-agent system built with FastAPI that processes loan applications through specialized AI agents for comprehensive credit analysis.

## 🏗️ Architecture

This system implements a multi-agent architecture with the following components:

### Agents

1. **Orchestrator Agent** - Coordinates all sub-agents and manages workflow
2. **Greeting Agent** - Sends initial acknowledgment
3. **Planner Agent** - Creates verification strategy
4. **Credit History Agent** - Analyzes credit score and payment history
5. **Employment Verification Agent** - Validates employment details
6. **Collateral Verification Agent** - Assesses collateral value
7. **Critique Agent** - Reviews and validates agent outputs
8. **Final Decision Agent** - Makes approval decision with reasoning

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## 🚀 Setup Instructions

### 1. Clone and Navigate

```bash
cd /home/labuser/loan_approval
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file and add your API keys:

```bash
GEMINI_API_KEY=your_actual_gemini_api_key
SERPER_API_KEY=db9ed35c9262af6e3e4bada7fbfb1102d5565564
```

### 5. Initialize Database

The database will be automatically created on first run.

### 6. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Documentation

### Endpoint: POST /loan/apply

Submit a loan application for automated verification.

**Request Body:**

```json
{
  "name": "John Doe",
  "income": 75000.0,
  "loan_amount": 250000.0,
  "existing_loans": 2,
  "repayment_score": 0.85,
  "employment_years": 5.0,
  "company_name": "Tech Corp",
  "collateral_value": 300000.0
}
```

**Response:**

```json
{
  "decision": "Approved",
  "risk_score": 0.23,
  "reasoning": "Applicant has strong credit history...",
  "agent_summary": {
    "credit_history": {...},
    "employment": {...},
    "collateral": {...},
    "critique": {...}
  }
}
```

### Interactive API Docs

Visit these URLs when the server is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Example cURL Request

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

### Example Python Request

```python
import requests

url = "http://localhost:8000/loan/apply"
data = {
    "name": "Jane Smith",
    "income": 90000,
    "loan_amount": 300000,
    "existing_loans": 1,
    "repayment_score": 0.92,
    "employment_years": 7.5,
    "company_name": "Microsoft",
    "collateral_value": 400000
}

response = requests.post(url, json=data)
print(response.json())
```

## 📊 Risk Scoring Logic

### Credit History Agent
- **Low Risk**: Credit score > 700, repayment score > 0.8
- **Medium Risk**: Credit score 600-700, repayment score 0.6-0.8
- **High Risk**: Credit score < 600, repayment score < 0.6

### Employment Verification
- Validates employment duration > 1 year
- Checks company authenticity (simulated)

### Collateral Verification
- Applies 80% LTV (Loan-to-Value) ratio
- Ensures collateral coverage

## 🗂️ Project Structure

```
loan_approval/
├── main.py                 # FastAPI application entry point
├── database.py             # SQLite database setup
├── models.py               # Pydantic models
├── orchestrator.py         # Main orchestrator agent
├── agents/
│   ├── __init__.py
│   ├── greeting_agent.py
│   ├── planner_agent.py
│   ├── credit_history_agent.py
│   ├── employment_agent.py
│   ├── collateral_agent.py
│   ├── critique_agent.py
│   └── final_decision_agent.py
├── requirements.txt
├── .env
└── README.md
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Keep API keys secure
- Use HTTPS in production
- Implement rate limiting for production use
- Add authentication/authorization as needed

## 📝 Logging

Logs are written to console with INFO level by default. Adjust `LOG_LEVEL` in `.env` file:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

## 🛠️ Development

### Adding New Agents

1. Create new agent file in `agents/` folder
2. Implement agent logic
3. Register in orchestrator
4. Update models if needed

### Database Schema

The system uses SQLite to track:
- Application ID
- Applicant details
- Agent outputs
- Final decision
- Timestamps

## 🤝 Contributing

This is a demonstration project. For production use:
- Add comprehensive error handling
- Implement real API integrations
- Add authentication
- Enhance security measures
- Add comprehensive testing
- Implement monitoring and alerting

## 📄 License

MIT License - Feel free to use and modify.

## 🐛 Troubleshooting

### Database Locked Error
```bash
rm loan_approval.db
# Restart application
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use
```bash
uvicorn main:app --port 8001
```

## 📞 Support

For issues or questions, please check the logs and API documentation first.
