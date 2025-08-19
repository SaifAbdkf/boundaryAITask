"""
Survey generation routes.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.survey import SurveyGenerateRequest
from app.services.openai_service import OpenAIService
from app.database import get_db

router = APIRouter(prefix="/api/surveys", tags=["surveys"])

# Initialize OpenAI service
openai_service = OpenAIService()

@router.post("/generate")
def generate_survey(request: SurveyGenerateRequest, db: Session = Depends(get_db)):
    """Generate a survey based on title and description using OpenAI with caching."""
    
    # Check if OpenAI is configured
    if not openai_service.is_available():
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured"
        )
    
    try:
        # Generate survey with storage integration
        survey_data, is_cached = openai_service.generate_survey_with_storage(request, db)
        
        # Add metadata about whether this was cached
        response_data = {
            **survey_data,
            "metadata": {
                "is_cached": is_cached,
                "cached_at": None if not is_cached else "from_database"
            }
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating survey: {str(e)}"
        )
