"""
Main FastAPI Application
Agentic AI Loan Eligibility Verification System
"""
import logging
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models import LoanApplicationRequest, LoanApplicationResponse
from orchestrator import orchestrator
from database import db

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting Agentic AI Loan Eligibility Verification System")
    logger.info(f"Database path: {db.db_path}")
    logger.info("All agents initialized successfully")
    
    # Verify environment variables
    serper_key = os.getenv("SERPER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if serper_key:
        logger.info("SERPER_API_KEY configured")
    else:
        logger.warning("SERPER_API_KEY not configured (using mock mode)")
    
    if gemini_key and gemini_key != "your_gemini_api_key_here":
        logger.info("GEMINI_API_KEY configured")
    else:
        logger.warning("GEMINI_API_KEY not configured (not required for current implementation)")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic AI Loan Eligibility Verification System")


# Initialize FastAPI app
app = FastAPI(
    title="Agentic AI Loan Eligibility Verification System",
    description=(
        "A sophisticated multi-agent system for comprehensive loan application verification. "
        "This system uses specialized AI agents to analyze credit history, employment, "
        "collateral, and provides intelligent loan approval decisions."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Redirects to beautiful UI
    
    Returns:
        FileResponse: HTML UI for testing
    """
    import os
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    
    return {
        "status": "online",
        "service": "Agentic AI Loan Eligibility Verification System",
        "version": "1.0.0",
        "endpoints": {
            "apply": "/loan/apply",
            "status": "/loan/status/{application_id}",
            "docs": "/docs",
            "health": "/health",
            "ui": "/ui"
        }
    }


@app.get("/ui", tags=["Health"])
async def ui():
    """
    Beautiful UI for testing the loan application system
    
    Returns:
        FileResponse: HTML UI
    """
    import os
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UI file not found"
        )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: System health status
    """
    try:
        # Test database connection
        test_app = db.get_application("TEST-APP")
        
        return {
            "status": "healthy",
            "database": "connected",
            "agents": {
                "greeting": "ready",
                "planner": "ready",
                "credit_history": "ready",
                "employment": "ready",
                "collateral": "ready",
                "critique": "ready",
                "final_decision": "ready"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.post(
    "/loan/apply",
    response_model=LoanApplicationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Loan Application"]
)
async def apply_for_loan(application: LoanApplicationRequest):
    """
    Submit a loan application for automated verification
    
    This endpoint processes loan applications through a multi-agent system that:
    1. Greets and acknowledges the application
    2. Plans the verification strategy
    3. Verifies credit history
    4. Verifies employment details
    5. Assesses collateral value
    6. Performs critique and consistency checks
    7. Makes final approval decision
    
    Args:
        application: Loan application details
        
    Returns:
        LoanApplicationResponse: Complete analysis and decision
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Received loan application from {application.name}")
        
        # Validate input
        if application.loan_amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan amount must be greater than 0"
            )
        
        if application.income <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Income must be greater than 0"
            )
        
        if not 0 <= application.repayment_score <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Repayment score must be between 0 and 1"
            )
        
        # Process application through orchestrator
        result = await orchestrator.process_application(application)
        
        logger.info(
            f"Application processed successfully: {result.application_id}, "
            f"Decision: {result.decision}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing loan application: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process loan application: {str(e)}"
        )


@app.get(
    "/loan/status/{application_id}",
    tags=["Loan Application"]
)
async def get_application_status(application_id: str):
    """
    Get the status and details of a loan application
    
    Args:
        application_id: Unique application identifier
        
    Returns:
        dict: Application status and processing details
        
    Raises:
        HTTPException: If application not found
    """
    try:
        logger.info(f"Retrieving status for application: {application_id}")
        
        status_info = orchestrator.get_application_status(application_id)
        
        if "error" in status_info and status_info["error"] == "Application not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application {application_id} not found"
            )
        
        return status_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving application status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve application status: {str(e)}"
        )


@app.get(
    "/loan/history",
    tags=["Loan Application"]
)
async def get_application_history(limit: int = 10):
    """
    Get recent loan applications (demo endpoint)
    
    Args:
        limit: Maximum number of applications to return
        
    Returns:
        dict: List of recent applications
    """
    # This is a simple demo endpoint
    # In production, add proper pagination and filtering
    return {
        "message": "History endpoint - implement as needed",
        "limit": limit,
        "note": "Query database for recent applications"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred processing your request",
            "type": type(exc).__name__
        }
    )


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level=log_level.lower()
    )
