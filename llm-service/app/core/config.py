from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Variables relacionadas con el modelo
MODEL_ID = os.getenv("MODEL_ID", "Qwen2.5-1.5B-Instruct")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "256"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
TOP_P = float(os.getenv("TOP_P", "0.9"))
DO_SAMPLE = os.getenv("DO_SAMPLE", "false").lower() == "false"

# Variable para controlar el tipo de carga
LOAD_MODEL_ON_STARTUP = os.getenv("LOAD_MODEL_ON_STARTUP", "false").lower() == "true"

# Directorio de prompt
PROMPTS_DIR = Path(os.getenv("PROMPTS_DIR", "app/prompts"))

# Ficheros prompt
ANALYSIS_TYPE_TO_PROMPT = {
    "basic_analysis": "incident_basic_analysis.txt",
    "full_analysis": "incident_full_analysis.txt",
}

DEFAULT_ANALYSIS_TYPE = "basic_analysis"