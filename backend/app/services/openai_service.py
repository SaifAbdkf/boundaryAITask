"""
OpenAI integration service.
"""

import json
from typing import Optional, Dict, Any
from openai import OpenAI
import httpx

from app.config import settings
from app.schemas.survey import SurveyGenerateRequest

class OpenAIService:
    """Service for handling OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI service."""
        self.client: Optional[OpenAI] = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI client with error handling."""
        if not settings.is_openai_configured:
            print("OpenAI API key not configured")
            return
        
        try:
            # Try different initialization approaches to avoid proxy conflicts
            http_client = httpx.Client(
                timeout=30.0,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
            
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                http_client=http_client
            )
            print("OpenAI client initialized successfully with custom HTTP client")
        except Exception as e:
            print(f"Failed to initialize OpenAI client with custom HTTP: {e}")
            
            # Fallback: try basic initialization
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("OpenAI client initialized successfully with basic setup")
            except Exception as e2:
                print(f"Failed to initialize OpenAI client with basic setup: {e2}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if OpenAI client is available."""
        return self.client is not None
    
    def generate_survey(self, request: SurveyGenerateRequest) -> Dict[str, Any]:
        """Generate a survey using OpenAI."""
        if not self.is_available():
            raise Exception("OpenAI client not available")
        
        prompt = self._create_survey_prompt(request)
        
        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a survey creation assistant. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            ai_response = response.choices[0].message.content
            
            # Try to parse JSON
            try:
                survey_data = json.loads(ai_response)
                return survey_data
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw response for debugging
                return {
                    "title": request.title,
                    "description": request.description,
                    "raw_ai_response": ai_response,
                    "error": "Failed to parse AI response as JSON"
                }
        
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
    
    
    def _create_survey_prompt(self, request: SurveyGenerateRequest) -> str:
        """Create the prompt for OpenAI survey generation."""
        return f"""Create a survey with the title "{request.title}" and description "{request.description}".

Generate a JSON response with exactly this structure:
{{
    "title": "{request.title}",
    "description": "{request.description}",
    "questions": [
        {{
            "id": "q1",
            "type": "shortAnswer",
            "title": "Question text here",
            "saved": true,
            "options": []
        }},
        {{
            "id": "q2", 
            "type": "multipleChoice",
            "title": "Question text here",
            "saved": true,
            "options": [
                {{"id": "opt1", "text": "Option 1"}},
                {{"id": "opt2", "text": "Option 2"}}
            ]
        }},
        {{
            "id": "q3",
            "type": "singleChoice",
            "title": "Question text here",
            "saved": true,
            "options": [
                {{"id": "opt1", "text": "Option 1"}},
                {{"id": "opt2", "text": "Option 2"}}
            ]
        }},
        {{
            "id": "q4",
            "type": "openQuestion",
            "title": "Question text here",
            "saved": true,
            "options": []
        }},
         {{
            "id": "q3",
            "type": "scale",
            "title": "Question text here",
            "saved": true,
            "options": []
        }},
    ]
}}

Valid question types are: shortAnswer, multipleChoice, singleChoice, openQuestion, scale
Include 5-7 relevant questions with variety between the types. For choice questions, provide 
appropriate options. the question should match the type of question, for example if a question 
is better answered with one option, it should be a singleChoice question.
Return only valid JSON, no other text."""
