from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from app.infrastructure.db.base import Base

class Incident(Base):
    __tablename__ = "incidents"

    # Atributos basicos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False) # Text es mejor para descripciones largas
    
    # Atributos de estado
    status = Column(String(50), default="open")     # open, in_progress, resolved, closed
    priority = Column(String(50), nullable=True)   # low, medium, high, critical (lo llenará la IA)
    category = Column(String(100), nullable=True)  # hardware, software, network (lo llenará la IA)
    
    # Atributos para el LLM
    ai_summary = Column(Text, nullable=True)       # Resumen generado por el LLM
    ai_confidence = Column(Integer, nullable=True) # Puntuación de confianza de la IA (0-100)

    # Fechas de creacion y actualizacion
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))