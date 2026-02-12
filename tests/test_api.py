"""
API Integration Tests  
Tests for FastAPI endpoints and API functionality
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "agents_ready" in data


class TestLoanApplicationEndpoint:
    """Test loan application submission"""
    
    @pytest.mark.asyncio
    async def test_successful_application(self, sample_strong_application):
        response = client.post("/apply", json=sample_strong_application)
        assert response.status_code == 200
        
        data = response.json()
        assert "application_id" in data
        assert "decision" in data
        assert data["decision"] in ["APPROVED", "REJECTED", "CONDITIONAL"]
    
    @pytest.mark.asyncio
    async def test_missing_fields(self):
        incomplete_app = {
            "name": "Test User",
            "income": 50000.0
            # Missing required fields
        }
        
        response = client.post("/apply", json=incomplete_app)
        assert response.status_code == 422  # Validation error


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        
        # Should serve HTML
        assert "text/html" in response.headers["content-type"]


class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_openapi_schema(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
    
    def test_docs_endpoint(self):
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
