from sqlalchemy import Column, Integer, String, DateTime, Text, func
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
    analysis_summary = Column(Text, nullable=True)
    analysis_confidence = Column(Integer, nullable=True)

    # Fechas de creacion y actualizacion
    created_at = Column(
            DateTime(timezone=True), 
            default=func.now(),
            server_default=func.now(), 
            nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True), 
        default=func.now(),
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    # Metodo de la propia incidencia
    # Es logica de negocio
    # Permite saber si la incidencia puede ser borrada o no
    def can_be_deleted(self) -> bool:
        return self.status == IncidentStatus.CLOSED.value