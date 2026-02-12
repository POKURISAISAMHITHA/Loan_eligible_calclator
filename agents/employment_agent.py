"""
Employment Verification Agent
Simulates employment and company verification through mock searches
"""
import logging
import os
from typing import Dict, Any
from models import EmploymentVerificationResponse, LoanApplicationRequest
from prompts import EMPLOYMENT_MESSAGES, KNOWN_COMPANIES, RISK_THRESHOLDS

logger = logging.getLogger(__name__)


class EmploymentVerificationAgent:
    """Agent responsible for employment verification"""
    
    def __init__(self):
        self.name = "employment_verification_agent"
        self.serper_api_key = os.getenv("SERPER_API_KEY", "")
        logger.info(f"{self.name} initialized")
        
        # Use known companies from prompts
        self.known_companies = KNOWN_COMPANIES
    
    def simulate_linkedin_search(self, name: str, company: str) -> Dict[str, Any]:
        """
        Simulate LinkedIn profile search
        
        Args:
            name: Applicant name
            company: Company name
            
        Returns:
            Dict: Simulated search results
        """
        logger.info(f"Simulating LinkedIn search for {name} at {company}")
        
        # Mock simulation - in production, this would use real API
        profile_found = True  # Simulate successful search
        current_position = company
        
        return {
            "profile_found": profile_found,
            "current_company": current_position,
            "verification_source": "LinkedIn (simulated)",
            "confidence": 0.85
        }
    
    def simulate_glassdoor_verification(self, company: str) -> Dict[str, Any]:
        """
        Simulate Glassdoor company verification
        
        Args:
            company: Company name
            
        Returns:
            Dict: Simulated verification results
        """
        logger.info(f"Simulating Glassdoor verification for {company}")
        
        # Check if company is in known companies database
        company_lower = company.lower()
        is_legitimate = any(known in company_lower for known in self.known_companies)
        
        # Simulate company data
        if is_legitimate:
            rating = 4.2
            employee_count = "1000-5000"
            verified = True
        else:
            # Still give benefit of doubt for unknown companies
            rating = 3.5
            employee_count = "50-200"
            verified = True  # Assume legitimate unless proven otherwise
        
        return {
            "company_verified": verified,
            "company_rating": rating,
            "employee_count": employee_count,
            "verification_source": "Glassdoor (simulated)"
        }
    
    def perform_web_verification(self, company: str) -> Dict[str, Any]:
        """
        Simulate web search verification using Serper API (mocked)
        
        Args:
            company: Company name
            
        Returns:
            Dict: Simulated web search results
        """
        logger.info(f"Simulating web verification for {company}")
        
        # In production, this would use actual Serper API
        # For now, we simulate the response
        
        has_web_presence = True
        search_results = 150  # Simulated result count
        
        return {
            "web_presence": has_web_presence,
            "search_results_count": search_results,
            "verification_source": "Serper API (simulated)",
            "api_key_configured": bool(self.serper_api_key)
        }
    
    def assess_employment_stability(self, years: float) -> str:
        """
        Assess employment stability based on years
        
        Args:
            years: Years of employment
            
        Returns:
            str: Stability assessment
        """
        messages = EMPLOYMENT_MESSAGES
        thresholds = RISK_THRESHOLDS["employment_years"]
        
        if years >= thresholds["excellent"]:
            return messages["stability_excellent"]
        elif years >= thresholds["good"]:
            return messages["stability_good"]
        elif years >= thresholds["acceptable"]:
            return messages["stability_acceptable"]
        else:
            return messages["stability_concerning"]
    
    async def process(self, application: LoanApplicationRequest) -> EmploymentVerificationResponse:
        """
        Perform comprehensive employment verification
        
        Args:
            application: Loan application data
            
        Returns:
            EmploymentVerificationResponse: Employment verification results
        """
        try:
            logger.info(f"Verifying employment for {application.name} at {application.company_name}")
            
            # Perform simulated verifications
            linkedin_result = self.simulate_linkedin_search(
                application.name,
                application.company_name
            )
            
            glassdoor_result = self.simulate_glassdoor_verification(
                application.company_name
            )
            
            web_result = self.perform_web_verification(
                application.company_name
            )
            
            # Assess stability
            stability = self.assess_employment_stability(application.employment_years)
            
            # Determine verification status
            employment_verified = linkedin_result["profile_found"] and application.employment_years >= 0.5
            company_verified = glassdoor_result["company_verified"] and web_result["web_presence"]
            
            # Generate analysis
            analysis_parts = []
            messages = EMPLOYMENT_MESSAGES
            thresholds = RISK_THRESHOLDS["employment_years"]
            
            if employment_verified:
                analysis_parts.append(
                    messages["verified_template"].format(
                        company=application.company_name,
                        years=application.employment_years
                    )
                )
            else:
                analysis_parts.append(messages["unable_to_verify"])
            
            if company_verified:
                analysis_parts.append(
                    messages["company_verified"].format(company=application.company_name)
                )
            else:
                analysis_parts.append(messages["company_inconclusive"])
            
            analysis_parts.append(f"Employment stability: {stability}")
            
            # Additional insights
            if application.employment_years >= thresholds["good"]:
                analysis_parts.append(messages["strong_commitment"])
            elif application.employment_years >= thresholds["acceptable"]:
                analysis_parts.append(messages["reasonable_history"])
            else:
                analysis_parts.append(messages["limited_tenure"])
            
            analysis = ". ".join(analysis_parts) + "."
            
            # Determine if passed
            passed = (
                employment_verified and
                company_verified and
                application.employment_years >= thresholds["acceptable"]
            )
            
            response = EmploymentVerificationResponse(
                employment_verified=employment_verified,
                company_verified=company_verified,
                employment_stability=stability,
                years_employed=application.employment_years,
                analysis=analysis,
                passed=passed
            )
            
            logger.info(
                f"Employment verification complete: "
                f"Verified={employment_verified}, Passed={passed}"
            )
            return response
            
        except Exception as e:
            logger.error(f"Error in employment verification agent: {e}")
            raise
