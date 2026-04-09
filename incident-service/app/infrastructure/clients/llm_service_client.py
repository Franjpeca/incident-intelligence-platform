import os
import requests

LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL")

def analyze_text_with_llm(text: str):
    response = requests.post(
        f"{LLM_SERVICE_URL}/api/v1/analysis/text",
        json={"text": text},
        timeout=10
    )

    response.raise_for_status()

    return response.json()