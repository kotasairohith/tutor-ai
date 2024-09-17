from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
import httpx 
app = FastAPI()


GEMINI_API_KEY = "your_gemini_api_key"  # Replace with your actual Gemini API key

GEMINI_API_URL = "https://api.deepmind.com/gemini/v1/generate"

# Pydantic models for request and response validation
class QuestionRequest(BaseModel):
    topic: constr(min_length=1, max_length=50) = Field(..., example="Linear Algebra")
    difficulty: constr(regex="^(easy|medium|hard)$") = Field(..., example="medium")
    question_type: constr(regex="^(multiple-choice|short-answer|true-false)$") = Field(..., example="multiple-choice")

class QuestionResponse(BaseModel):
    question: str
    options: list[str] = []
    answer: str


async def generate_question_with_gemini(prompt: str):
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "prompt": prompt,
        "max_length": 100,  
        "temperature": 0.7,  
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Endpoint to generate a learning question
@app.post("/generate-question", response_model=QuestionResponse)
async def generate_question(request: QuestionRequest):
    prompt = f"Generate a {request.difficulty} {request.question_type} question about {request.topic}."
    
    try:
       
        response = await generate_question_with_gemini(prompt)
        generated_text = response["generated_text"]

        # Example: Extract question and answer from the generated text
        question = generated_text.split("Question: ")[-1].split(" Options: ")[0]
        options = generated_text.split("Options: ")[-1].split(" Answer: ")[0].split(", ")
        answer = generated_text.split("Answer: ")[-1]

        return QuestionResponse(question=question, options=options, answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Tutor-AIis up and running!"}
