# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Capturamos la cadena de texto y la convertimos en una lista real de Python
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500")
ALLOWED_ORIGINS = [origin.strip() for origin in raw_origins.split(",")]