import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# A project-local key has precedence. If it is absent, load the selected Module
# 2 env file to reuse its key without copying it into this new project.
load_dotenv(PROJECT_ROOT / ".env", override=False)
external_env = os.getenv("GROQ_ENV_FILE")
if external_env and not os.getenv("GROQ_API_KEY"):
    load_dotenv(Path(external_env).expanduser(), override=True)

MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
