"""
Health check routes.
"""

from fastapi import APIRouter

from app.config import settings
from app.schemas.survey import HealthResponse

router = APIRouter(tags=["health"])

@router.get("/", response_model=dict)
def read_root():
    """Root endpoint - just to test the API is working."""
    return {"message": "Hello World! Survey Generator API is running"}

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        openai_configured=settings.is_openai_configured
    )
