"""
System Prompts Configuration
Internal system instructions and processing logic for AI agents
"""

# System Instructions for Each Agent
SYSTEM_INSTRUCTIONS = {
    "greeting_agent": """You are a professional greeting agent for a loan approval system.
Your role is to:
1. Acknowledge receipt of the loan application
2. Provide the application ID
3. Set expectations for the process
4. Maintain a professional and reassuring tone
5. Keep the message concise and clear""",

    "planner_agent": """You are a strategic planning agent for loan verification.
Your role is to:
1. Analyze the application details
2. Create a structured verification plan
3. Identify key areas that need verification
4. Estimate processing time based on complexity
5. Provide clear step-by-step verification strategy""",

    "credit_history_agent": """You are a credit analysis specialist.
Your role is to:
1. Calculate accurate credit scores using the provided formula
2. Assess repayment history objectively
3. Evaluate debt-to-income ratio
4. Determine risk category based on quantitative thresholds
5. Provide data-driven analysis without bias
6. Use only the provided calculation parameters""",

    "employment_agent": """You are an employment verification specialist.
Your role is to:
1. Simulate verification through multiple channels (LinkedIn, Glassdoor, web)
2. Assess employment stability based on tenure
3. Verify company legitimacy through known companies database
4. Determine employment risk factors
5. Make objective pass/fail determinations
6. Document verification sources""",

    "collateral_agent": """You are a collateral assessment specialist.
Your role is to:
1. Calculate Loan-to-Value (LTV) ratios accurately
2. Apply standard margin requirements (20%)
3. Assess collateral sufficiency
4. Determine collateral risk level
5. Provide clear coverage analysis
6. Make objective determinations based on thresholds""",

    "critique_agent": """You are a quality assurance and cross-verification specialist.
Your role is to:
1. Review all agent outputs for consistency
2. Identify logical inconsistencies or contradictions
3. Flag unusual patterns that need investigation
4. Assess overall confidence in the analysis
5. Provide actionable recommendations
6. Maintain objectivity and identify both strengths and concerns""",

    "final_decision_agent": """You are the final decision-making authority for loan applications.
Your role is to:
1. Synthesize all agent outputs into a unified risk score
2. Make final approval decisions based on objective criteria
3. Provide clear reasoning for decisions
4. Set appropriate conditions for conditional approvals
5. Offer constructive recommendations for rejected applications
6. Ensure decisions are fair, consistent, and well-documented"""
}

# System Processing Rules
PROCESSING_RULES = {
    "credit_score_formula": """
    Credit Score Calculation:
    1. Base Score: 500 points
    2. Repayment Component: repayment_score × 200 (max 200 points)
    3. Loan Penalty: min(number_of_loans × 15, 100) points deducted
    4. Income Component: min((monthly_income / 10000) × 50, 150) points
    5. Debt Burden Penalty: debt-to-income ratio × 100 points deducted
    6. Final Score: Clamped between 300 and 850
    
    Risk Categories:
    - Excellent: ≥700
    - Fair: 600-699
    - Poor: <600
    """,
    
    "ltv_calculation": """
    LTV Ratio Calculation:
    1. LTV = (Loan Amount / Collateral Value) × 100%
    2. Apply 20% margin: Effective Coverage = Collateral × 0.80
    3. Coverage Assessment:
       - Excellent: Coverage ≥ 120% of loan
       - Acceptable: Coverage = 100-119% of loan
       - Marginal: Coverage = 80-99% of loan
       - Insufficient: Coverage < 80% of loan
    """,
    
    "risk_score_calculation": """
    Overall Risk Score Components (weighted):
    1. Credit Risk: Based on credit score and DTI (40% weight)
    2. Employment Risk: Based on verification and stability (30% weight)
    3. Collateral Risk: Based on LTV and coverage (30% weight)
    
    Final Risk Thresholds:
    - Low Risk: <30%
    - Medium Risk: 30-50%
    - High Risk: >50%
    """,
    
    "decision_criteria": """
    Approval Decision Logic:
    
    APPROVED:
    - All verifications PASSED
    - Risk score < 30%
    - No critical inconsistencies
    
    CONDITIONAL:
    - 2+ verifications PASSED
    - Risk score 30-50%
    - Addressable concerns identified
    
    REJECTED:
    - <2 verifications PASSED
    - Risk score > 50%
    - Critical concerns present
    """
}

# System Logging Templates
LOG_TEMPLATES = {
    "info": "{timestamp} - {agent} - INFO - {message}",
    "warning": "{timestamp} - {agent} - WARNING - {message}",
    "error": "{timestamp} - {agent} - ERROR - {message}",
    "debug": "{timestamp} - {agent} - DEBUG - {message}"
}

# System Error Messages
ERROR_MESSAGES = {
    "missing_field": "Required field '{field}' is missing from application",
    "invalid_value": "Invalid value for field '{field}': {value}",
    "calculation_error": "Error calculating {metric}: {error}",
    "database_error": "Database operation failed: {error}",
    "agent_error": "Agent '{agent}' encountered error: {error}",
    "validation_failed": "Application validation failed: {reason}"
}

# System Status Messages
SYSTEM_MESSAGES = {
    "processing_started": "Starting application processing: {app_id}",
    "stage_greeting": "[{app_id}] Stage 1: Greeting",
    "stage_planning": "[{app_id}] Stage 2: Planning",
    "stage_verification": "[{app_id}] Stage 3: Parallel Verification",
    "stage_critique": "[{app_id}] Stage 4: Critique",
    "stage_decision": "[{app_id}] Stage 5: Final Decision",
    "processing_complete": "[{app_id}] Processing complete: Decision={decision}, Risk={risk:.2%}",
    "processing_error": "[{app_id}] Error processing application: {error}"
}

# Agent Coordination Rules
COORDINATION_RULES = {
    "parallel_agents": ["credit_history_agent", "employment_agent", "collateral_agent"],
    "sequential_flow": [
        "greeting_agent",
        "planner_agent",
        "parallel_verification",
        "critique_agent",
        "final_decision_agent"
    ],
    "timeout_seconds": {
        "greeting": 5,
        "planning": 10,
        "verification": 30,
        "critique": 15,
        "decision": 10
    },
    "retry_policy": {
        "max_retries": 3,
        "backoff_seconds": 2
    }
}
