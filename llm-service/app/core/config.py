from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "Qwen2.5-1.5B-Instruct")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "256"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
TOP_P = float(os.getenv("TOP_P", "0.9"))
DO_SAMPLE = os.getenv("DO_SAMPLE", "false").lower() == "false"

LOAD_MODEL_ON_STARTUP = os.getenv("LOAD_MODEL_ON_STARTUP", "false").lower() == "true"

PROMPTS_DIR = Path(os.getenv("PROMPTS_DIR", "app/prompts"))

PROMPT_BASIC_FILE = os.getenv("PROMPT_BASIC_FILE", "incident_analysis_v1.txt")
