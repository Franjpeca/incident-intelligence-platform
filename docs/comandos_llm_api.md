# API Analysis

Base URL: http://localhost:8001

---

## Documentación

### Swagger UI
Interfaz interactiva para probar endpoints
http://localhost:8001/docs

### ReDoc
Documentación alternativa
http://localhost:8001/redoc

---

## 1. Analizar texto
Envía un texto al LLM y devuelve su análisis

Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8001/api/v1/analysis/text" `
  -ContentType "application/json" `
  -Body '{
    "text": "Servidor caido en produccion. No responde el sistema."
  }'