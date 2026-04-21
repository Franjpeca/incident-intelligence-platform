## Estructura del microservicio (`llm-service`)

Este microservicio está centrado en el procesamiento de texto mediante modelos de lenguaje. A diferencia del servicio de incidencias, su estructura es más simple, ya que no incluye persistencia ni lógica de base de datos.

```
llm-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/   # Reciben la petición y llaman a los services
│   │       └── routers/       # Definición de endpoints
│   │
│   ├── core/                  # Configuración del servicio
│   │   # (carga del modelo, logging, excepciones, settings)
│   │
│   ├── prompts/               # Plantillas de prompts
│   │   # (texto y contexto que se envía al modelo)
│   │
│   ├── schemas/               # Modelos de entrada y salida (Pydantic)
│   │
│   ├── services/              # Lógica de procesamiento
│   │   # (inferencia del modelo y generación de resultados)
│   │
│   └── main.py                # Punto de entrada del servicio
│
├── logs/                      # Logs del servicio
│
├── tests/                     # Tests del microservicio
│   ├── integration/           # Tests de endpoints
│   ├── unit/                  # Tests de lógica aislada
│   └── conftest.py            # Configuración común de pytest
│
├── .dockerignore              # Exclusiones para la imagen Docker
├── .env                       # Variables de entorno
├── .env.example               # Ejemplo de configuración
├── Dockerfile                 # Imagen del servicio
├── pytest.ini                 # Configuración de pytest
├── README.md                  # Documentación del servicio
└── requirements.txt           # Dependencias
```