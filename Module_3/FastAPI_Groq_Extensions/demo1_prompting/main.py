from fastapi import FastAPI, HTTPException

from demo1_prompting.schemas import CompareRequest, CompareResponse
from demo1_prompting.service import compare_prompts
from shared.groq_client import groq_error
from shared.settings import MODEL_NAME


app = FastAPI(
    title="Module 3 Demo 1 - Prompting Strategies",
    description="Compare zero-shot, few-shot, and step-guided prompts with Groq.",
    version="1.0.0",
)


@app.get("/")
def health():
    return {"status": "ok", "demo": "prompting strategies", "model": MODEL_NAME}


@app.post("/compare", response_model=CompareResponse)
def compare(request: CompareRequest):
    try:
        return {"model": MODEL_NAME, "results": compare_prompts(request.question)}
    except HTTPException:
        raise
    except Exception as exc:
        raise groq_error() from exc
