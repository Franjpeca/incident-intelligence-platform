# API Incidents

Base URL: http://localhost:8000

---

## Documentación

### Swagger UI
Interfaz interactiva para probar endpoints
http://localhost:8000/docs

### ReDoc
Documentación alternativa
http://localhost:8000/redoc

---

## 1. Crear incidencia
Crea una nueva incidencia en el sistema

Invoke-RestMethod -Method POST `PP
  -Uri "http://localhost:8000/api/v1/incidents" `
  -ContentType "application/json" `
  -Body '{
    "title": "Servidor caido",
    "description": "El servidor no responde",
    "status": "open"
  }'

---

## 2. Obtener todas las incidencias
Devuelve la lista completa

Invoke-RestMethod -Method GET `
  -Uri "http://localhost:8000/api/v1/incidents"

---

## 3. Obtener incidencia por ID
Devuelve una incidencia concreta

Invoke-RestMethod -Method GET `
  -Uri "http://localhost:8000/api/v1/incidents/1"

---

## 4. Actualizar estado
Modifica solo el estado de la incidencia

Invoke-RestMethod -Method PATCH `
  -Uri "http://localhost:8000/api/v1/incidents/1/status" `
  -ContentType "application/json" `
  -Body '{
    "status": "in_progress"
  }'

---

## 5. Actualizar incidencia completa
Reemplaza todos los datos de la incidencia

Invoke-RestMethod -Method PUT `
  -Uri "http://localhost:8000/api/v1/incidents/1" `
  -ContentType "application/json" `
  -Body '{
    "title": "Error actualizado",
    "description": "Nuevo detalle del error",
    "status": "resolved"
  }'

---

## 6. Borrar incidencia
Elimina una incidencia por ID

Invoke-RestMethod -Method DELETE `
  -Uri "http://localhost:8000/api/v1/incidents/1"

---

## 7. Generar análisis de la incidencia
Genera análisis automático de la incidencia

Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8000/api/v1/incidents/1/analysis"

---

## 8. Obtener análisis
Obtiene el análisis generado previamente

Invoke-RestMethod -Method GET `
  -Uri "http://localhost:8000/api/v1/incidents/1/analysis"