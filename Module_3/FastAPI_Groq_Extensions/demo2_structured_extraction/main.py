from fastapi import FastAPI, HTTPException

from demo2_structured_extraction.schemas import ExtractionRequest, ExtractionResponse
from demo2_structured_extraction.service import extract_ticket
from shared.groq_client import groq_error
from shared.settings import MODEL_NAME


app = FastAPI(
    title="Module 3 Demo 2 - Structured Extraction",
    description="Extract a typed support ticket from an email using Groq tool calling and Pydantic.",
    version="1.0.0",
)


@app.get("/")
def health():
    return {"status": "ok", "demo": "structured extraction", "model": MODEL_NAME}


@app.post("/extract-ticket", response_model=ExtractionResponse)
def extract(request: ExtractionRequest):
    try:
        return {"model": MODEL_NAME, "ticket": extract_ticket(request.email)}
    except HTTPException:
        raise
    except Exception as exc:
        raise groq_error() from exc
