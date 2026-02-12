"""
Credit History Agent
Performs deterministic credit score calculation and risk assessment
"""
import logging
from models import CreditHistoryResponse, LoanApplicationRequest, RiskCategory
from prompts import CREDIT_ANALYSIS_MESSAGES, RISK_THRESHOLDS, CREDIT_SCORE_PARAMS

logger = logging.getLogger(__name__)


class CreditHistoryAgent:
    """Agent responsible for credit history analysis and risk scoring"""
    
    def __init__(self):
        self.name = "credit_history_agent"
        logger.info(f"{self.name} initialized")
    
    def calculate_credit_score(
        self,
        income: float,
        existing_loans: int,
        repayment_score: float,
        loan_amount: float
    ) -> float:
        """
        Calculate credit score using deterministic formula
        
        Args:
            income: Annual income
            existing_loans: Number of existing loans
            repayment_score: Historical repayment score (0-1)
            loan_amount: Requested loan amount
            
        Returns:
            float: Credit score (300-850 range)
        """
        params = CREDIT_SCORE_PARAMS
        
        # Base score
        base_score = params["base_score"]
        
        # Repayment history component
        repayment_component = repayment_score * params["repayment_max"]
        
        # Existing loans penalty
        loan_penalty = min(existing_loans * params["loan_penalty_per_loan"], params["loan_penalty_max"])
        
        # Income to loan ratio component
        income_ratio = income / loan_amount if loan_amount > 0 else 0
        income_component = min(income_ratio * params["income_ratio_multiplier"], params["income_component_max"])
        
        # Debt burden component
        debt_burden = existing_loans / (income / 10000) if income > 0 else 10
        debt_component = max(0, params["debt_burden_base"] - (debt_burden * params["debt_burden_multiplier"]))
        
        # Calculate final score
        credit_score = (
            base_score +
            repayment_component -
            loan_penalty +
            income_component +
            debt_component
        )
        
        # Clamp to valid range
        return max(params["score_min"], min(params["score_max"], credit_score))
    
    def determine_risk_category(self, credit_score: float, repayment_score: float) -> RiskCategory:
        """
        Determine risk category based on credit score and repayment history
        
        Args:
            credit_score: Calculated credit score
            repayment_score: Historical repayment score
            
        Returns:
            RiskCategory: Risk classification
        """
        thresholds = RISK_THRESHOLDS
        
        if credit_score >= thresholds["credit_score"]["excellent"] and repayment_score >= thresholds["repayment_score"]["strong"]:
            return RiskCategory.LOW
        elif credit_score >= thresholds["credit_score"]["fair"] and repayment_score >= thresholds["repayment_score"]["acceptable"]:
            return RiskCategory.MEDIUM
        else:
            return RiskCategory.HIGH
    
    async def process(self, application: LoanApplicationRequest) -> CreditHistoryResponse:
        """
        Perform comprehensive credit history analysis
        
        Args:
            application: Loan application data
            
        Returns:
            CreditHistoryResponse: Credit analysis results
        """
        try:
            logger.info(f"Analyzing credit history for {application.name}")
            
            # Calculate credit score
            credit_score = self.calculate_credit_score(
                application.income,
                application.existing_loans,
                application.repayment_score,
                application.loan_amount
            )
            
            # Calculate debt-to-income ratio
            estimated_monthly_debt = (application.existing_loans * 500) + (application.loan_amount * 0.005)
            monthly_income = application.income / 12
            debt_to_income_ratio = estimated_monthly_debt / monthly_income if monthly_income > 0 else 0
            
            # Determine risk category
            risk_category = self.determine_risk_category(credit_score, application.repayment_score)
            
            # Generate analysis
            analysis_parts = []
            messages = CREDIT_ANALYSIS_MESSAGES
            thresholds = RISK_THRESHOLDS
            
            # Credit score analysis
            if credit_score >= thresholds["credit_score"]["excellent"]:
                analysis_parts.append(messages["excellent_score"].format(score=credit_score))
            elif credit_score >= thresholds["credit_score"]["fair"]:
                analysis_parts.append(messages["fair_score"].format(score=credit_score))
            else:
                analysis_parts.append(messages["below_average_score"].format(score=credit_score))
            
            # Repayment history analysis
            if application.repayment_score >= thresholds["repayment_score"]["strong"]:
                analysis_parts.append(messages["strong_repayment"].format(score=application.repayment_score))
            elif application.repayment_score >= thresholds["repayment_score"]["acceptable"]:
                analysis_parts.append(messages["acceptable_repayment"].format(score=application.repayment_score))
            else:
                analysis_parts.append(messages["concerning_repayment"].format(score=application.repayment_score))
            
            # Existing loans analysis
            if application.existing_loans == 0:
                analysis_parts.append(messages["no_loans"])
            elif application.existing_loans <= 2:
                analysis_parts.append(messages["manageable_loans"].format(count=application.existing_loans))
            else:
                analysis_parts.append(messages["high_debt_burden"].format(count=application.existing_loans))
            
            # Debt-to-income analysis
            if debt_to_income_ratio < thresholds["dti_ratio"]["healthy"]:
                analysis_parts.append(messages["healthy_dti"].format(ratio=debt_to_income_ratio))
            elif debt_to_income_ratio < thresholds["dti_ratio"]["moderate"]:
                analysis_parts.append(messages["moderate_dti"].format(ratio=debt_to_income_ratio))
            else:
                analysis_parts.append(messages["high_dti"].format(ratio=debt_to_income_ratio))
            
            analysis = messages["analysis_template"].format(
                details=', '.join(analysis_parts),
                risk_level=risk_category.value
            )
            
            # Determine if passed
            passed = risk_category in [RiskCategory.LOW, RiskCategory.MEDIUM] and debt_to_income_ratio < RISK_THRESHOLDS["dti_ratio"]["moderate"]
            
            response = CreditHistoryResponse(
                credit_score=credit_score,
                risk_category=risk_category,
                debt_to_income_ratio=debt_to_income_ratio,
                analysis=analysis,
                passed=passed
            )
            
            logger.info(f"Credit analysis complete: Score={credit_score:.0f}, Risk={risk_category.value}")
            return response
            
        except Exception as e:
            logger.error(f"Error in credit history agent: {e}")
            raise
