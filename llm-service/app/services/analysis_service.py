from app.schemas.analysis_response import AnalysisResponse

def analyze_text(text: str) -> AnalysisResponse:
    return AnalysisResponse(
        summary=f"Mock summary for: {text}",
        category="software",
        priority="high",
        confidence=90
    )