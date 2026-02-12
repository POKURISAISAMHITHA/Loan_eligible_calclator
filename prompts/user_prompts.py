"""
User-Facing Prompts and Messages
All templates, messages, and text that users will see
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

# Credit Analysis User Messages
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

# Employment Verification User Messages
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

# Collateral Assessment User Messages
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

# Critique Agent User Messages
CRITIQUE_MESSAGES = {
    # Inconsistency Messages
    "low_risk_conflict_employment": "Low credit risk conflicts with concerning employment stability",
    "high_risk_excellent_employment": "High credit risk despite excellent employment history warrants investigation",
    "critical_high_risk_no_collateral": "Critical: High credit risk combined with insufficient collateral",
    "low_risk_high_ltv": "Low credit risk applicant has high LTV ratio - unusual pattern",
    "all_passed_high_dti": "All verifications passed but DTI ratio is concerning",
    "all_failed_confirmed": "All verifications failed - confirms high-risk profile",
    
    # Recommendation Messages
    "debt_consolidation": "Consider debt consolidation before reapplying",
    "credit_counseling": "Recommend credit counseling to improve credit profile",
    "reapply_after_employment": "Recommend reapplying after 1+ years of employment",
    "additional_documentation": "Additional employment documentation required",
    "larger_down_payment": "Collateral shortfall of {shortfall:.0f}% - consider larger down payment",
    "cosigner_or_collateral": "Consider co-signer or additional collateral",
    "manual_review": "Manual review recommended due to identified inconsistencies",
    "proceed_standard": "All verifications consistent - proceed with standard approval process",
    
    # Summary Messages
    "consistent_summary": "All agent outputs are consistent and coherent. Confidence score: {confidence:.2%}. Credit: {risk} risk, Employment: {employment_status}, Collateral: {collateral_status}.",
    "inconsistencies_summary": "Found {count} inconsistency(ies) requiring attention. Confidence score: {confidence:.2%}. Recommend careful review of highlighted areas."
}

# Final Decision User Messages
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

# Planner Agent User Messages
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

# Status Labels for UI
STATUS_LABELS = {
    "pending": "Pending Review",
    "in_progress": "In Progress",
    "completed": "Completed",
    "approved": "Approved",
    "conditional": "Conditionally Approved",
    "rejected": "Rejected"
}

# Risk Level Labels for UI
RISK_LABELS = {
    "low": "Low Risk",
    "medium": "Medium Risk",
    "high": "High Risk"
}

# Verification Status Labels
VERIFICATION_LABELS = {
    "passed": "Passed ✓",
    "failed": "Failed ✗",
    "pending": "Pending...",
    "in_progress": "In Progress..."
}
