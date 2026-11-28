import json

from shared.groq_client import get_groq_client
from shared.policy import SYSTEM_PERSONA
from shared.settings import MODEL_NAME


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Look up shipping status for an order.",
            "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "initiate_refund",
            "description": "Create a mock refund request for an order.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                "required": ["order_id", "reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "track_shipment",
            "description": "Look up carrier tracking details for an order.",
            "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate an ambiguous case or an upset customer.",
            "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]},
        },
    },
]

# These functions are deliberately mock implementations for classroom safety.
MOCK_BACKEND = {
    "check_order_status": lambda order_id: {"order_id": order_id, "status": "out for delivery", "eta": "today by 8pm"},
    "initiate_refund": lambda order_id, reason: {"order_id": order_id, "refund_status": "mock initiated", "reason_logged": reason},
    "track_shipment": lambda order_id: {"order_id": order_id, "carrier": "Example Carrier", "last_scan": "regional hub", "eta": "tomorrow"},
    "escalate_to_human": lambda reason: {"escalated": True, "priority": "high", "reason_logged": reason},
}


def route_message(customer_message: str) -> dict:
    client = get_groq_client()
    messages = [{"role": "user", "content": customer_message}]
    first = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": SYSTEM_PERSONA}, *messages],
        tools=TOOLS,
        tool_choice="auto",
        temperature=0,
        max_tokens=450,
    )
    assistant_message = first.choices[0].message
    calls = assistant_message.tool_calls or []
    if not calls:
        return {"tool_used": None, "tool_input": {}, "backend_result": {}, "final_reply": assistant_message.content or "I could not draft a response."}

    call = calls[0]
    tool_name = call.function.name
    if tool_name not in MOCK_BACKEND:
        raise ValueError("Groq selected an unknown tool.")
    tool_input = json.loads(call.function.arguments)
    backend_result = MOCK_BACKEND[tool_name](**tool_input)
    messages.append(assistant_message.model_dump(exclude_none=True))
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(backend_result)})
    final = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": SYSTEM_PERSONA}, *messages],
        tools=TOOLS,
        temperature=0.2,
        max_tokens=300,
    )
    return {
        "tool_used": tool_name,
        "tool_input": tool_input,
        "backend_result": backend_result,
        "final_reply": final.choices[0].message.content or "The request was processed.",
    }
