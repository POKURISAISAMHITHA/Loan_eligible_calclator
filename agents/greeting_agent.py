"""
Greeting Agent
Sends initial acknowledgment and welcomes the applicant
"""
import logging
from datetime import datetime
from models import GreetingResponse
from prompts import GREETING_TEMPLATES

logger = logging.getLogger(__name__)


class GreetingAgent:
    """Agent responsible for initial greeting and acknowledgment"""
    
    def __init__(self):
        self.name = "greeting_agent"
        logger.info(f"{self.name} initialized")
    
    async def process(self, application_id: str, applicant_name: str) -> GreetingResponse:
        """
        Generate greeting message for applicant
        
        Args:
            application_id: Unique application identifier
            applicant_name: Name of the applicant
            
        Returns:
            GreetingResponse: Greeting message with application details
        """
        try:
            logger.info(f"Processing greeting for {applicant_name}")
            
            message = GREETING_TEMPLATES["welcome_message"].format(
                applicant_name=applicant_name,
                application_id=application_id
            )
            
            response = GreetingResponse(
                message=message,
                application_id=application_id,
                timestamp=datetime.now().isoformat()
            )
            
            logger.info(f"Greeting processed successfully for {applicant_name}")
            return response
            
        except Exception as e:
            logger.error(f"Error in greeting agent: {e}")
            raise
