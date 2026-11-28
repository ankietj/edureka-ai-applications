from shared.groq_client import get_groq_client
from shared.policy import SYSTEM_PERSONA
from shared.settings import MODEL_NAME


PROMPT_BUILDERS = {
    "zero-shot": lambda question: (
        f"Customer question: {question}\n\n"
        "Is the customer eligible for a refund, store credit, or neither? "
        "Give a concise explanation and end with a clear verdict."
    ),
    "few-shot": lambda question: (
        "Examples:\n"
        "Q: Unopened shoes returned 10 days after delivery.\n"
        "A: Eligible for a full refund: within 30 days and unopened.\n"
        "Q: Clearance jacket returned after 5 days.\n"
        "A: Not eligible: clearance items are final sale.\n\n"
        f"Now answer this question: {question}"
    ),
    "step-guided": lambda question: (
        f"Customer question: {question}\n\n"
        "Apply the policy in order: identify days since delivery, item condition, "
        "product type, then state the applicable rule and verdict in under 120 words."
    ),
}


def compare_prompts(question: str) -> list[dict]:
    client = get_groq_client()
    results = []
    for strategy, build_prompt in PROMPT_BUILDERS.items():
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PERSONA},
                {"role": "user", "content": build_prompt(question)},
            ],
            temperature=0.2,
            max_tokens=800,
        )
        choice = response.choices[0]
        answer = (choice.message.content or "").strip()
        if not answer:
            raise ValueError("Groq returned an empty text answer for this strategy.")
        results.append(
            {
                "strategy": strategy,
                "answer": answer,
                "total_tokens": response.usage.total_tokens if response.usage else None,
            }
        )
    return results
