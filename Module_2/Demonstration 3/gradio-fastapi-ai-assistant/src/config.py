from pathlib import Path
from dotenv import load_dotenv
import os

_demo_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_demo_dir / ".env")
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
