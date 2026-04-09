from fastapi import APIRouter
from app.api.v1.controllers.analysis_controller import analyze_text_controller
from app.schemas.analysis_request import AnalysisRequest
from app.schemas.analysis_response import AnalysisResponse

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

@router.post("/text", response_model=AnalysisResponse)
def analyze_text(data: AnalysisRequest):
    return analyze_text_controller(data)