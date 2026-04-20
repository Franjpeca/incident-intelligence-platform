from app.schemas.analysis_request import AnalysisRequest
from app.services.analysis_service import analyze_text

import logging

# Mandamos a la funcion el texto a analizar y el tipo de prompt a usar
def analyze_text_controller(data: AnalysisRequest):
    return analyze_text(
        text=data.text,
        analysis_type=data.analysis_type
    )