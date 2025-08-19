"""
Survey generation orchestration service.
This service coordinates between OpenAI generation and database storage.
"""

from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session

from app.schemas.survey import SurveyGenerateRequest
from app.services.openai_service import OpenAIService
from app.services.survey_storage_service import SurveyStorageService
from app.config import settings


class SurveyGenerationService:
    """Orchestrates the survey generation workflow."""
    
    def __init__(self):
        self.openai_service = OpenAIService()
    
    def generate_survey(self, request: SurveyGenerateRequest, db: Session) -> Tuple[Dict[str, Any], bool]:
        """
        Generate a survey with intelligent caching.
        
        Args:
            request: Survey generation request
            db: Database session
            
        Returns:
            Tuple of (survey_data, is_cached)
        """
        # Check if survey already exists
        existing_survey = SurveyStorageService.find_existing_survey(
            db, request.title, request.description
        )
        
        if existing_survey:
            print(f"📋 Found cached survey for: {request.title}")
            return existing_survey.generated_data, True
        
        # Generate new survey using OpenAI
        print(f"🤖 Generating new survey for: {request.title}")
        survey_data = self.openai_service.generate_survey(request)
        
        # Save to database
        try:
            SurveyStorageService.save_generated_survey(
                db=db,
                request=request,
                generated_data=survey_data,
                openai_model=settings.LLM_MODEL
            )
            print(f"💾 Survey saved to database: {request.title}")
        except Exception as e:
            print(f"⚠️ Failed to save survey to database: {e}")
            # Still return the generated survey even if save fails
        
        return survey_data, False
    