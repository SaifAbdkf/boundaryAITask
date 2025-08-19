from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Initialize OpenAI client
print(f"----------OpenAI API key configured: {bool(OPENAI_API_KEY)}")
openai_client = None

def initialize_openai_client():
    """Initialize OpenAI client with error handling"""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("OpenAI API key not configured")
        return None
    
    try:
        # Try different initialization approaches to avoid proxy conflicts
        import httpx
        
        # Create a custom HTTP client without proxy settings
        http_client = httpx.Client(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=http_client
        )
        print("OpenAI client initialized successfully with custom HTTP client")
        return client
    except Exception as e:
        print(f"Failed to initialize OpenAI client with custom HTTP: {e}")
        
        # Fallback: try basic initialization
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            print("OpenAI client initialized successfully with basic setup")
            return client
        except Exception as e2:
            print(f"Failed to initialize OpenAI client with basic setup: {e2}")
            return None

# Initialize the client
openai_client = initialize_openai_client()

# Create FastAPI application
app = FastAPI(
    title="Survey Generator API",
    description="AI-powered survey generation API"
)

# Enums
class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multipleChoice"
    SINGLE_CHOICE = "singleChoice"
    OPEN_QUESTION = "openQuestion"
    SHORT_ANSWER = "shortAnswer"
    SCALE = "scale"

# Request/Response models
class SurveyGenerateRequest(BaseModel):
    title: str
    description: str

class QuestionOption(BaseModel):
    id: str
    text: str

class Question(BaseModel):
    id: str
    type: QuestionType
    title: str
    saved: bool
    options: List[QuestionOption] = []

class SurveyGenerateResponse(BaseModel):
    title: str
    description: str
    questions: List[Question]

@app.get("/")
def read_root():
    """Root endpoint - just to test the API is working"""
    return {"message": "Hello World! Survey Generator API is running"}

@app.post("/api/surveys/generate")
def generate_survey(request: SurveyGenerateRequest):
    """Generate a survey based on title and description using OpenAI"""
    
    # Check if OpenAI is configured
    if not openai_client:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured"
        )
    
    try:
        # Simple prompt to OpenAI
        prompt = f"""Create a survey with the title "{request.title}" and description "{request.description}".

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
        }}
    ]
}}

Valid question types are: shortAnswer, multipleChoice, singleChoice, openQuestion, scale
Include 3-5 relevant questions. For choice questions, provide appropriate options.
Return only valid JSON, no other text."""

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a survey creation assistant. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Get the response content
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
        raise HTTPException(
            status_code=500,
            detail=f"Error generating survey: {str(e)}"
        )




@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "openai_configured": bool(OPENAI_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
