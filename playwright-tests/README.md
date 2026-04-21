## Estructura del directorio de test (`playwright-tests`)

Este directorio posee el codigo que se encarga de probar los flujos principales del sistema simulando el comportamiento de un usuario en el navegador.

```
playwright-tests/
├── pages/                     # Clases que representan páginas y acciones sobre la UI
│
├── tests/                     # Tests E2E organizados por flujos
│   # (usan las clases de pages para interactuar con la web)
│
├── conftest.py                # Fixtures y configuración común (navegador, base URL, etc.)
├── pytest.ini                 # Configuración de pytest
│
├── .dockerignore              # Exclusiones para la imagen Docker
├── Dockerfile                 # Ejecución de tests en contenedor
└── requirements.txt           # Dependencias (pytest, playwright)
```