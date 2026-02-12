"""
Collateral Verification Agent
Validates collateral value and calculates loan-to-value ratios
"""
import logging
from models import CollateralVerificationResponse, LoanApplicationRequest
from prompts import COLLATERAL_MESSAGES, LTV_CONFIG, RISK_THRESHOLDS

logger = logging.getLogger(__name__)


class CollateralVerificationAgent:
    """Agent responsible for collateral assessment"""
    
    def __init__(self):
        self.name = "collateral_verification_agent"
        self.ltv_ratio = LTV_CONFIG["standard_ratio"]  # 80% Loan-to-Value ratio
        logger.info(f"{self.name} initialized with LTV ratio: {self.ltv_ratio}")
    
    def calculate_ltv_ratio(self, loan_amount: float, collateral_value: float) -> float:
        """
        Calculate Loan-to-Value ratio
        
        Args:
            loan_amount: Requested loan amount
            collateral_value: Value of collateral
            
        Returns:
            float: LTV ratio
        """
        if collateral_value <= 0:
            return float('inf')
        return loan_amount / collateral_value
    
    def apply_margin(self, collateral_value: float) -> float:
        """
        Apply safety margin to collateral value
        
        Args:
            collateral_value: Original collateral value
            
        Returns:
            float: Effective collateral value after margin
        """
        return collateral_value * self.ltv_ratio
    
    async def process(self, application: LoanApplicationRequest) -> CollateralVerificationResponse:
        """
        Perform comprehensive collateral verification
        
        Args:
            application: Loan application data
            
        Returns:
            CollateralVerificationResponse: Collateral assessment results
        """
        try:
            logger.info(
                f"Assessing collateral for {application.name}: "
                f"Loan=${application.loan_amount:,.2f}, "
                f"Collateral=${application.collateral_value:,.2f}"
            )
            
            # Calculate LTV ratio
            ltv_ratio = self.calculate_ltv_ratio(
                application.loan_amount,
                application.collateral_value
            )
            
            # Apply margin to get effective coverage
            effective_collateral = self.apply_margin(application.collateral_value)
            effective_coverage = effective_collateral / application.loan_amount if application.loan_amount > 0 else 0
            
            # Determine if collateral is sufficient
            collateral_sufficient = effective_collateral >= application.loan_amount
            
            # Generate detailed analysis
            analysis_parts = []
            messages = COLLATERAL_MESSAGES
            thresholds = LTV_CONFIG["coverage_thresholds"]
            ltv_thresholds = RISK_THRESHOLDS["ltv_ratio"]
            
            # Collateral value assessment
            analysis_parts.append(messages["value_statement"].format(value=application.collateral_value))
            
            # LTV ratio analysis
            if ltv_ratio <= ltv_thresholds["standard"]:
                analysis_parts.append(
                    messages["excellent_ltv"].format(ltv=ltv_ratio, threshold=self.ltv_ratio)
                )
            elif ltv_ratio <= ltv_thresholds["acceptable"]:
                analysis_parts.append(messages["acceptable_ltv"].format(ltv=ltv_ratio))
            else:
                analysis_parts.append(messages["high_ltv"].format(ltv=ltv_ratio))
            
            # Margin application
            analysis_parts.append(
                messages["margin_applied"].format(
                    margin=self.ltv_ratio,
                    coverage=effective_collateral,
                    percentage=effective_coverage
                )
            )
            
            # Sufficiency assessment
            if collateral_sufficient:
                surplus = effective_collateral - application.loan_amount
                analysis_parts.append(messages["sufficient_with_surplus"].format(surplus=surplus))
            else:
                shortfall = application.loan_amount - effective_collateral
                analysis_parts.append(messages["insufficient_shortfall"].format(shortfall=shortfall))
            
            # Risk assessment
            if effective_coverage >= thresholds["excellent"]:
                analysis_parts.append(messages["low_risk"])
            elif effective_coverage >= thresholds["acceptable"]:
                analysis_parts.append(messages["acceptable_coverage"])
            elif effective_coverage >= thresholds["marginal"]:
                analysis_parts.append(messages["marginal_coverage"])
            else:
                analysis_parts.append(messages["insufficient_coverage"])
            
            analysis = ". ".join(analysis_parts) + "."
            
            # Determine if passed
            passed = collateral_sufficient and effective_coverage >= thresholds["acceptable"]
            
            response = CollateralVerificationResponse(
                collateral_sufficient=collateral_sufficient,
                loan_to_value_ratio=ltv_ratio,
                margin_applied=self.ltv_ratio,
                effective_coverage=effective_coverage,
                analysis=analysis,
                passed=passed
            )
            
            logger.info(
                f"Collateral assessment complete: "
                f"LTV={ltv_ratio:.2%}, "
                f"Sufficient={collateral_sufficient}, "
                f"Passed={passed}"
            )
            return response
            
        except Exception as e:
            logger.error(f"Error in collateral verification agent: {e}")
            raise
