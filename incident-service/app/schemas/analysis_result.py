from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    category: str
    priority: str
    confidence: int