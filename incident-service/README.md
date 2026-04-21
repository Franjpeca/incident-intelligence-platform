## Estructura del microservicio (`incident-service`)

El microservicio principal de incidencias está organizado en capas siguiendo una estructura modular, con el objetivo de separar responsabilidades y facilitar el mantenimiento del código.

```
incident-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/   # Llaman a los services y devuelven el resultado al router
│   │       └── routers/       # Definición de endpoints y entrada HTTP
│   │
│   ├── application/           # Lógica de aplicación
│   │   └── services/          # Casos de uso, lógica de negocio y orquestación
│   │
│   ├── core/                  # Configuración común del servicio
│   │                          # (logging, excepciones, handlers, config)
│   │
│   ├── domain/                # Reglas y estructuras de negocio
│   │   ├── enums/             # Enumerados del dominio
│   │   └── rules/             # Reglas deterministas (negocio)
│   │
│   ├── infrastructure/        # Integración con elementos externos
│   │   ├── clients/           # Clientes HTTP para otros microservicios
│   │   └── db/
│   │       ├── models/        # Modelos ORM de la base de datos
│   │       ├── repositories/  # Operaciones de acceso a datos
│   │       └── base.py / session.py # Base declarativa y sesión de base de datos
│   │
│   ├── schemas/               # Modelos Pydantic de entrada y salida
│   │
│   └── main.py                # Punto de entrada del servicio
│
├── logs/                      # Logs del servicio
│
├── tests/                     # Tests del microservicio
│   ├── integration/           # Tests de integración
│   ├── unit/                  # Tests unitarios
│   └── conftest.py            # Fixtures y configuración común de pytest
│
├── .dockerignore              # Exclusiones para construir la imagen Docker
├── .env                       # Variables de entorno locales
├── .env.example               # Ejemplo de variables de entorno
├── Dockerfile                 # Imagen Docker del servicio
├── README.md                  # Documentación del microservicio
└── requirements.txt           # Dependencias de Python
```