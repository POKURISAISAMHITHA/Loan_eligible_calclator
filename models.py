"""
Pydantic Models for Loan Application System
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RiskCategory(str, Enum):
    """Risk category enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class LoanDecision(str, Enum):
    """Loan decision enumeration"""
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CONDITIONAL = "Conditional"


class LoanApplicationRequest(BaseModel):
    """Incoming loan application request"""
    name: str = Field(..., min_length=1, description="Applicant's full name")
    income: float = Field(..., gt=0, description="Annual income in USD")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    existing_loans: int = Field(..., ge=0, description="Number of existing loans")
    repayment_score: float = Field(..., ge=0, le=1, description="Repayment history score (0-1)")
    employment_years: float = Field(..., ge=0, description="Years of employment")
    company_name: str = Field(..., min_length=1, description="Current employer name")
    collateral_value: float = Field(..., ge=0, description="Collateral value in USD")

    @validator('repayment_score')
    def validate_repayment_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Repayment score must be between 0 and 1')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "income": 75000.0,
                "loan_amount": 250000.0,
                "existing_loans": 2,
                "repayment_score": 0.85,
                "employment_years": 5.0,
                "company_name": "Tech Corp",
                "collateral_value": 300000.0
            }
        }


class GreetingResponse(BaseModel):
    """Response from greeting agent"""
    message: str
    application_id: str
    timestamp: str


class PlannerResponse(BaseModel):
    """Response from planner agent"""
    plan: list[str]
    verification_steps: Dict[str, str]
    estimated_duration: str


class CreditHistoryResponse(BaseModel):
    """Response from credit history agent"""
    credit_score: float
    risk_category: RiskCategory
    debt_to_income_ratio: float
    analysis: str
    passed: bool


class EmploymentVerificationResponse(BaseModel):
    """Response from employment verification agent"""
    employment_verified: bool
    company_verified: bool
    employment_stability: str
    years_employed: float
    analysis: str
    passed: bool


class CollateralVerificationResponse(BaseModel):
    """Response from collateral verification agent"""
    collateral_sufficient: bool
    loan_to_value_ratio: float
    margin_applied: float
    effective_coverage: float
    analysis: str
    passed: bool


class CritiqueResponse(BaseModel):
    """Response from critique agent"""
    inconsistencies_found: list[str]
    recommendations: list[str]
    confidence_score: float
    critique_summary: str


class FinalDecisionResponse(BaseModel):
    """Response from final decision agent"""
    decision: LoanDecision
    risk_score: float
    reasoning: str
    conditions: Optional[list[str]] = None


class LoanApplicationResponse(BaseModel):
    """Final API response"""
    decision: str
    risk_score: float
    reasoning: str
    agent_summary: Dict[str, Any]
    application_id: str
    timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "Approved",
                "risk_score": 0.23,
                "reasoning": "Applicant has strong credit history with excellent repayment score...",
                "agent_summary": {
                    "credit_history": {"credit_score": 750, "risk_category": "Low"},
                    "employment": {"employment_verified": True},
                    "collateral": {"collateral_sufficient": True}
                },
                "application_id": "APP-20260211-001",
                "timestamp": "2026-02-11T10:30:00"
            }
        }


class TaskState(BaseModel):
    """Internal task state model"""
    application_id: str
    applicant_name: str
    status: str
    current_stage: str
    created_at: str
    updated_at: str
    application_data: Dict[str, Any]
    agent_results: Dict[str, Any] = {}
    final_decision: Optional[Dict[str, Any]] = None


class AgentResult(BaseModel):
    """Generic agent result wrapper"""
    agent_name: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    timestamp: str
