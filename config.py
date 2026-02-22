"""Load config from environment; .env file is loaded automatically."""
from pathlib import Path

from dotenv import load_dotenv
import os

# Load .env from the same directory as this file (backend folder)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
