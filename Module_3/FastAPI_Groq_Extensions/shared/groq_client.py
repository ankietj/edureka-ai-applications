from fastapi import HTTPException
from groq import Groq

from shared.settings import GROQ_API_KEY


def get_groq_client() -> Groq:
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Groq is not configured. Set GROQ_API_KEY or GROQ_ENV_FILE.",
        )
    return Groq(api_key=GROQ_API_KEY)


def groq_error() -> HTTPException:
    # Keep provider exception details and credentials out of API responses.
    return HTTPException(
        status_code=502,
        detail="Groq request failed. Check the key, model availability, quota, and network.",
    )
