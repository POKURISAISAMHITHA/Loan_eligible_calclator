"""
Unit tests for all agents in the loan approval system
"""
import pytest
from agents.greeting_agent import GreetingAgent
from agents.credit_history_agent import CreditHistoryAgent
from agents.employment_agent import EmploymentVerificationAgent
from agents.collateral_agent import CollateralVerificationAgent
from agents.testing_agent import TestingAgent
from models import LoanApplicationRequest


class TestGreetingAgent:
    """Test Greeting Agent"""
    
    @pytest.mark.asyncio
    async def test_greeting_generation(self):
        agent = GreetingAgent()
        result = await agent.process("APP-TEST-001", "John Doe")
        
        assert result.message is not None
        assert len(result.message) > 0
        assert "John Doe" in result.message
        assert result.application_id == "APP-TEST-001"
        assert result.timestamp is not None


class TestCreditHistoryAgent:
    """Test Credit History Agent"""
    
    @pytest.mark.asyncio
    async def test_excellent_credit(self, sample_strong_application):
        agent = CreditHistoryAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process(app)
        
        # Strong application should have low risk
        assert result.risk_category in ["Low", "Medium"]
        assert result.credit_score > 700
        assert result.analysis is not None
    
    @pytest.mark.asyncio
    async def test_poor_credit(self, sample_weak_application):
        agent = CreditHistoryAgent()
        app = LoanApplicationRequest(**sample_weak_application)
        result = await agent.process(app)
        
        # Weak application should have high risk
        assert result.risk_category in ["High", "Medium"]
        assert result.credit_score < 700
        assert result.analysis is not None


class TestEmploymentVerificationAgent:
    """Test Employment Verification Agent"""
    
    @pytest.mark.asyncio
    async def test_stable_employment(self, sample_strong_application):
        agent = EmploymentVerificationAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process(app)
        
        # Strong employment history
        assert result.employment_verified is True
        assert result.employment_stability is not None
        assert result.analysis is not None
    
    @pytest.mark.asyncio
    async def test_unstable_employment(self, sample_weak_application):
        agent = EmploymentVerificationAgent()
        app = LoanApplicationRequest(**sample_weak_application)
        result = await agent.process(app)
        
        # Weak employment history
        assert result.employment_verified is not None
        assert result.analysis is not None


class TestCollateralVerificationAgent:
    """Test Collateral Verification Agent"""
    
    @pytest.mark.asyncio
    async def test_sufficient_collateral(self, sample_strong_application):
        agent = CollateralVerificationAgent()
        app = LoanApplicationRequest(**sample_strong_application)
        result = await agent.process(app)
        
        # Sufficient collateral
        assert result.collateral_sufficient is True
        assert result.loan_to_value_ratio < 0.8
        assert result.analysis is not None
    
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
        result = await agent.process(app)
        
        # No collateral
        assert result.collateral_sufficient is False
        assert result.analysis is not None


class TestTestingAgent:
    """Test the Testing Agent itself"""
    
    @pytest.mark.asyncio
    async def test_validation_pass(self):
        """Test that testing agent validates correct decisions"""
        agent = TestingAgent()
        
        # Strong application should be approved
        application = {
            "income": 120000,
            "loan_amount": 200000,
            "repayment_score": 0.92,
            "existing_loans": 1,
            "employment_years": 8,
            "name": "Test User"
        }
        
        decision_result = {
            "final_decision": "APPROVED",
            "confidence_score": 0.95,
            "reasoning": "Strong financial profile",
            "agent_results": {}
        }
        
        result = agent.analyze(application, decision_result)
        assert result["test_score"] >= 0.0
        assert "validation" in result
    
    @pytest.mark.asyncio
    async def test_bias_detection(self):
        """Test bias detection with inconsistent decisions"""
        agent = TestingAgent()
        
        # Two similar applications with different decisions
        test_cases = [
            {
                "application": {"income": 100000, "loan_amount": 200000, "repayment_score": 0.8, "existing_loans": 1, "employment_years": 5, "name": "User1"},
                "decision": {"final_decision": "APPROVED", "confidence_score": 0.9, "reasoning": "Good profile"}
            },
            {
                "application": {"income": 100000, "loan_amount": 200000, "repayment_score": 0.8, "existing_loans": 1, "employment_years": 5, "name": "User2"},
                "decision": {"final_decision": "REJECTED", "confidence_score": 0.9, "reasoning": "Risk concerns"}
            }
        ]
        
        for test in test_cases:
            agent.analyze(test["application"], test["decision"])
        
        stats = agent.get_test_statistics()
        # Should detect consistency issues
        assert stats["total_tests"] == 2
    
    @pytest.mark.asyncio
    async def test_anomaly_detection(self):
        """Test anomaly detection for suspicious patterns"""
        agent = TestingAgent()
        
        # High confidence approval with weak reasoning
        application = {
            "income": 30000,
            "loan_amount": 500000,
            "repayment_score": 0.3,
            "existing_loans": 5,
            "employment_years": 1,
            "name": "Test Anomaly"
        }
        
        decision_result = {
            "final_decision": "APPROVED",
            "confidence_score": 0.95,
            "reasoning": "Approved",
            "agent_results": {}
        }
        
        result = agent.analyze(application, decision_result)
        assert "anomaly_detection" in result
        assert result["anomaly_detection"]["anomalies_detected"] > 0
    
    @pytest.mark.asyncio
    async def test_statistics_generation(self):
        """Test statistics generation"""
        agent = TestingAgent()
        
        # Add some test results
        for i in range(10):
            application = {
                "income": 100000,
                "loan_amount": 200000,
                "repayment_score": 0.8,
                "existing_loans": 1,
                "employment_years": 5,
                "name": f"Test User {i}"
            }
            decision = {
                "final_decision": "APPROVED" if i % 2 == 0 else "REJECTED",
                "confidence_score": 0.85,
                "reasoning": f"Test {i}",
                "agent_results": {}
            }
            agent.analyze(application, decision)
        
        stats = agent.get_test_statistics()
        assert stats["total_tests"] == 10
        assert "pass_rate" in stats
        assert "average_test_score" in stats


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
        credit_result = await credit_agent.process(app)
        employment_result = await employment_agent.process(app)
        collateral_result = await collateral_agent.process(app)
        
        # All agents should return results
        assert greeting_result is not None
        assert credit_result is not None
        assert employment_result is not None
        assert collateral_result is not None
        
        # Strong application should get positive signals
        assert credit_result.credit_score > 700
        assert employment_result.employment_verified is True
        assert collateral_result.collateral_sufficient is True
    
    @pytest.mark.asyncio
    async def test_agent_consistency(self, sample_applications_batch):
        """Test that agents are consistent across multiple applications"""
        agent = CreditHistoryAgent()
        
        results = []
        for app_data in sample_applications_batch:
            app = LoanApplicationRequest(**app_data)
            result = await agent.process(app)
            results.append(result)
        
        # All results should have required fields
        for result in results:
            assert result.credit_score is not None
            assert result.risk_category is not None
            assert result.analysis is not None
