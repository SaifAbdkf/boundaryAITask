"""
Health check routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import settings
from app.schemas.survey import HealthResponse
from app.database import get_db

router = APIRouter(tags=["health"])

@router.get("/", response_model=dict)
def read_root():
    """Root endpoint - just to test the API is working."""
    return {"message": "Hello World! Survey Generator API is running"}

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        # Test database connection using proper SQLAlchemy syntax
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        openai_configured=settings.is_openai_configured,
        database_status=db_status
    )
