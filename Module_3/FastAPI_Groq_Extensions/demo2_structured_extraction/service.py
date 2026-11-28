import json

from pydantic import ValidationError

from demo2_structured_extraction.schemas import SupportTicket
from shared.groq_client import get_groq_client
from shared.settings import MODEL_NAME


TOOL = {
    "type": "function",
    "function": {
        "name": "extract_support_ticket",
        "description": "Extract a support ticket from a customer email.",
        "parameters": SupportTicket.model_json_schema(),
    },
}


def extract_ticket(email: str) -> SupportTicket:
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Extract only facts supported by the email. Use the required categories.",
            },
            {"role": "user", "content": f"Extract a support ticket from this email:\n{email}"},
        ],
        tools=[TOOL],
        tool_choice={"type": "function", "function": {"name": "extract_support_ticket"}},
        temperature=0,
        max_tokens=500,
    )
    calls = response.choices[0].message.tool_calls or []
    if not calls:
        raise ValueError("Groq did not return the required extraction tool call.")
    payload = json.loads(calls[0].function.arguments)
    try:
        return SupportTicket.model_validate(payload)
    except ValidationError as exc:
        raise ValueError("Groq returned ticket fields that failed validation.") from exc
