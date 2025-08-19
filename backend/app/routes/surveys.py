"""
Survey generation routes.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.survey import SurveyGenerateRequest
from app.services.survey_generation_service import SurveyGenerationService
from app.database import get_db

router = APIRouter(prefix="/api/surveys", tags=["surveys"])

# Initialize survey generation service
survey_generation_service = SurveyGenerationService()

@router.post("/generate")
def generate_survey(request: SurveyGenerateRequest, db: Session = Depends(get_db)):
    """Generate a survey based on title and description using OpenAI with caching."""
    
    try:
        # Generate survey with storage integration
        survey_data, is_cached = survey_generation_service.generate_survey(request, db)
        
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
