from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from app.infrastructure.db.base import Base
from app.domain.enums.incident_status import IncidentStatus

class Incident(Base):
    __tablename__ = "incidents"

    # Atributos basicos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Atributos de estado
    status = Column(String(50), default=IncidentStatus.OPEN.value)
    priority = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    
    # Atributos para el LLM
    ai_summary = Column(Text, nullable=True)
    ai_confidence = Column(Integer, nullable=True)

    # Fechas de creacion y actualizacion
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))