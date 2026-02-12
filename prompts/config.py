"""
Configuration Parameters and Thresholds
Numerical constants, thresholds, and business rules
"""

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
    "margin": 0.20,  # 20% margin requirement
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

# Weight Configuration for Risk Calculation
RISK_WEIGHTS = {
    "credit": 0.4,      # 40% weight
    "employment": 0.3,  # 30% weight
    "collateral": 0.3   # 30% weight
}

# Application Status Flow
STATUS_FLOW = [
    "received",
    "greeting",
    "planning",
    "verification",
    "critique",
    "final_decision",
    "completed"
]

# Verification Pass/Fail Criteria
VERIFICATION_CRITERIA = {
    "credit": {
        "pass_threshold": 600,  # Minimum credit score
        "dti_threshold": 0.5    # Maximum DTI ratio
    },
    "employment": {
        "min_years": 1.0,       # Minimum employment years
        "verification_required": True
    },
    "collateral": {
        "max_ltv": 0.90,        # Maximum LTV ratio
        "min_coverage": 0.8     # Minimum coverage after margin
    }
}
