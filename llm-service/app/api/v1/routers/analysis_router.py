from fastapi import APIRouter
from app.api.v1.controllers.analysis_controller import analyze_text_controller
from app.schemas.analysis_request import AnalysisRequest
from app.schemas.analysis_response import AnalysisResponse

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

@router.post("/text", response_model=AnalysisResponse)
def analyze_text(data: AnalysisRequest):
    logger.info("Peticion de analisis de una incidencia recibida en llm-service", len(data.text))
    return analyze_text_controller(data)