from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    question: str = Field(
        min_length=5,
        max_length=2000,
        examples=["I bought a blender 35 days ago, opened it, and it stopped working. Can I get a refund?"],
    )


class StrategyResult(BaseModel):
    strategy: str
    answer: str
    total_tokens: int | None = None


class CompareResponse(BaseModel):
    model: str
    results: list[StrategyResult]
