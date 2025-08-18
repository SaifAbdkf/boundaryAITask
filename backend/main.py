from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum

# Create FastAPI application
app = FastAPI(title="Survey Generator API")

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

@app.post("/api/surveys/generate", response_model=SurveyGenerateResponse)
def generate_survey(request: SurveyGenerateRequest):
    """Generate a survey based on title and description - returns hardcoded fake data"""
    
    # Hardcoded fake survey questions
    fake_questions = [
        Question(
            id="q1",
            type=QuestionType.SHORT_ANSWER,
            title="What is your overall satisfaction with our service?",
            saved=True,
            options=[]
        ),
        Question(
            id="q2", 
            type=QuestionType.MULTIPLE_CHOICE,
            title="Which features do you use most frequently? (Select all that apply)",
            saved=True,
            options=[
                QuestionOption(id="opt1", text="Feature A"),
                QuestionOption(id="opt2", text="Feature B"),
                QuestionOption(id="opt3", text="Feature C"),
                QuestionOption(id="opt4", text="Feature D")
            ]
        ),
        Question(
            id="q3",
            type=QuestionType.SINGLE_CHOICE, 
            title="How likely are you to recommend us to a friend?",
            saved=True,
            options=[
                QuestionOption(id="opt5", text="Very likely"),
                QuestionOption(id="opt6", text="Somewhat likely"),
                QuestionOption(id="opt7", text="Neutral"),
                QuestionOption(id="opt8", text="Unlikely"),
                QuestionOption(id="opt9", text="Very unlikely")
            ]
        ),
        Question(
            id="q4",
            type=QuestionType.OPEN_QUESTION,
            title="What improvements would you like to see?",
            saved=True,
            options=[]
        ),
        Question(
            id="q5",
            type=QuestionType.SCALE,
            title="On a scale of 1-10, how would you rate our customer service?",
            saved=True,
            options=[]
        )
    ]
    
    return SurveyGenerateResponse(
        title=request.title,
        description=request.description,
        questions=fake_questions
    )




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
