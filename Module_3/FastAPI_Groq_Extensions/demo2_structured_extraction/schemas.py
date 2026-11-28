from typing import Literal

from pydantic import BaseModel, Field


class ExtractionRequest(BaseModel):
    email: str = Field(
        min_length=10,
        max_length=10000,
        examples=["Hi, I'm Priya Nair. Order SE-48213 arrived with a torn sole. Please refund or replace it."],
    )


class SupportTicket(BaseModel):
    customer_name: str = Field(description="Full name of the customer")
    order_id: str = Field(description="Order identifier, such as SE-48213")
    issue_category: Literal[
        "damaged_item", "shipping_delay", "refund_request", "product_defect", "other"
    ]
    sentiment: Literal["positive", "neutral", "negative"]
    requested_action: Literal[
        "refund", "replacement", "store_credit", "status_update", "none"
    ]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(description="One-sentence summary of the issue")


class ExtractionResponse(BaseModel):
    model: str
    ticket: SupportTicket
