import sys
from pathlib import Path

# Ensure src directory is in sys.path so imports work from any working directory
_src_dir = str(Path(__file__).resolve().parent)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from fastapi import FastAPI, HTTPException
from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME
from models import PromptRequest, PromptResponse


app = FastAPI(
    title="FastAPI LLM Application",
    description="A simple FastAPI application powered by Groq",
    version="1.0.0"
)

client = Groq(api_key=GROQ_API_KEY or "your_api_key")


@app.get("/")
def home():
    return {
        "message": "FastAPI LLM Application is running."
    }


@app.post(
    "/generate",
    response_model=PromptResponse
)
def generate_response(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": request.prompt
                }
            ],
            temperature=0.2,
            max_tokens=300
        )

        generated_text = (
            response.choices[0]
            .message
            .content
        )

        return {
            "response": generated_text,
            "model": MODEL_NAME,
            "status": "success"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
