## Estructura del directorio de test (`selenium-tests`)

Este repositorio proporciona una capa adicional de testing E2E utilizando Selenium, ejecutando flujos completos sobre la aplicación desde el navegador.

```
selenium-tests/
├── pages/                     # Clases que representan páginas y acciones sobre la UI
│
├── tests/                     # Tests E2E organizados por flujos
│   # (usan las clases de pages para interactuar con la web)
│
├── utils/                     # Funciones auxiliares para los tests
│   # (generación de datos, esperas, helpers)
│
├── conftest.py                # Fixtures y configuración del WebDriver
├── pytest.ini                 # Configuración de pytest
│
├── .dockerignore              # Exclusiones para la imagen Docker
├── Dockerfile                 # Ejecución de tests en contenedor
├── README.md                  # Documentación del servicio
└── requirements.txt           # Dependencias (pytest, selenium)
```