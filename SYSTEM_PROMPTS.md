# System Prompts and Configuration Reference

Complete reference guide for all prompts, messages, and configuration parameters used in the Agentic AI Loan Eligibility Verification System.

---

## 📋 Table of Contents

1. [Greeting Templates](#greeting-templates)
2. [Credit Analysis Messages](#credit-analysis-messages)
3. [Employment Verification Messages](#employment-verification-messages)
4. [Collateral Assessment Messages](#collateral-assessment-messages)
5. [Critique Agent Messages](#critique-agent-messages)
6. [Final Decision Templates](#final-decision-templates)
7. [Planner Messages](#planner-messages)
8. [Risk Thresholds](#risk-thresholds)
9. [Credit Score Parameters](#credit-score-parameters)
10. [LTV Configuration](#ltv-configuration)
11. [Known Companies Database](#known-companies-database)
12. [System Messages](#system-messages)

---

## 1. Greeting Templates

### Welcome Message Template

```
Dear {applicant_name},

Thank you for submitting your loan application. We have received your request and assigned it the reference number: {application_id}.

Our AI-powered verification system is now processing your application through multiple specialized agents to ensure a comprehensive and fair assessment.

You will receive a detailed response shortly.

Best regards,
Loan Verification Team
```

**Variables:**
- `{applicant_name}` - Full name of the applicant
- `{application_id}` - Unique application reference number (e.g., APP-20260212-ABC12345)

---

## 2. Credit Analysis Messages

### Credit Score Messages

| Score Range | Message Template |
|-------------|-----------------|
| ≥700 | `"Excellent credit score of {score:.0f}"` |
| 600-699 | `"Fair credit score of {score:.0f}"` |
| <600 | `"Below-average credit score of {score:.0f}"` |

### Repayment History Messages

| Score Range | Message Template |
|-------------|-----------------|
| ≥0.8 | `"strong repayment history ({score:.2%})"` |
| 0.6-0.79 | `"acceptable repayment history ({score:.2%})"` |
| <0.6 | `"concerning repayment history ({score:.2%})"` |

### Existing Loans Messages

| Loan Count | Message Template |
|------------|-----------------|
| 0 | `"no existing loans"` |
| 1-2 | `"{count} existing loans (manageable)"` |
| 3+ | `"{count} existing loans (high debt burden)"` |

### Debt-to-Income (DTI) Messages

| DTI Ratio | Message Template |
|-----------|-----------------|
| <0.36 | `"healthy DTI ratio of {ratio:.2%}"` |
| 0.36-0.49 | `"moderate DTI ratio of {ratio:.2%}"` |
| ≥0.5 | `"high DTI ratio of {ratio:.2%}"` |

### Analysis Template

```
Applicant shows {details}. Risk level: {risk_level}.
```

**Variables:**
- `{details}` - Comma-separated list of analysis points
- `{risk_level}` - "Low", "Medium", or "High"

---

## 3. Employment Verification Messages

### Employment Status Messages

```python
"Employment verified at {company} for {years} years"
"Unable to fully verify employment history"
"Company {company} verified through multiple sources"
"Company verification inconclusive"
```

### Employment Stability Categories

| Years of Employment | Stability Label |
|--------------------|----------------|
| ≥5.0 years | `"Excellent (5+ years)"` |
| 3.0-4.9 years | `"Good (3-5 years)"` |
| 1.0-2.9 years | `"Acceptable (1-3 years)"` |
| <1.0 year | `"Concerning (< 1 year)"` |

### Employment Duration Messages

| Years | Message |
|-------|---------|
| ≥3.0 | `"Demonstrates strong employment commitment"` |
| 1.0-2.9 | `"Shows reasonable employment history"` |
| <1.0 | `"Limited employment tenure raises concerns"` |

---

## 4. Collateral Assessment Messages

### Collateral Value Statement

```
"Collateral value: ${value:,.2f}"
```

### LTV Ratio Messages

| LTV Ratio | Message Template |
|-----------|-----------------|
| ≤0.80 | `"Excellent LTV ratio of {ltv:.2%} (well within {threshold:.0%} threshold)"` |
| 0.81-0.90 | `"Acceptable LTV ratio of {ltv:.2%} (slightly above optimal)"` |
| >0.90 | `"High LTV ratio of {ltv:.2%} (exceeds recommended threshold)"` |

### Margin Applied Message

```
"After applying {margin:.0%} margin, effective coverage is ${coverage:,.2f} ({percentage:.2%} of loan amount)"
```

### Sufficiency Messages

```python
# If sufficient:
"Collateral is sufficient with ${surplus:,.2f} surplus after margin"

# If insufficient:
"Collateral is insufficient by ${shortfall:,.2f} after applying margin"
```

### Risk Assessment Messages

| Coverage Ratio | Message |
|---------------|---------|
| ≥1.2 | `"Low collateral risk with strong coverage"` |
| 1.0-1.19 | `"Acceptable collateral coverage"` |
| 0.8-0.99 | `"Marginal collateral coverage - increased risk"` |
| <0.8 | `"Insufficient collateral coverage - high risk"` |

---

## 5. Critique Agent Messages

### Inconsistency Messages

```python
"Low credit risk conflicts with concerning employment stability"

"High credit risk despite excellent employment history warrants investigation"

"Critical: High credit risk combined with insufficient collateral"

"Low credit risk applicant has high LTV ratio - unusual pattern"

"All verifications passed but DTI ratio is concerning"

"All verifications failed - confirms high-risk profile"
```

### Recommendation Messages

```python
"Consider debt consolidation before reapplying"

"Recommend credit counseling to improve credit profile"

"Recommend reapplying after 1+ years of employment"

"Additional employment documentation required"

"Collateral shortfall of {shortfall:.0f}% - consider larger down payment"

"Consider co-signer or additional collateral"

"Manual review recommended due to identified inconsistencies"

"All verifications consistent - proceed with standard approval process"
```

### Summary Templates

#### Consistent Output Summary
```
All agent outputs are consistent and coherent. Confidence score: {confidence:.2%}. Credit: {risk} risk, Employment: {employment_status}, Collateral: {collateral_status}.
```

#### Inconsistencies Found Summary
```
Found {count} inconsistency(ies) requiring attention. Confidence score: {confidence:.2%}. Recommend careful review of highlighted areas.
```

---

## 6. Final Decision Templates

### Decision Introduction Messages

#### Approved
```
After comprehensive multi-agent analysis, the loan application has been approved with an overall risk score of {risk:.2%}.
```

#### Conditional
```
After comprehensive multi-agent analysis, the loan application has been conditionally approved with an overall risk score of {risk:.2%}.
```

#### Rejected
```
After comprehensive multi-agent analysis, the loan application has been rejected with an overall risk score of {risk:.2%}.
```

### Decision Rationale Messages

#### Approved Rationale
```
The applicant demonstrates strong creditworthiness across all verification dimensions. Low risk profile ({risk:.2%}) and consistent positive indicators support approval.
```

#### Conditional Rationale
```
The applicant shows potential for approval with moderate risk ({risk:.2%}). Conditional approval is granted subject to meeting the following requirements:
```

#### Rejected Rationale
```
The application presents high risk ({risk:.2%}) with multiple verification concerns. The applicant is encouraged to address the identified issues and reapply in the future.
```

### Section Headers

```python
conditions_header = "\n\nConditional Requirements:"
recommendations_header = "\n\nRecommendations:"
```

---

## 7. Planner Messages

### Verification Plan Steps

```python
[
    "Step 1: Credit History Verification",
    "Step 2: Employment Verification",
    "Step 3: Collateral Assessment",
    "Step 4: Cross-verification and Critique",
    "Step 5: Final Decision Making"
]
```

### Verification Step Details

#### Credit Step
```
"Analyze credit profile: {loans} existing loans, repayment score {score}, income ${income:,.2f}"
```

#### Employment Step
```
"Verify employment at {company} for {years} years"
```

#### Collateral Step
```
"Assess collateral value ${collateral:,.2f} against loan amount ${loan:,.2f}"
```

#### Critique Step
```
"Cross-verify all agent outputs for consistency and accuracy"
```

#### Decision Step
```
"Synthesize all verification results into final approval decision"
```

### Duration Estimates

| Complexity Level | Duration |
|-----------------|----------|
| Low (<2) | `"2-3 minutes"` |
| Medium (2-4) | `"3-5 minutes"` |
| High (>4) | `"5-7 minutes"` |

**Complexity Calculation:**
```python
complexity_score = (existing_loans * 0.5) + ((1 - repayment_score) * 2) + (1 if collateral < loan else 0)
```

---

## 8. Risk Thresholds

### Credit Score Thresholds

| Category | Threshold |
|----------|-----------|
| Excellent | ≥700 |
| Fair | 600-699 |
| Poor | <600 |

### Repayment Score Thresholds

| Category | Threshold |
|----------|-----------|
| Strong | ≥0.8 |
| Acceptable | 0.6-0.79 |
| Concerning | <0.6 |

### Debt-to-Income (DTI) Ratio Thresholds

| Category | Threshold |
|----------|-----------|
| Healthy | <0.36 (36%) |
| Moderate | 0.36-0.49 (36-49%) |
| High | ≥0.5 (50%) |

### Employment Years Thresholds

| Category | Threshold |
|----------|-----------|
| Excellent | ≥5.0 years |
| Good | 3.0-4.9 years |
| Acceptable | 1.0-2.9 years |
| Concerning | <1.0 year |

### Loan-to-Value (LTV) Ratio Thresholds

| Category | Threshold |
|----------|-----------|
| Standard | ≤0.80 (80%) |
| Acceptable | 0.81-0.90 (81-90%) |
| High | >0.90 (90%) |

### Overall Risk Score Thresholds

| Category | Threshold | Typical Decision |
|----------|-----------|------------------|
| Low | ≤0.30 (30%) | Approved |
| Medium | 0.31-0.50 (31-50%) | Conditional |
| High | >0.50 (50%) | Rejected |

---

## 9. Credit Score Parameters

### Calculation Formula

```python
credit_score = base_score 
             + (repayment_score * repayment_max)
             - min(existing_loans * loan_penalty_per_loan, loan_penalty_max)
             + min((income/loan_amount) * income_ratio_multiplier, income_component_max)
             + max(0, debt_burden_base - (debt_burden * debt_burden_multiplier))
```

### Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `base_score` | 500 | Starting credit score |
| `repayment_max` | 200 | Maximum points from repayment history |
| `loan_penalty_per_loan` | 15 | Penalty per existing loan |
| `loan_penalty_max` | 100 | Maximum loan penalty |
| `income_ratio_multiplier` | 50 | Multiplier for income-to-loan ratio |
| `income_component_max` | 150 | Maximum points from income |
| `debt_burden_base` | 100 | Base debt burden component |
| `debt_burden_multiplier` | 10 | Debt burden penalty multiplier |
| `score_min` | 300 | Minimum credit score |
| `score_max` | 850 | Maximum credit score |

### Example Calculation

**Input:**
- Income: $75,000
- Loan Amount: $250,000
- Existing Loans: 2
- Repayment Score: 0.85

**Calculation:**
```
Base: 500
Repayment: 0.85 × 200 = 170
Loan Penalty: 2 × 15 = -30
Income Component: min((75000/250000) × 50, 150) = 15
Debt Burden: max(0, 100 - ((2/(75000/10000)) × 10)) = 73.33

Credit Score = 500 + 170 - 30 + 15 + 73.33 = 728.33
```

---

## 10. LTV Configuration

### Standard LTV Ratio

```
0.80 (80%)
```

This means the bank will lend up to 80% of the collateral value.

### Coverage Thresholds

| Category | Ratio | Description |
|----------|-------|-------------|
| Excellent | ≥1.2 | Collateral covers 120%+ of loan after margin |
| Acceptable | 1.0-1.19 | Collateral covers 100-119% of loan |
| Marginal | 0.8-0.99 | Collateral covers 80-99% of loan |
| Insufficient | <0.8 | Collateral covers less than 80% |

### LTV Calculation Example

**Input:**
- Loan Amount: $250,000
- Collateral Value: $300,000

**Calculation:**
```
LTV Ratio = Loan Amount / Collateral Value
          = $250,000 / $300,000
          = 0.833 (83.3%)

Effective Collateral = Collateral Value × 0.80
                     = $300,000 × 0.80
                     = $240,000

Effective Coverage = Effective Collateral / Loan Amount
                   = $240,000 / $250,000
                   = 0.96 (96%)

Result: Marginal coverage (insufficient - needs $10,000 more)
```

---

## 11. Known Companies Database

### Verified Companies List

```
microsoft, google, amazon, apple, meta, facebook,
tesla, nvidia, intel, ibm, oracle, salesforce,
adobe, netflix, uber, airbnb, twitter, linkedin,
tech corp, global solutions, innovation labs, digital systems,
accenture, deloitte, pwc, ey, kpmg, mckinsey,
jp morgan, goldman sachs, morgan stanley, citigroup
```

### Usage

Companies in this list are automatically verified during employment checks. Companies not in the list still receive verification but with lower confidence.

**To Add Companies:**
Edit `prompts.py` and add to `KNOWN_COMPANIES` set.

---

## 12. System Messages

### Processing Stage Messages

```python
"Starting application processing: {app_id}"

"[{app_id}] Stage 1: Greeting"
"[{app_id}] Stage 2: Planning"
"[{app_id}] Stage 3: Parallel Verification"
"[{app_id}] Stage 4: Critique"
"[{app_id}] Stage 5: Final Decision"

"[{app_id}] Processing complete: Decision={decision}, Risk={risk:.2%}"

"[{app_id}] Error processing application: {error}"
```

### Variables

- `{app_id}` - Application ID (e.g., APP-20260212-ABC12345)
- `{decision}` - Final decision (Approved/Rejected/Conditional)
- `{risk}` - Risk score percentage
- `{error}` - Error message if processing fails

---

## 📊 Risk Scoring Summary

### Overall Risk Score Calculation

```python
# Credit Risk Component (0-0.4)
credit_risk = {
    "Low": 0.1,
    "Medium": 0.25,
    "High": 0.4
}[risk_category]

# DTI Risk (0-0.2)
dti_risk = min(dti_ratio * 0.3, 0.2)

# Employment Risk (0-0.25)
employment_risk = {
    "passed": 0.05,
    "verified_only": 0.15,
    "failed": 0.25
}

# Collateral Risk (0-0.25)
collateral_risk = {
    "passed": 0.05,
    "sufficient_only": 0.15,
    "failed": 0.25
}

# Critique Confidence Impact (0-0.1)
critique_risk = (1 - confidence_score) * 0.1

# Total Risk Score
total_risk = credit_risk + dti_risk + employment_risk + collateral_risk + critique_risk
```

### Risk Score to Decision Mapping

```python
if risk_score <= 0.3 and passed_count >= 3:
    decision = "Approved"

elif risk_score <= 0.5 and passed_count >= 2:
    decision = "Conditional"
    
else:
    decision = "Rejected"
```

---

## 🎯 Quick Reference Tables

### Decision Matrix

| Risk Score | Verifications Passed | Decision |
|------------|---------------------|----------|
| ≤0.30 | 3/3 | Approved |
| 0.31-0.50 | 2+/3 | Conditional |
| >0.50 | Any | Rejected |
| Any | 0-1/3 | Rejected |

### Agent Pass/Fail Criteria

| Agent | Pass Criteria |
|-------|--------------|
| Credit History | (Low or Medium risk) AND (DTI < 50%) |
| Employment | Verified AND Company Verified AND Years ≥ 1.0 |
| Collateral | Sufficient AND Effective Coverage ≥ 100% |

---

## 📝 Customization Guide

### To Change Approval Thresholds

Edit in `prompts.py`:
```python
RISK_THRESHOLDS = {
    "credit_score": {
        "excellent": 720,  # Change from 700
        "fair": 620,       # Change from 600
    }
}
```

### To Modify Messages

Edit in `prompts.py`:
```python
GREETING_TEMPLATES["welcome_message"] = """
Your custom welcome message here with {applicant_name} and {application_id} placeholders.
"""
```

### To Adjust Risk Calculation

Edit in `prompts.py`:
```python
CREDIT_SCORE_PARAMS["base_score"] = 550  # More lenient
LTV_CONFIG["standard_ratio"] = 0.85      # Higher LTV allowed
```

---

## 🔗 Related Files

- **Configuration:** `prompts.py`
- **Models:** `models.py`
- **Agents:** `agents/*.py`
- **Architecture Doc:** `PROMPTS_ARCHITECTURE.md`

---

**Last Updated:** February 12, 2026  
**Version:** 1.0.0  
**System:** Agentic AI Loan Eligibility Verification System
