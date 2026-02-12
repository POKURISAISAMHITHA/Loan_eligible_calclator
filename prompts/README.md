# Prompts Configuration

This folder contains all prompts, messages, and configuration for the Agentic AI Loan Eligibility Verification System.

## 📁 Structure

### `system_prompts.py`
**Internal system instructions and processing logic**

Contains:
- `SYSTEM_INSTRUCTIONS`: AI agent role definitions and behavior guidelines
- `PROCESSING_RULES`: Calculation formulas and business logic
- `LOG_TEMPLATES`: Logging format templates
- `ERROR_MESSAGES`: Error handling messages
- `SYSTEM_MESSAGES`: Internal status messages
- `COORDINATION_RULES`: Agent orchestration rules

**Usage:** Used internally by agents for processing logic and system operations.

### `user_prompts.py`
**User-facing messages and templates**

Contains:
- `GREETING_TEMPLATES`: Welcome messages for applicants
- `CREDIT_ANALYSIS_MESSAGES`: Credit score and risk messages
- `EMPLOYMENT_MESSAGES`: Employment verification messages
- `COLLATERAL_MESSAGES`: Collateral assessment messages
- `CRITIQUE_MESSAGES`: Quality assurance messages
- `DECISION_REASONING`: Approval/rejection explanations
- `PLANNER_MESSAGES`: Verification plan messages
- `STATUS_LABELS`: UI status labels
- `RISK_LABELS`: Risk level labels
- `VERIFICATION_LABELS`: Verification status labels

**Usage:** Used by agents to communicate with applicants and display results.

### `config.py`
**Configuration parameters and thresholds**

Contains:
- `RISK_THRESHOLDS`: Numerical thresholds for risk assessment
- `CREDIT_SCORE_PARAMS`: Credit score calculation parameters
- `LTV_CONFIG`: Loan-to-Value ratio configuration
- `KNOWN_COMPANIES`: Company database for verification
- `RISK_WEIGHTS`: Component weights for overall risk
- `STATUS_FLOW`: Application processing stages
- `VERIFICATION_CRITERIA`: Pass/fail criteria for each verification

**Usage:** Used by agents for calculations and decision-making logic.

## 🔧 How to Use

### Importing in Agent Code

```python
# Import specific components
from prompts import GREETING_TEMPLATES, RISK_THRESHOLDS

# Or import from specific modules
from prompts.system_prompts import SYSTEM_INSTRUCTIONS
from prompts.user_prompts import CREDIT_ANALYSIS_MESSAGES
from prompts.config import CREDIT_SCORE_PARAMS
```

### Example: Using Templates

```python
# Greeting message
from prompts import GREETING_TEMPLATES

message = GREETING_TEMPLATES["welcome_message"].format(
    applicant_name="John Doe",
    application_id="APP-123456"
)
```

### Example: Using Thresholds

```python
# Credit score evaluation
from prompts import RISK_THRESHOLDS, CREDIT_SCORE_PARAMS

if score >= RISK_THRESHOLDS["credit_score"]["excellent"]:
    risk_level = "Low"
elif score >= RISK_THRESHOLDS["credit_score"]["fair"]:
    risk_level = "Medium"
else:
    risk_level = "High"
```

## 🎨 Customization

### Changing Messages

Edit `user_prompts.py` to customize messages shown to applicants:

```python
GREETING_TEMPLATES = {
    "welcome_message": "Your custom greeting here..."
}
```

### Adjusting Thresholds

Edit `config.py` to change risk thresholds or calculation parameters:

```python
RISK_THRESHOLDS = {
    "credit_score": {
        "excellent": 720,  # Changed from 700
        "fair": 620,       # Changed from 600
        # ...
    }
}
```

### Modifying System Instructions

Edit `system_prompts.py` to change agent behavior:

```python
SYSTEM_INSTRUCTIONS = {
    "credit_history_agent": "Your custom instructions..."
}
```

## 📋 Best Practices

1. **Separation of Concerns**
   - Keep system logic in `system_prompts.py`
   - Keep user messages in `user_prompts.py`
   - Keep constants in `config.py`

2. **Template Variables**
   - Use `{variable_name}` for string formatting
   - Document required variables in docstrings
   - Validate variables before formatting

3. **Threshold Changes**
   - Test thoroughly after changing thresholds
   - Document business reasoning for changes
   - Update documentation if criteria change

4. **Version Control**
   - Track all changes to prompts in git
   - Use descriptive commit messages
   - Review prompt changes carefully

## 🔍 Validation

After making changes, validate:

1. **Syntax**: No Python syntax errors
2. **Imports**: All imports work correctly
3. **Templates**: All format variables are valid
4. **Logic**: Thresholds make business sense
5. **Testing**: Run test cases to verify behavior

## 📚 Documentation

For detailed prompt documentation, see:
- Main [README.md](../README.md) for system overview
- [DOCKER_GUIDE.md](../DOCKER_GUIDE.md) for deployment
- Agent files in `agents/` folder for usage examples

## 🤝 Contributing

When adding new prompts:

1. Determine if it's system, user, or config
2. Add to appropriate file
3. Export in `__init__.py`
4. Update this README
5. Test thoroughly
6. Document usage in agent code

---

**Note:** This centralized prompt structure makes it easy to:
- Update messages without changing code
- Maintain consistency across agents
- Support internationalization (future)
- A/B test different prompts
- Audit and review all messaging
