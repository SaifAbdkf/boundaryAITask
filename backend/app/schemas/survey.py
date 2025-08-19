"""
Pydantic models for request/response schemas.
"""

from pydantic import BaseModel
from typing import List
from enum import Enum

class QuestionType(str, Enum):
    """Valid question types for survey questions."""
    MULTIPLE_CHOICE = "multipleChoice"
    SINGLE_CHOICE = "singleChoice"
    OPEN_QUESTION = "openQuestion"
    SHORT_ANSWER = "shortAnswer"
    SCALE = "scale"

class SurveyGenerateRequest(BaseModel):
    """Request model for survey generation."""
    title: str
    description: str

class QuestionOption(BaseModel):
    """Model for question options (used in choice questions)."""
    id: str
    text: str

class Question(BaseModel):
    """Model for survey questions."""
    id: str
    type: QuestionType
    title: str
    saved: bool
    options: List[QuestionOption] = []

class SurveyGenerateResponse(BaseModel):
    """Response model for generated surveys."""
    title: str
    description: str
    questions: List[Question]

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    openai_configured: bool
    database_status: str
