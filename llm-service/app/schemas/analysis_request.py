from typing import Optional
from pydantic import BaseModel, Field


# Por ejemplo, "only_summary", "all"
# Esto depende de lo que quiera el cliente, se indica por API
# Es mejor que que el cliente mande el prompt entero o el
# nombre del fichero de prompt, es mas desacoplado y escalable
class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    analysis_type: Optional[str] = None