from app.schemas.analysis_request import AnalysisRequest
from app.services.analysis_service import analyze_text

def analyze_text_controller(data: AnalysisRequest):
    return analyze_text(data.text)