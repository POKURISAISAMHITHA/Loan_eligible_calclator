"""
Planner Agent
Creates verification strategy and breaks down the loan verification process
"""
import logging
from models import PlannerResponse, LoanApplicationRequest
from prompts import PLANNER_MESSAGES

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Agent responsible for planning the verification workflow"""
    
    def __init__(self):
        self.name = "planner_agent"
        logger.info(f"{self.name} initialized")
    
    async def process(self, application: LoanApplicationRequest) -> PlannerResponse:
        """
        Create verification plan based on application details
        
        Args:
            application: Loan application data
            
        Returns:
            PlannerResponse: Detailed verification plan
        """
        try:
            logger.info(f"Creating verification plan for {application.name}")
            
            # Use plan from prompts
            plan = PLANNER_MESSAGES["verification_plan"].copy()
            
            # Define detailed verification steps
            verification_steps = {
                "credit_history": PLANNER_MESSAGES["credit_step"].format(
                    loans=application.existing_loans,
                    score=application.repayment_score,
                    income=application.loan_amount
                ),
                "employment": PLANNER_MESSAGES["employment_step"].format(
                    company=application.company_name,
                    years=application.employment_years
                ),
                "collateral": PLANNER_MESSAGES["collateral_step"].format(
                    collateral=application.collateral_value,
                    loan=application.loan_amount
                ),
                "critique": PLANNER_MESSAGES["critique_step"],
                "final_decision": PLANNER_MESSAGES["decision_step"]
            }
            
            # Estimate duration based on complexity
            complexity_score = (
                application.existing_loans * 0.5 +
                (1 - application.repayment_score) * 2 +
                (1 if application.collateral_value < application.loan_amount else 0)
            )
            
            if complexity_score < 2:
                estimated_duration = PLANNER_MESSAGES["duration_low"]
            elif complexity_score < 4:
                estimated_duration = PLANNER_MESSAGES["duration_medium"]
            else:
                estimated_duration = PLANNER_MESSAGES["duration_high"]
            
            response = PlannerResponse(
                plan=plan,
                verification_steps=verification_steps,
                estimated_duration=estimated_duration
            )
            
            logger.info(f"Verification plan created successfully for {application.name}")
            return response
            
        except Exception as e:
            logger.error(f"Error in planner agent: {e}")
            raise
