"""
Final Decision Agent
Makes the final loan approval decision based on all agent outputs
"""
import logging
from typing import Optional
from models import (
    FinalDecisionResponse,
    LoanDecision,
    CreditHistoryResponse,
    EmploymentVerificationResponse,
    CollateralVerificationResponse,
    CritiqueResponse
)

logger = logging.getLogger(__name__)


class FinalDecisionAgent:
    """Agent responsible for making the final loan decision"""
    
    def __init__(self):
        self.name = "final_decision_agent"
        logger.info(f"{self.name} initialized")
    
    def calculate_risk_score(
        self,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse,
        critique_result: CritiqueResponse
    ) -> float:
        """
        Calculate overall risk score (0-1, where 0 is lowest risk)
        
        Args:
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            critique_result: Critique analysis
            
        Returns:
            float: Risk score
        """
        # Credit risk component (0-0.4)
        credit_risk_map = {"Low": 0.1, "Medium": 0.25, "High": 0.4}
        credit_risk = credit_risk_map.get(credit_result.risk_category.value, 0.4)
        
        # Add DTI ratio risk
        dti_risk = min(credit_result.debt_to_income_ratio * 0.3, 0.2)
        
        # Employment risk component (0-0.25)
        if employment_result.passed:
            employment_risk = 0.05
        elif employment_result.employment_verified:
            employment_risk = 0.15
        else:
            employment_risk = 0.25
        
        # Collateral risk component (0-0.25)
        if collateral_result.passed:
            collateral_risk = 0.05
        elif collateral_result.collateral_sufficient:
            collateral_risk = 0.15
        else:
            collateral_risk = 0.25
        
        # Critique confidence impact (0-0.1)
        critique_risk = (1 - critique_result.confidence_score) * 0.1
        
        # Calculate total risk
        total_risk = credit_risk + dti_risk + employment_risk + collateral_risk + critique_risk
        
        return min(1.0, total_risk)
    
    def make_decision(
        self,
        risk_score: float,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse,
        critique_result: CritiqueResponse
    ) -> tuple[LoanDecision, Optional[list[str]]]:
        """
        Make final loan decision
        
        Args:
            risk_score: Calculated risk score
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            critique_result: Critique analysis
            
        Returns:
            tuple: (Decision, Conditions if applicable)
        """
        # Count passed verifications
        passed_count = sum([
            credit_result.passed,
            employment_result.passed,
            collateral_result.passed
        ])
        
        conditions = []
        
        # Decision logic
        if risk_score <= 0.3 and passed_count >= 3:
            # Low risk, all verifications passed - Approve
            decision = LoanDecision.APPROVED
            
        elif risk_score <= 0.5 and passed_count >= 2:
            # Medium risk, most verifications passed - Conditional
            decision = LoanDecision.CONDITIONAL
            
            # Add conditions based on what failed
            if not credit_result.passed:
                if credit_result.debt_to_income_ratio > 0.5:
                    conditions.append("Reduce debt-to-income ratio below 50%")
                if credit_result.risk_category.value == "High":
                    conditions.append("Provide additional credit references")
            
            if not employment_result.passed:
                if employment_result.years_employed < 1:
                    conditions.append("Provide 1+ year employment verification")
                if not employment_result.company_verified:
                    conditions.append("Submit additional employment documentation")
            
            if not collateral_result.passed:
                shortfall = (1 - collateral_result.effective_coverage) * 100
                if shortfall > 10:
                    conditions.append(f"Increase collateral by {shortfall:.0f}%")
                else:
                    conditions.append("Provide co-signer or additional collateral")
            
            # Add critique-based conditions
            if len(critique_result.inconsistencies_found) > 0:
                conditions.append("Complete manual review due to identified inconsistencies")
            
        else:
            # High risk or multiple failures - Reject
            decision = LoanDecision.REJECTED
            conditions = None
        
        return decision, conditions
    
    def generate_reasoning(
        self,
        decision: LoanDecision,
        risk_score: float,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse,
        critique_result: CritiqueResponse,
        conditions: Optional[list[str]]
    ) -> str:
        """
        Generate detailed reasoning for the decision
        
        Args:
            decision: Final decision
            risk_score: Risk score
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            critique_result: Critique analysis
            conditions: Conditions if applicable
            
        Returns:
            str: Detailed reasoning
        """
        reasoning_parts = []
        
        # Opening statement
        reasoning_parts.append(
            f"After comprehensive multi-agent analysis, the loan application has been "
            f"{decision.value.lower()} with an overall risk score of {risk_score:.2%}."
        )
        
        # Credit analysis summary
        reasoning_parts.append(
            f"\n\nCredit Analysis: {credit_result.analysis}"
        )
        
        # Employment verification summary
        reasoning_parts.append(
            f"\n\nEmployment Verification: {employment_result.analysis}"
        )
        
        # Collateral assessment summary
        reasoning_parts.append(
            f"\n\nCollateral Assessment: {collateral_result.analysis}"
        )
        
        # Critique summary
        reasoning_parts.append(
            f"\n\nQuality Review: {critique_result.critique_summary}"
        )
        
        # Decision rationale
        if decision == LoanDecision.APPROVED:
            reasoning_parts.append(
                f"\n\nDecision Rationale: The applicant demonstrates strong creditworthiness "
                f"across all verification dimensions. Low risk profile ({risk_score:.2%}) "
                f"and consistent positive indicators support approval."
            )
        elif decision == LoanDecision.CONDITIONAL:
            reasoning_parts.append(
                f"\n\nDecision Rationale: The applicant shows potential for approval with "
                f"moderate risk ({risk_score:.2%}). Conditional approval is granted subject "
                f"to meeting the following requirements:"
            )
            if conditions:
                for idx, condition in enumerate(conditions, 1):
                    reasoning_parts.append(f"\n  {idx}. {condition}")
        else:
            reasoning_parts.append(
                f"\n\nDecision Rationale: The application presents high risk ({risk_score:.2%}) "
                f"with multiple verification concerns. The applicant is encouraged to address "
                f"the identified issues and reapply in the future."
            )
        
        # Recommendations from critique
        if critique_result.recommendations:
            reasoning_parts.append("\n\nRecommendations:")
            for idx, rec in enumerate(critique_result.recommendations, 1):
                reasoning_parts.append(f"\n  {idx}. {rec}")
        
        return "".join(reasoning_parts)
    
    async def process(
        self,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse,
        critique_result: CritiqueResponse
    ) -> FinalDecisionResponse:
        """
        Make final loan decision based on all agent outputs
        
        Args:
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            critique_result: Critique analysis
            
        Returns:
            FinalDecisionResponse: Final decision with reasoning
        """
        try:
            logger.info("Making final loan decision")
            
            # Calculate risk score
            risk_score = self.calculate_risk_score(
                credit_result,
                employment_result,
                collateral_result,
                critique_result
            )
            
            # Make decision
            decision, conditions = self.make_decision(
                risk_score,
                credit_result,
                employment_result,
                collateral_result,
                critique_result
            )
            
            # Generate reasoning
            reasoning = self.generate_reasoning(
                decision,
                risk_score,
                credit_result,
                employment_result,
                collateral_result,
                critique_result,
                conditions
            )
            
            response = FinalDecisionResponse(
                decision=decision,
                risk_score=risk_score,
                reasoning=reasoning,
                conditions=conditions
            )
            
            logger.info(
                f"Final decision: {decision.value}, Risk score: {risk_score:.2%}"
            )
            return response
            
        except Exception as e:
            logger.error(f"Error in final decision agent: {e}")
            raise
