"""
Orchestrator Agent
Coordinates all sub-agents and manages the loan application workflow
"""
import logging
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

from models import (
    LoanApplicationRequest,
    LoanApplicationResponse,
    GreetingResponse,
    PlannerResponse,
    CreditHistoryResponse,
    EmploymentVerificationResponse,
    CollateralVerificationResponse,
    CritiqueResponse,
    FinalDecisionResponse
)
from database import db
from agents import (
    GreetingAgent,
    PlannerAgent,
    CreditHistoryAgent,
    EmploymentVerificationAgent,
    CollateralVerificationAgent,
    CritiqueAgent,
    FinalDecisionAgent
)

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Main orchestrator that coordinates all verification agents
    and manages the workflow state
    """
    
    def __init__(self):
        """Initialize orchestrator and all sub-agents"""
        self.name = "orchestrator_agent"
        
        # Initialize all agents
        self.greeting_agent = GreetingAgent()
        self.planner_agent = PlannerAgent()
        self.credit_history_agent = CreditHistoryAgent()
        self.employment_agent = EmploymentVerificationAgent()
        self.collateral_agent = CollateralVerificationAgent()
        self.critique_agent = CritiqueAgent()
        self.final_decision_agent = FinalDecisionAgent()
        
        logger.info(f"{self.name} initialized with all sub-agents")
    
    def generate_application_id(self) -> str:
        """
        Generate unique application ID
        
        Returns:
            str: Unique application ID
        """
        date_str = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid4())[:8].upper()
        return f"APP-{date_str}-{unique_id}"
    
    async def process_application(
        self,
        application: LoanApplicationRequest
    ) -> LoanApplicationResponse:
        """
        Process loan application through all agents
        
        Args:
            application: Loan application request
            
        Returns:
            LoanApplicationResponse: Final decision with complete analysis
        """
        application_id = self.generate_application_id()
        
        try:
            logger.info(f"Starting application processing: {application_id}")
            
            # Create database record
            db.create_application(
                application_id=application_id,
                applicant_name=application.name,
                application_data=application.model_dump()
            )
            
            # Stage 1: Greeting
            logger.info(f"[{application_id}] Stage 1: Greeting")
            db.update_stage(application_id, "greeting")
            
            greeting_response = await self.greeting_agent.process(
                application_id,
                application.name
            )
            
            db.save_agent_result(
                application_id,
                "greeting_agent",
                True,
                greeting_response.model_dump()
            )
            
            # Stage 2: Planning
            logger.info(f"[{application_id}] Stage 2: Planning")
            db.update_stage(application_id, "planning")
            
            planner_response = await self.planner_agent.process(application)
            
            db.save_agent_result(
                application_id,
                "planner_agent",
                True,
                planner_response.model_dump()
            )
            
            # Stage 3: Parallel Verification (Credit, Employment, Collateral)
            logger.info(f"[{application_id}] Stage 3: Parallel Verification")
            db.update_stage(application_id, "verification")
            
            # Credit History Verification
            logger.info(f"[{application_id}] Running Credit History Agent")
            credit_response = await self.credit_history_agent.process(application)
            
            db.save_agent_result(
                application_id,
                "credit_history_agent",
                True,
                credit_response.model_dump()
            )
            
            # Employment Verification
            logger.info(f"[{application_id}] Running Employment Verification Agent")
            employment_response = await self.employment_agent.process(application)
            
            db.save_agent_result(
                application_id,
                "employment_verification_agent",
                True,
                employment_response.model_dump()
            )
            
            # Collateral Verification
            logger.info(f"[{application_id}] Running Collateral Verification Agent")
            collateral_response = await self.collateral_agent.process(application)
            
            db.save_agent_result(
                application_id,
                "collateral_verification_agent",
                True,
                collateral_response.model_dump()
            )
            
            # Stage 4: Critique
            logger.info(f"[{application_id}] Stage 4: Critique")
            db.update_stage(application_id, "critique")
            
            critique_response = await self.critique_agent.process(
                credit_response,
                employment_response,
                collateral_response
            )
            
            db.save_agent_result(
                application_id,
                "critique_agent",
                True,
                critique_response.model_dump()
            )
            
            # Stage 5: Final Decision
            logger.info(f"[{application_id}] Stage 5: Final Decision")
            db.update_stage(application_id, "final_decision")
            
            final_response = await self.final_decision_agent.process(
                credit_response,
                employment_response,
                collateral_response,
                critique_response
            )
            
            db.save_agent_result(
                application_id,
                "final_decision_agent",
                True,
                final_response.model_dump()
            )
            
            # Save final decision to database
            db.save_final_decision(
                application_id,
                final_response.model_dump()
            )
            
            # Compile agent summary
            agent_summary = {
                "greeting": {
                    "message": greeting_response.message[:100] + "...",
                    "timestamp": greeting_response.timestamp
                },
                "planner": {
                    "plan_steps": len(planner_response.plan),
                    "estimated_duration": planner_response.estimated_duration
                },
                "credit_history": {
                    "credit_score": credit_response.credit_score,
                    "risk_category": credit_response.risk_category.value,
                    "debt_to_income_ratio": credit_response.debt_to_income_ratio,
                    "passed": credit_response.passed,
                    "analysis": credit_response.analysis
                },
                "employment": {
                    "employment_verified": employment_response.employment_verified,
                    "company_verified": employment_response.company_verified,
                    "stability": employment_response.employment_stability,
                    "passed": employment_response.passed,
                    "analysis": employment_response.analysis
                },
                "collateral": {
                    "collateral_sufficient": collateral_response.collateral_sufficient,
                    "ltv_ratio": collateral_response.loan_to_value_ratio,
                    "effective_coverage": collateral_response.effective_coverage,
                    "passed": collateral_response.passed,
                    "analysis": collateral_response.analysis
                },
                "critique": {
                    "inconsistencies_count": len(critique_response.inconsistencies_found),
                    "inconsistencies": critique_response.inconsistencies_found,
                    "recommendations": critique_response.recommendations,
                    "confidence_score": critique_response.confidence_score,
                    "summary": critique_response.critique_summary
                },
                "final_decision": {
                    "decision": final_response.decision.value,
                    "risk_score": final_response.risk_score,
                    "conditions": final_response.conditions
                }
            }
            
            # Create final response
            final_api_response = LoanApplicationResponse(
                decision=final_response.decision.value,
                risk_score=final_response.risk_score,
                reasoning=final_response.reasoning,
                agent_summary=agent_summary,
                application_id=application_id,
                timestamp=datetime.now().isoformat()
            )
            
            logger.info(
                f"[{application_id}] Processing complete: "
                f"Decision={final_response.decision.value}, "
                f"Risk={final_response.risk_score:.2%}"
            )
            
            return final_api_response
            
        except Exception as e:
            logger.error(f"[{application_id}] Error processing application: {e}")
            
            # Save error to database
            db.save_agent_result(
                application_id,
                "orchestrator",
                False,
                {},
                str(e)
            )
            
            # Return error response
            raise Exception(f"Failed to process loan application: {str(e)}")
    
    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """
        Get current status of an application
        
        Args:
            application_id: Application ID
            
        Returns:
            Dict: Application status and details
        """
        try:
            application = db.get_application(application_id)
            
            if not application:
                return {
                    "error": "Application not found",
                    "application_id": application_id
                }
            
            return {
                "application_id": application["application_id"],
                "status": application["status"],
                "current_stage": application["current_stage"],
                "created_at": application["created_at"],
                "updated_at": application["updated_at"],
                "agent_results": application["agent_results"],
                "final_decision": application["final_decision"]
            }
            
        except Exception as e:
            logger.error(f"Error retrieving application status: {e}")
            return {
                "error": str(e),
                "application_id": application_id
            }


# Global orchestrator instance
orchestrator = OrchestratorAgent()
