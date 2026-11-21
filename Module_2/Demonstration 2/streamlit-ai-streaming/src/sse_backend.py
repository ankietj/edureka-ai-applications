import sys
from pathlib import Path

# Ensure src directory is in sys.path so imports work from any working directory
_src_dir = str(Path(__file__).resolve().parent)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

import json
from typing import List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

app = FastAPI(
    title="FastAPI SSE Streaming Backend",
    description="Streams Groq LLM responses to a Streamlit frontend using true SSE",
    version="2.0.0"
)

client = Groq(api_key=GROQ_API_KEY or "your_api_key")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.get("/")
def home():
    return {"message": "FastAPI SSE backend is running."}

@app.post("/stream")
def stream_response(request: ChatRequest):
    def generate():
        try:
            formatted_messages = [
                m.model_dump() if hasattr(m, "model_dump") else m.dict()
                for m in request.messages
            ]
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=formatted_messages,
                temperature=0.2,
                max_tokens=500,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    payload = json.dumps({"content": content})
                    yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as error:
            error_msg = f"\n\n[Groq API Error: {error}]"
            payload = json.dumps({"error": str(error), "content": error_msg})
            yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no", 
        },
    )

@app.post("/generate")
def generate_response(request: ChatRequest):
    try:
        formatted_messages = [
            m.model_dump() if hasattr(m, "model_dump") else m.dict()
            for m in request.messages
        ]
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=formatted_messages,
            temperature=0.2,
            max_tokens=500,
        )
        return {"response": response.choices[0].message.content}
    except Exception as error:
        return {"response": f"[Groq API Error: {error}]", "error": str(error)}
