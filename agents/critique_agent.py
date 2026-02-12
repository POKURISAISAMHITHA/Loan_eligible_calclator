"""
Critique Agent
Reviews and validates outputs from all verification agents
"""
import logging
from typing import Dict, Any
from models import CritiqueResponse, CreditHistoryResponse, EmploymentVerificationResponse, CollateralVerificationResponse

logger = logging.getLogger(__name__)


class CritiqueAgent:
    """Agent responsible for critiquing and validating other agents' outputs"""
    
    def __init__(self):
        self.name = "critique_agent"
        logger.info(f"{self.name} initialized")
    
    def check_credit_consistency(
        self,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse
    ) -> list[str]:
        """
        Check consistency between credit and employment results
        
        Args:
            credit_result: Credit history analysis
            employment_result: Employment verification
            
        Returns:
            list: List of inconsistencies found
        """
        inconsistencies = []
        
        # Check if low employment stability conflicts with good credit
        if (credit_result.risk_category.value == "Low" and
            "Concerning" in employment_result.employment_stability):
            inconsistencies.append(
                "Low credit risk conflicts with concerning employment stability"
            )
        
        # Check if excellent employment conflicts with high credit risk
        if (credit_result.risk_category.value == "High" and
            "Excellent" in employment_result.employment_stability):
            inconsistencies.append(
                "High credit risk despite excellent employment history warrants investigation"
            )
        
        return inconsistencies
    
    def check_collateral_consistency(
        self,
        credit_result: CreditHistoryResponse,
        collateral_result: CollateralVerificationResponse
    ) -> list[str]:
        """
        Check consistency between credit and collateral results
        
        Args:
            credit_result: Credit history analysis
            collateral_result: Collateral verification
            
        Returns:
            list: List of inconsistencies found
        """
        inconsistencies = []
        
        # High risk with insufficient collateral is very concerning
        if (credit_result.risk_category.value == "High" and
            not collateral_result.collateral_sufficient):
            inconsistencies.append(
                "Critical: High credit risk combined with insufficient collateral"
            )
        
        # Low risk should have reasonable collateral
        if (credit_result.risk_category.value == "Low" and
            collateral_result.loan_to_value_ratio > 0.95):
            inconsistencies.append(
                "Low credit risk applicant has high LTV ratio - unusual pattern"
            )
        
        return inconsistencies
    
    def check_overall_coherence(
        self,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse
    ) -> list[str]:
        """
        Check overall coherence of all verifications
        
        Args:
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            
        Returns:
            list: List of inconsistencies found
        """
        inconsistencies = []
        
        # Count passed verifications
        passed_count = sum([
            credit_result.passed,
            employment_result.passed,
            collateral_result.passed
        ])
        
        # All passed but high debt-to-income
        if passed_count == 3 and credit_result.debt_to_income_ratio > 0.45:
            inconsistencies.append(
                "All verifications passed but DTI ratio is concerning"
            )
        
        # None passed - ensure consistency
        if passed_count == 0:
            inconsistencies.append(
                "All verifications failed - confirms high-risk profile"
            )
        
        return inconsistencies
    
    def generate_recommendations(
        self,
        inconsistencies: list[str],
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse
    ) -> list[str]:
        """
        Generate recommendations based on analysis
        
        Args:
            inconsistencies: List of found inconsistencies
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Recommendations based on credit
        if not credit_result.passed:
            if credit_result.debt_to_income_ratio > 0.5:
                recommendations.append(
                    "Consider debt consolidation before reapplying"
                )
            if credit_result.risk_category.value == "High":
                recommendations.append(
                    "Recommend credit counseling to improve credit profile"
                )
        
        # Recommendations based on employment
        if not employment_result.passed:
            if employment_result.years_employed < 1:
                recommendations.append(
                    "Recommend reapplying after 1+ years of employment"
                )
            if not employment_result.company_verified:
                recommendations.append(
                    "Additional employment documentation required"
                )
        
        # Recommendations based on collateral
        if not collateral_result.passed:
            shortfall_pct = (1 - collateral_result.effective_coverage) * 100
            if shortfall_pct > 20:
                recommendations.append(
                    f"Collateral shortfall of {shortfall_pct:.0f}% - consider larger down payment"
                )
            else:
                recommendations.append(
                    "Consider co-signer or additional collateral"
                )
        
        # General recommendations
        if len(inconsistencies) > 0:
            recommendations.append(
                "Manual review recommended due to identified inconsistencies"
            )
        
        if not recommendations:
            recommendations.append(
                "All verifications consistent - proceed with standard approval process"
            )
        
        return recommendations
    
    def calculate_confidence_score(
        self,
        inconsistencies: list[str],
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse
    ) -> float:
        """
        Calculate confidence score for the overall assessment
        
        Args:
            inconsistencies: List of inconsistencies
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            
        Returns:
            float: Confidence score (0-1)
        """
        base_confidence = 0.95
        
        # Reduce confidence for each inconsistency
        inconsistency_penalty = len(inconsistencies) * 0.10
        
        # Reduce confidence if verifications are borderline
        borderline_penalty = 0
        if credit_result.credit_score < 650:
            borderline_penalty += 0.05
        if employment_result.years_employed < 2:
            borderline_penalty += 0.05
        if collateral_result.effective_coverage < 1.1:
            borderline_penalty += 0.05
        
        # Calculate final confidence
        confidence = base_confidence - inconsistency_penalty - borderline_penalty
        
        return max(0.5, min(1.0, confidence))  # Clamp between 0.5 and 1.0
    
    async def process(
        self,
        credit_result: CreditHistoryResponse,
        employment_result: EmploymentVerificationResponse,
        collateral_result: CollateralVerificationResponse
    ) -> CritiqueResponse:
        """
        Perform comprehensive critique of all agent outputs
        
        Args:
            credit_result: Credit history analysis
            employment_result: Employment verification
            collateral_result: Collateral verification
            
        Returns:
            CritiqueResponse: Critique analysis results
        """
        try:
            logger.info("Performing critique analysis on all agent outputs")
            
            # Collect all inconsistencies
            inconsistencies = []
            
            inconsistencies.extend(
                self.check_credit_consistency(credit_result, employment_result)
            )
            
            inconsistencies.extend(
                self.check_collateral_consistency(credit_result, collateral_result)
            )
            
            inconsistencies.extend(
                self.check_overall_coherence(credit_result, employment_result, collateral_result)
            )
            
            # Generate recommendations
            recommendations = self.generate_recommendations(
                inconsistencies,
                credit_result,
                employment_result,
                collateral_result
            )
            
            # Calculate confidence score
            confidence_score = self.calculate_confidence_score(
                inconsistencies,
                credit_result,
                employment_result,
                collateral_result
            )
            
            # Generate summary
            if len(inconsistencies) == 0:
                critique_summary = (
                    f"All agent outputs are consistent and coherent. "
                    f"Confidence score: {confidence_score:.2%}. "
                    f"Credit: {credit_result.risk_category.value} risk, "
                    f"Employment: {'Verified' if employment_result.passed else 'Concerns'}, "
                    f"Collateral: {'Sufficient' if collateral_result.passed else 'Insufficient'}."
                )
            else:
                critique_summary = (
                    f"Found {len(inconsistencies)} inconsistency(ies) requiring attention. "
                    f"Confidence score: {confidence_score:.2%}. "
                    f"Recommend careful review of highlighted areas."
                )
            
            response = CritiqueResponse(
                inconsistencies_found=inconsistencies,
                recommendations=recommendations,
                confidence_score=confidence_score,
                critique_summary=critique_summary
            )
            
            logger.info(
                f"Critique complete: {len(inconsistencies)} inconsistencies, "
                f"confidence={confidence_score:.2%}"
            )
            return response
            
        except Exception as e:
            logger.error(f"Error in critique agent: {e}")
            raise
