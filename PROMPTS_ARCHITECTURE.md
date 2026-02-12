# Configuration Architecture - Prompts Externalization

## ✅ **Prompts Successfully Moved Outside the System**

All text content, messages, thresholds, and configuration values have been externalized to `prompts.py` for easy customization and maintenance.

---

## 📁 **Architecture Overview**

### **Before:**
- Prompts and messages hardcoded in agent files
- Difficult to customize text
- Hard to maintain consistency
- No central configuration

### **After:**
- ✅ All prompts in `prompts.py`
- ✅ Easy to customize without touching code
- ✅ Consistent messaging across agents
- ✅ Centralized configuration management

---

## 🗂️ **What's in prompts.py**

### **1. Greeting Templates**
```python
GREETING_TEMPLATES = {
    "welcome_message": "Dear {applicant_name}..."
}
```

### **2. Credit Analysis Messages**
```python
CREDIT_ANALYSIS_MESSAGES = {
    "excellent_score": "Excellent credit score of {score:.0f}",
    "fair_score": "Fair credit score of {score:.0f}",
    ...
}
```

### **3. Employment Verification Messages**
```python
EMPLOYMENT_MESSAGES = {
    "verified_template": "Employment verified at {company}...",
    "stability_excellent": "Excellent (5+ years)",
    ...
}
```

### **4. Collateral Assessment Messages**
```python
COLLATERAL_MESSAGES = {
    "excellent_ltv": "Excellent LTV ratio of {ltv:.2%}...",
    ...
}
```

### **5. Critique Agent Messages**
```python
CRITIQUE_MESSAGES = {
    "low_risk_conflict_employment": "Low credit risk conflicts...",
    ...
}
```

### **6. Final Decision Templates**
```python
DECISION_REASONING = {
    "approved_intro": "After comprehensive analysis...",
    "approved_rationale": "The applicant demonstrates...",
    ...
}
```

### **7. Risk Thresholds**
```python
RISK_THRESHOLDS = {
    "credit_score": {"excellent": 700, "fair": 600, "poor": 300},
    "repayment_score": {"strong": 0.8, "acceptable": 0.6},
    "dti_ratio": {"healthy": 0.36, "moderate": 0.5},
    "employment_years": {"excellent": 5.0, "good": 3.0, "acceptable": 1.0},
    "ltv_ratio": {"standard": 0.80, "acceptable": 0.90},
    ...
}
```

### **8. Credit Score Parameters**
```python
CREDIT_SCORE_PARAMS = {
    "base_score": 500,
    "repayment_max": 200,
    "loan_penalty_per_loan": 15,
    ...
}
```

### **9. LTV Configuration**
```python
LTV_CONFIG = {
    "standard_ratio": 0.80,  # 80% LTV
    "coverage_thresholds": {
        "excellent": 1.2,
        "acceptable": 1.0,
        ...
    }
}
```

### **10. Known Companies Database**
```python
KNOWN_COMPANIES = {
    "microsoft", "google", "amazon", ...
}
```

---

## 🎯 **How Agents Use Prompts**

### **Example 1: Greeting Agent**
```python
from prompts import GREETING_TEMPLATES

message = GREETING_TEMPLATES["welcome_message"].format(
    applicant_name=applicant_name,
    application_id=application_id
)
```

### **Example 2: Credit History Agent**
```python
from prompts import CREDIT_ANALYSIS_MESSAGES, RISK_THRESHOLDS, CREDIT_SCORE_PARAMS

# Use thresholds
if credit_score >= RISK_THRESHOLDS["credit_score"]["excellent"]:
    message = CREDIT_ANALYSIS_MESSAGES["excellent_score"].format(score=credit_score)

# Use parameters
base_score = CREDIT_SCORE_PARAMS["base_score"]
```

### **Example 3: Employment Agent**
```python
from prompts import EMPLOYMENT_MESSAGES, KNOWN_COMPANIES, RISK_THRESHOLDS

# Check company database
if company.lower() in KNOWN_COMPANIES:
    verified = True

# Use thresholds
if years >= RISK_THRESHOLDS["employment_years"]["excellent"]:
    stability = EMPLOYMENT_MESSAGES["stability_excellent"]
```

---

## 🔧 **How to Customize**

### **To Change Messages:**

1. Open `prompts.py`
2. Find the relevant section (e.g., `GREETING_TEMPLATES`)
3. Edit the message text
4. Save - no code changes needed!

### **To Adjust Thresholds:**

```python
# In prompts.py
RISK_THRESHOLDS = {
    "credit_score": {
        "excellent": 750,  # Changed from 700
        "fair": 650,       # Changed from 600
        "poor": 300
    }
}
```

### **To Modify Credit Scoring:**

```python
# In prompts.py
CREDIT_SCORE_PARAMS = {
    "base_score": 550,        # Changed from 500
    "repayment_max": 250,     # Changed from 200
    "loan_penalty_per_loan": 20,  # Changed from 15
    ...
}
```

### **To Add New Companies:**

```python
# In prompts.py
KNOWN_COMPANIES = {
    "microsoft", "google", "amazon",
    "your_company_name",  # Add here
    ...
}
```

---

## ✅ **Benefits**

### **1. Easy Customization**
- Change messages without touching code
- Update thresholds in one place
- Modify all agent behavior centrally

### **2. Better Maintainability**
- All configuration in one file
- Easy to review and update
- No hunting through code files

### **3. Consistency**
- Same message formats everywhere
- Consistent thresholds across agents
- Unified terminology

### **4. Internationalization Ready**
- Easy to add multiple languages
- Just create `prompts_es.py`, `prompts_fr.py`, etc.
- Switch based on user preference

### **5. A/B Testing Friendly**
- Test different message variants
- Experiment with thresholds
- Easy rollback if needed

---

## 📊 **What Changed in Each Agent**

### **✅ greeting_agent.py**
- Imports `GREETING_TEMPLATES`
- Uses template for welcome message

### **✅ planner_agent.py**
- Imports `PLANNER_MESSAGES`
- Uses predefined plan steps
- Uses duration messages

### **✅ credit_history_agent.py**
- Imports `CREDIT_ANALYSIS_MESSAGES`, `RISK_THRESHOLDS`, `CREDIT_SCORE_PARAMS`
- All messages from prompts
- All thresholds configurable
- Calculation parameters external

### **✅ employment_agent.py**
- Imports `EMPLOYMENT_MESSAGES`, `KNOWN_COMPANIES`, `RISK_THRESHOLDS`
- All messages from prompts
- Company database external
- Stability thresholds configurable

### **✅ collateral_agent.py**
- Imports `COLLATERAL_MESSAGES`, `LTV_CONFIG`, `RISK_THRESHOLDS`
- All messages from prompts
- LTV ratio configurable
- Coverage thresholds external

---

## 🚀 **Quick Start - Customization Examples**

### **Example 1: Make Credit Scoring More Lenient**
```python
# In prompts.py
RISK_THRESHOLDS["credit_score"]["excellent"] = 680  # Lower from 700
RISK_THRESHOLDS["credit_score"]["fair"] = 580      # Lower from 600
```

### **Example 2: Change Welcome Message**
```python
# In prompts.py
GREETING_TEMPLATES["welcome_message"] = """Hello {applicant_name}!

Your loan application {application_id} is being processed by our AI team.
We'll get back to you shortly!

Cheers,
Your Friendly Loan Team"""
```

### **Example 3: Adjust LTV Requirements**
```python
# In prompts.py
LTV_CONFIG["standard_ratio"] = 0.85  # More lenient (was 0.80)
```

---

## 📝 **File Structure**

```
loan_approval/
├── prompts.py               # ⭐ All prompts and configuration
├── agents/
│   ├── greeting_agent.py    # Uses GREETING_TEMPLATES
│   ├── planner_agent.py     # Uses PLANNER_MESSAGES
│   ├── credit_history_agent.py  # Uses CREDIT_*, RISK_THRESHOLDS
│   ├── employment_agent.py  # Uses EMPLOYMENT_*, KNOWN_COMPANIES
│   ├── collateral_agent.py  # Uses COLLATERAL_*, LTV_CONFIG
│   ├── critique_agent.py    # Uses CRITIQUE_MESSAGES
│   └── final_decision_agent.py  # Uses DECISION_REASONING
└── ...
```

---

## 🎉 **Result**

Your system is now **highly configurable** with:
- ✅ All text externalized
- ✅ All thresholds configurable
- ✅ Easy to maintain
- ✅ Ready for customization
- ✅ Production-ready architecture

**Just edit `prompts.py` to customize the entire system!** 🚀
