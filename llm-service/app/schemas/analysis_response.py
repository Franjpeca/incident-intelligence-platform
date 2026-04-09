from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    summary: str
    category: str
    priority: str
    confidence: int