from fastapi import FastAPI, HTTPException

from demo3_function_routing.schemas import RouteRequest, RouteResponse
from demo3_function_routing.service import route_message
from shared.groq_client import groq_error
from shared.settings import MODEL_NAME


app = FastAPI(
    title="Module 3 Demo 3 - Function Routing",
    description="Use Groq tool calling to route a customer request to a mock backend action.",
    version="1.0.0",
)


@app.get("/")
def health():
    return {"status": "ok", "demo": "function routing", "model": MODEL_NAME}


@app.post("/route-message", response_model=RouteResponse)
def route(request: RouteRequest):
    try:
        return {"model": MODEL_NAME, **route_message(request.message)}
    except HTTPException:
        raise
    except Exception as exc:
        raise groq_error() from exc
