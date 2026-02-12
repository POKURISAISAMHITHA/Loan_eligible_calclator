"""
Unit Tests for Individual Agents
Tests each agent's decision-making logic independently
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.greeting_agent import GreetingAgent
from agents.planner_agent import PlannerAgent
from agents.credit_history_agent import CreditHistoryAgent
from agents.employment_agent import EmploymentVerificationAgent
from agents.collateral_agent import CollateralVerificationAgent
from agents.critique_agent import CritiqueAgent
from agents.final_decision_agent import FinalDecisionAgent
from agents.testing_agent import TestingAgent
from models import LoanApplicationRequest, RiskCategory


class TestGreetingAgent:
    """Test Greeting Agent"""
    
    @pytest.mark.asyncio
    async def test_greeting_generation(self):
        agent = GreetingAgent()
        result = await agent.process("APP-TEST-001", "John Doe")
        
        assert result.greeting_message is not None
        assert len(result.greeting_message) > 0
        assert result.timestamp is not None


class TestCreditHistoryAgent:
    """Test Credit History Agent"""
    
    @pytest.mark.asyncio
    async def test_excellent_credit(self, sample_strong_application):
        agent = CreditHistoryAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process("APP-TEST-001", app)
        
        assert result.passed == True
        assert result.credit_score >= 600
        assert result.risk_category in [RiskCategory.LOW, RiskCategory.MEDIUM]
    
    @pytest.mark.asyncio
    async def test_poor_credit(self, sample_weak_application):
        agent = CreditHistoryAgent()
        app = LoanApplicationRequest(**sample_weak_application)
        result = await agent.process("APP-TEST-002", app)
        
        # Weak application likely has issues
        assert result.credit_score is not None
        assert result.debt_to_income_ratio > 3.0


class TestEmploymentVerificationAgent:
    """Test Employment Verification Agent"""
    
    @pytest.mark.asyncio
    async def test_stable_employment(self, sample_strong_application):
        agent = EmploymentVerificationAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process("APP-TEST-001", app)
        
        assert result.employment_verified == True
        assert result.passed == True
    
    @pytest.mark.asyncio
    async def test_unstable_employment(self, sample_weak_application):
        agent = EmploymentVerificationAgent()
        app = LoanApplicationRequest(**sample_weak_application)
        result = await agent.process("APP-TEST-002", app)
        
        # Check that analysis is provided
        assert result.analysis is not None


class TestCollateralVerificationAgent:
    """Test Collateral Verification Agent"""
    
    @pytest.mark.asyncio
    async def test_sufficient_collateral(self, sample_strong_application):
        agent = CollateralVerificationAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process("APP-TEST-001", app)
        
        assert result.loan_to_value_ratio < 1.0  # Good LTV ratio
        assert result.passed == True
    
    @pytest.mark.asyncio
    async def test_no_collateral(self):
        agent = CollateralVerificationAgent()
        app_data = {
            "name": "No Collateral User",
            "income": 80000.0,
            "loan_amount": 150000.0,
            "existing_loans": 1,
            "repayment_score": 0.75,
            "employment_years": 5.0,
            "company_name": "Tech Corp",
            "collateral_value": 0.0
        }
        app = LoanApplicationRequest(**app_data)
        result = await agent.process("APP-TEST-003", app)
        
        assert result.collateral_sufficient == False


class TestTestingAgent:
    """Test the Testing Agent itself"""
    
    def test_validation_pass(self):
        agent = TestingAgent()
        
        application = {
            "name": "Test User",
            "income": 120000.0,
            "loan_amount": 200000.0,
            "repayment_score": 0.92,
            "existing_loans": 1,
            "employment_years": 8.0,
            "company_name": "Tech Corp",
            "collateral_value": 300000.0
        }
        
        decision_result = {
            "final_decision": "APPROVED",
            "confidence_score": 0.90,
            "agent_results": {},
            "reasoning": "Strong financial profile with excellent repayment history"
        }
        
        test_result = agent.analyze(application, decision_result)
        
        assert "test_id" in test_result
        assert test_result["passed"] == True
        assert test_result["test_score"] >= 0.70
    
    def test_bias_detection(self):
        agent = TestingAgent()
        
        # Create a potentially biased scenario
        application = {
            "name": "Low Income User",
            "income": 45000.0,  # Low income
            "loan_amount": 120000.0,
            "repayment_score": 0.85,  # Good repayment
            "existing_loans": 1,
            "employment_years": 6.0,
            "company_name": "Small Business",
            "collateral_value": 150000.0
        }
        
        decision_result = {
            "final_decision": "REJECTED",  # Rejected despite good repayment
            "confidence_score": 0.80,
            "agent_results": {},
            "reasoning": "Income level concerns"
        }
        
        test_result = agent.analyze(application, decision_result)
        bias_check = test_result["bias_check"]
        
        # Should detect potential income bias
        assert "fairness_score" in bias_check
        assert isinstance(bias_check["bias_indicators"], list)
    
    def test_anomaly_detection(self):
        agent = TestingAgent()
        
        # Create anomalous scenario
        application = {
            "name": "Anomaly User",
            "income": 50000.0,
            "loan_amount": 600000.0,  # 12x income!
            "repayment_score": 0.60,
            "existing_loans": 2,
            "employment_years": 3.0,
            "company_name": "Startup",
            "collateral_value": 100000.0  # Insufficient collateral
        }
        
        decision_result = {
            "final_decision": "APPROVED",  # Anomalous approval
            "confidence_score": 0.98,  # Very high confidence
            "agent_results": {},
            "reasoning": "OK"  # Weak reasoning
        }
        
        test_result = agent.analyze(application, decision_result)
        anomalies = test_result["anomaly_detection"]
        
        assert anomalies["anomalies_detected"] > 0
        assert anomalies["requires_review"] == True
    
    def test_statistics_generation(self):
        agent = TestingAgent()
        
        # Run several tests
        for i in range(5):
            app = {
                "name": f"Test User {i}",
                "income": 60000.0 + i * 10000,
                "loan_amount": 150000.0,
                "repayment_score": 0.75,
                "existing_loans": 1,
                "employment_years": 5.0,
                "company_name": "Test Corp",
                "collateral_value": 180000.0
            }
            decision = {
                "final_decision": "APPROVED",
                "confidence_score": 0.85,
                "agent_results": {},
                "reasoning": "Good financial profile"
            }
            agent.analyze(app, decision)
        
        stats = agent.get_test_statistics()
        
        assert stats["total_tests"] == 5
        assert "pass_rate" in stats
        assert "average_test_score" in stats


# Integration test for all agents working together
class TestAgentIntegration:
    """Test agents working together"""
    
    @pytest.mark.asyncio
    async def test_full_agent_workflow(self, sample_strong_application):
        """Test all agents analyzing the same application"""
        app = LoanApplicationRequest(**sample_strong_application)
        
        greeting_agent = GreetingAgent()
        credit_agent = CreditHistoryAgent()
        employment_agent = EmploymentVerificationAgent()
        collateral_agent = CollateralVerificationAgent()
        
        # Test each agent can process
        greeting_result = await greeting_agent.process("APP-TEST-001", app.name)
        credit_result = await credit_agent.process("APP-TEST-001", app)
        employment_result = await employment_agent.process("APP-TEST-001", app)
        collateral_result = await collateral_agent.process("APP-TEST-001", app)
        
        # Each agent should return valid results
        assert greeting_result is not None
        assert credit_result is not None
        assert employment_result is not None
        assert collateral_result is not None
    
    @pytest.mark.asyncio
    async def test_agent_consistency(self, sample_applications_batch):
        """Test that agents are consistent across multiple applications"""
        agent = CreditHistoryAgent()
        
        results = []
        for app_data in sample_applications_batch:
            app = LoanApplicationRequest(**app_data)
            result = await agent.process(f"APP-TEST-{len(results)}", app)
            results.append(result)
        
        # All results should have valid structure
        for result in results:
            assert result.credit_score is not None
            assert result.risk_category in [RiskCategory.LOW, RiskCategory.MEDIUM, RiskCategory.HIGH]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
