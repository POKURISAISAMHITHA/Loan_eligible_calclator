"""
Prompts and Templates Configuration
All agent prompts, messages, and text templates
"""

# Greeting Agent Templates
GREETING_TEMPLATES = {
    "welcome_message": """Dear {applicant_name},

Thank you for submitting your loan application. We have received your request and assigned it the reference number: {application_id}.

Our AI-powered verification system is now processing your application through multiple specialized agents to ensure a comprehensive and fair assessment.

You will receive a detailed response shortly.

Best regards,
Loan Verification Team"""
}

# Credit Analysis Messages
CREDIT_ANALYSIS_MESSAGES = {
    "excellent_score": "Excellent credit score of {score:.0f}",
    "fair_score": "Fair credit score of {score:.0f}",
    "below_average_score": "Below-average credit score of {score:.0f}",
    
    "strong_repayment": "strong repayment history ({score:.2%})",
    "acceptable_repayment": "acceptable repayment history ({score:.2%})",
    "concerning_repayment": "concerning repayment history ({score:.2%})",
    
    "no_loans": "no existing loans",
    "manageable_loans": "{count} existing loans (manageable)",
    "high_debt_burden": "{count} existing loans (high debt burden)",
    
    "healthy_dti": "healthy DTI ratio of {ratio:.2%}",
    "moderate_dti": "moderate DTI ratio of {ratio:.2%}",
    "high_dti": "high DTI ratio of {ratio:.2%}",
    
    "analysis_template": "Applicant shows {details}. Risk level: {risk_level}."
}

# Employment Verification Messages
EMPLOYMENT_MESSAGES = {
    "verified_template": "Employment verified at {company} for {years} years",
    "unable_to_verify": "Unable to fully verify employment history",
    "company_verified": "Company {company} verified through multiple sources",
    "company_inconclusive": "Company verification inconclusive",
    
    "stability_excellent": "Excellent (5+ years)",
    "stability_good": "Good (3-5 years)",
    "stability_acceptable": "Acceptable (1-3 years)",
    "stability_concerning": "Concerning (< 1 year)",
    
    "strong_commitment": "Demonstrates strong employment commitment",
    "reasonable_history": "Shows reasonable employment history",
    "limited_tenure": "Limited employment tenure raises concerns"
}

# Collateral Assessment Messages
COLLATERAL_MESSAGES = {
    "value_statement": "Collateral value: ${value:,.2f}",
    
    "excellent_ltv": "Excellent LTV ratio of {ltv:.2%} (well within {threshold:.0%} threshold)",
    "acceptable_ltv": "Acceptable LTV ratio of {ltv:.2%} (slightly above optimal)",
    "high_ltv": "High LTV ratio of {ltv:.2%} (exceeds recommended threshold)",
    
    "margin_applied": "After applying {margin:.0%} margin, effective coverage is ${coverage:,.2f} ({percentage:.2%} of loan amount)",
    
    "sufficient_with_surplus": "Collateral is sufficient with ${surplus:,.2f} surplus after margin",
    "insufficient_shortfall": "Collateral is insufficient by ${shortfall:,.2f} after applying margin",
    
    "low_risk": "Low collateral risk with strong coverage",
    "acceptable_coverage": "Acceptable collateral coverage",
    "marginal_coverage": "Marginal collateral coverage - increased risk",
    "insufficient_coverage": "Insufficient collateral coverage - high risk"
}

# Critique Agent Messages
CRITIQUE_MESSAGES = {
    "low_risk_conflict_employment": "Low credit risk conflicts with concerning employment stability",
    "high_risk_excellent_employment": "High credit risk despite excellent employment history warrants investigation",
    "critical_high_risk_no_collateral": "Critical: High credit risk combined with insufficient collateral",
    "low_risk_high_ltv": "Low credit risk applicant has high LTV ratio - unusual pattern",
    "all_passed_high_dti": "All verifications passed but DTI ratio is concerning",
    "all_failed_confirmed": "All verifications failed - confirms high-risk profile",
    
    "debt_consolidation": "Consider debt consolidation before reapplying",
    "credit_counseling": "Recommend credit counseling to improve credit profile",
    "reapply_after_employment": "Recommend reapplying after 1+ years of employment",
    "additional_documentation": "Additional employment documentation required",
    "larger_down_payment": "Collateral shortfall of {shortfall:.0f}% - consider larger down payment",
    "cosigner_or_collateral": "Consider co-signer or additional collateral",
    "manual_review": "Manual review recommended due to identified inconsistencies",
    "proceed_standard": "All verifications consistent - proceed with standard approval process",
    
    "consistent_summary": "All agent outputs are consistent and coherent. Confidence score: {confidence:.2%}. Credit: {risk} risk, Employment: {employment_status}, Collateral: {collateral_status}.",
    "inconsistencies_summary": "Found {count} inconsistency(ies) requiring attention. Confidence score: {confidence:.2%}. Recommend careful review of highlighted areas."
}

# Final Decision Messages
DECISION_REASONING = {
    "approved_intro": "After comprehensive multi-agent analysis, the loan application has been approved with an overall risk score of {risk:.2%}.",
    "conditional_intro": "After comprehensive multi-agent analysis, the loan application has been conditionally approved with an overall risk score of {risk:.2%}.",
    "rejected_intro": "After comprehensive multi-agent analysis, the loan application has been rejected with an overall risk score of {risk:.2%}.",
    
    "approved_rationale": "The applicant demonstrates strong creditworthiness across all verification dimensions. Low risk profile ({risk:.2%}) and consistent positive indicators support approval.",
    
    "conditional_rationale": "The applicant shows potential for approval with moderate risk ({risk:.2%}). Conditional approval is granted subject to meeting the following requirements:",
    
    "rejected_rationale": "The application presents high risk ({risk:.2%}) with multiple verification concerns. The applicant is encouraged to address the identified issues and reapply in the future.",
    
    "conditions_header": "\n\nConditional Requirements:",
    "recommendations_header": "\n\nRecommendations:"
}

# Planner Agent Messages
PLANNER_MESSAGES = {
    "verification_plan": [
        "Step 1: Credit History Verification",
        "Step 2: Employment Verification",
        "Step 3: Collateral Assessment",
        "Step 4: Cross-verification and Critique",
        "Step 5: Final Decision Making"
    ],
    
    "credit_step": "Analyze credit profile: {loans} existing loans, repayment score {score}, income ${income:,.2f}",
    "employment_step": "Verify employment at {company} for {years} years",
    "collateral_step": "Assess collateral value ${collateral:,.2f} against loan amount ${loan:,.2f}",
    "critique_step": "Cross-verify all agent outputs for consistency and accuracy",
    "decision_step": "Synthesize all verification results into final approval decision",
    
    "duration_low": "2-3 minutes",
    "duration_medium": "3-5 minutes",
    "duration_high": "5-7 minutes"
}

# Risk Level Thresholds and Labels
RISK_THRESHOLDS = {
    "credit_score": {
        "excellent": 700,
        "fair": 600,
        "poor": 300
    },
    "repayment_score": {
        "strong": 0.8,
        "acceptable": 0.6,
        "concerning": 0.0
    },
    "dti_ratio": {
        "healthy": 0.36,
        "moderate": 0.5,
        "high": 1.0
    },
    "employment_years": {
        "excellent": 5.0,
        "good": 3.0,
        "acceptable": 1.0,
        "concerning": 0.0
    },
    "ltv_ratio": {
        "standard": 0.80,
        "acceptable": 0.90,
        "high": 1.0
    },
    "risk_score": {
        "low": 0.3,
        "medium": 0.5,
        "high": 1.0
    }
}

# Credit Score Calculation Constants
CREDIT_SCORE_PARAMS = {
    "base_score": 500,
    "repayment_max": 200,
    "loan_penalty_per_loan": 15,
    "loan_penalty_max": 100,
    "income_ratio_multiplier": 50,
    "income_component_max": 150,
    "debt_burden_base": 100,
    "debt_burden_multiplier": 10,
    "score_min": 300,
    "score_max": 850
}

# LTV Configuration
LTV_CONFIG = {
    "standard_ratio": 0.80,  # 80% LTV
    "coverage_thresholds": {
        "excellent": 1.2,
        "acceptable": 1.0,
        "marginal": 0.8,
        "insufficient": 0.0
    }
}

# Known Companies Database (for employment simulation)
KNOWN_COMPANIES = {
    "microsoft", "google", "amazon", "apple", "meta", "facebook",
    "tesla", "nvidia", "intel", "ibm", "oracle", "salesforce",
    "adobe", "netflix", "uber", "airbnb", "twitter", "linkedin",
    "tech corp", "global solutions", "innovation labs", "digital systems",
    "accenture", "deloitte", "pwc", "ey", "kpmg", "mckinsey",
    "jp morgan", "goldman sachs", "morgan stanley", "citigroup"
}

# System Messages
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
