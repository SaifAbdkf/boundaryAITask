"""
Survey generation routes.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.survey import SurveyGenerateRequest
from app.services.openai_service import OpenAIService

router = APIRouter(prefix="/api/surveys", tags=["surveys"])

# Initialize OpenAI service
openai_service = OpenAIService()

@router.post("/generate")
def generate_survey(request: SurveyGenerateRequest):
    """Generate a survey based on title and description using OpenAI."""
    
    # Check if OpenAI is configured
    if not openai_service.is_available():
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured"
        )
    
    try:
        survey_data = openai_service.generate_survey(request)
        return survey_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating survey: {str(e)}"
        )
