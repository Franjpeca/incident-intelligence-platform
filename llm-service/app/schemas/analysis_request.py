from typing import Optional
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    analysis_type: Optional[str] = None