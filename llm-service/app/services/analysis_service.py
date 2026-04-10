import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import MODEL_ID, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from app.schemas.analysis_response import AnalysisResponse

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto"
        )

    return _tokenizer, _model



def analyze_text(text: str):
    return "Análisis de texto no implementado aún"