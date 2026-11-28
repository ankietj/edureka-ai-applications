from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    message: str = Field(
        min_length=5,
        max_length=2000,
        examples=["Where is my order SE-71234? It was supposed to come yesterday."],
    )


class RouteResponse(BaseModel):
    model: str
    tool_used: str | None = None
    tool_input: dict = Field(default_factory=dict)
    backend_result: dict = Field(default_factory=dict)
    final_reply: str
