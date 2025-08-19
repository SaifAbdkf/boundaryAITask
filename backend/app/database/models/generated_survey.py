"""
Database models for survey storage.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import hashlib

Base = declarative_base()

class GeneratedSurvey(Base):
    """Model for storing generated surveys."""
    
    __tablename__ = "generated_surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Hash of the input (title + description) for quick lookup
    input_hash = Column(String(64), unique=True, index=True, nullable=False)
    
    # Original input data
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    
    # Generated survey data (stored as JSON)
    generated_data = Column(JSON, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # OpenAI API metadata
    openai_model = Column(String(100))
    openai_tokens_used = Column(Integer)
    
    @classmethod
    def create_input_hash(cls, title: str, description: str) -> str:
        """Create a hash of the input for deduplication."""
        input_string = f"{title.strip().lower()}:{description.strip().lower()}"
        return hashlib.sha256(input_string.encode()).hexdigest()
    
    def __repr__(self):
        return f"<GeneratedSurvey(id={self.id}, title='{self.title}', created_at={self.created_at})>"
