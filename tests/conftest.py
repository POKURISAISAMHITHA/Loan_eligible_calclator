"""
Pytest Configuration and Fixtures
Shared test fixtures and configuration for the test suite
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Database
from models import LoanApplication
from orchestrator import LoanOrchestrator


@pytest.fixture
def test_db():
    """Create a test database instance"""
    db = Database(db_path=":memory:")  # In-memory database for testing
    yield db
    # Cleanup happens automatically with in-memory DB


@pytest.fixture
def orchestrator():
    """Create a loan orchestrator instance"""
    return LoanOrchestrator()


@pytest.fixture
def sample_strong_application():
    """Strong loan application that should be approved"""
    return {
        "name": "Test Strong Applicant",
        "income": 120000.0,
        "loan_amount": 200000.0,
        "existing_loans": 1,
        "repayment_score": 0.92,
        "employment_years": 8.0,
        "company_name": "Tech Corp",
        "collateral_value": 300000.0
    }


@pytest.fixture
def sample_weak_application():
    """Weak loan application that should be rejected"""
    return {
        "name": "Test Weak Applicant",
        "income": 35000.0,
        "loan_amount": 250000.0,
        "existing_loans": 4,
        "repayment_score": 0.45,
        "employment_years": 1.0,
        "company_name": "Startup Inc",
        "collateral_value": 50000.0
    }


@pytest.fixture
def sample_moderate_application():
    """Moderate loan application that might be conditional"""
    return {
        "name": "Test Moderate Applicant",
        "income": 65000.0,
        "loan_amount": 180000.0,
        "existing_loans": 2,
        "repayment_score": 0.72,
        "employment_years": 4.0,
        "company_name": "Medium Business",
        "collateral_value": 200000.0
    }


@pytest.fixture
def sample_applications_batch():
    """Batch of diverse loan applications for testing"""
    return [
        {
            "name": "High Income Professional",
            "income": 150000.0,
            "loan_amount": 300000.0,
            "existing_loans": 0,
            "repayment_score": 0.95,
            "employment_years": 10.0,
            "company_name": "Fortune 500",
            "collateral_value": 500000.0
        },
        {
            "name": "Entry Level Worker",
            "income": 40000.0,
            "loan_amount": 100000.0,
            "existing_loans": 2,
            "repayment_score": 0.68,
            "employment_years": 2.0,
            "company_name": "Small Business",
            "collateral_value": 120000.0
        },
        {
            "name": "Entrepreneur",
            "income": 80000.0,
            "loan_amount": 250000.0,
            "existing_loans": 3,
            "repayment_score": 0.75,
            "employment_years": 5.0,
            "company_name": "Own Business",
            "collateral_value": 280000.0
        }
    ]
