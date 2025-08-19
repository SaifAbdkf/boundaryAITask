"""
Service for managing survey storage and retrieval.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.database.models.generated_survey import GeneratedSurvey
from app.schemas.survey import SurveyGenerateRequest

class SurveyStorageService:
    """Service for survey storage operations."""
    
    @staticmethod
    def find_existing_survey(db: Session, title: str, description: str) -> Optional[GeneratedSurvey]:
        """Find an existing survey by input hash."""
        input_hash = GeneratedSurvey.create_input_hash(title, description)
        
        return db.query(GeneratedSurvey).filter(
            GeneratedSurvey.input_hash == input_hash
        ).first()
    
    @staticmethod
    def save_generated_survey(
        db: Session, 
        request: SurveyGenerateRequest, 
        generated_data: Dict[str, Any],
        openai_model: str = None,
        tokens_used: int = None
    ) -> GeneratedSurvey:
        """Save a newly generated survey to the database."""
        
        # Create input hash for deduplication
        input_hash = GeneratedSurvey.create_input_hash(request.title, request.description)
        
        # Create new survey record
        survey = GeneratedSurvey(
            input_hash=input_hash,
            title=request.title,
            description=request.description,
            generated_data=generated_data,
            openai_model=openai_model,
            openai_tokens_used=tokens_used
        )
        
        # Save to database
        db.add(survey)
        db.commit()
        db.refresh(survey)
        
        return survey
    