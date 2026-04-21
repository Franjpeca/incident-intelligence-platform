# Incident Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Pytest](https://img.shields.io/badge/Pytest-testing-blue)
![Playwright](https://img.shields.io/badge/Playwright-E2E-green)
![Selenium](https://img.shields.io/badge/Selenium-E2E-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)

## 1. Descripción del proyecto

Este proyecto consiste en una plataforma orientada a la **gestión de incidencias y al análisis automático de su contenido**. El sistema está diseñado con una arquitectura de microservicios para separar claramente la lógica de negocio principal del procesamiento de texto realizado por el servicio de análisis.

El objetivo del proyecto es construir una solución **backend modular, mantenible y desplegable**, capaz de registrar incidencias, gestionarlas a través de una API REST y completarlas con información adicional como resumen, categoría, prioridad y nivel de confianza.

Para ello, la plataforma **combina reglas deterministas con análisis mediante modelos de lenguaje**, de forma que el procesamiento automático solo se utiliza cuando realmente aporta valor al flujo del sistema.


## 2. Arquitectura

La plataforma sigue una arquitectura de microservicios orquestada por Docker, donde cada componente se ejecuta de forma independiente y se comunica a través de HTTP mediante **APIs REST**.

El sistema está dividido en los siguientes servicios principales:

- **incident-service**: Servicio encargado de la gestión de incidencias, incluyendo operaciones CRUD, reglas de negocio y persistencia en base de datos.
- **llm-service**: Servicio independiente responsable del análisis de texto, que procesa las incidencias y devuelve información estructurada.
- **frontend**: Interfaz ligera para interactuar con la API y visualizar los resultados.
- **postgres**: Base de datos relacional utilizada para almacenar las incidencias y sus análisis.

La separación en microservicios permite desacoplar responsabilidades, facilitar el despliegue y escalar cada componente de forma independiente según las necesidades del sistema.

A nivel interno, el servicio principal (`incident-service`) sigue una arquitectura en capas:

- **Controllers**: gestionan la entrada HTTP y validación de datos.
- **Services**: contienen la lógica de aplicación y orquestación.
- **Domain**: define las reglas de negocio y estructuras principales.
- **Infrastructure**: gestiona la persistencia y la comunicación con servicios externos, como la base de datos o la llamada a otros microservicios.

Este enfoque favorece la mantenibilidad del código, la reutilización de componentes y la claridad en la separación de responsabilidades.

Adicionalmente, el proyecto incluye contenedores dedicados a testing de extremo a extremo (**E2E Testing**):

- **playwright-tests**: orientado a la validación de flujos completos de usuario de forma moderna y eficiente.
- **selenium-tests**: utilizado como alternativa adicional para garantizar estabilidad y compatibilidad en la automatización del frontend.

Ambos permiten validar el comportamiento completo del sistema dentro del entorno Docker.

> Nota: Dentro de cada directorio de microservicios y tests se puede ver la estructura de carpetas en su correspondiente README



## 3. Componentes del sistema

La plataforma está compuesta por varios microservicios independientes, cada uno con una responsabilidad concreta dentro del sistema.

- **incident-service**: servicio principal encargado de gestionar las incidencias, incluyendo su creación, consulta, actualización y almacenamiento. También coordina el proceso de análisis cuando es necesario.

- **llm-service**: servicio dedicado al análisis de texto. Recibe contenido de las incidencias y devuelve información estructurada como resumen, categoría, prioridad y nivel de confianza.

- **postgres**: base de datos relacional utilizada para persistir las incidencias y los resultados generados durante su procesamiento.

- **frontend**: interfaz web ligera para interactuar con el sistema, crear incidencias y consultar los resultados obtenidos.

- **playwright-tests**: contenedor de pruebas de extremo a extremo orientado a validar los flujos principales del sistema desde la interfaz web.

- **selenium-tests**: contenedor adicional de pruebas de extremo a extremo que refuerza la validación del frontend y la estabilidad de los flujos principales.

Todo lo realizado por los microservicios queda registrado y persistido mediante logs con niveles.

## 4. Flujo del sistema

Cuando una incidencia se registra y se solicita su análisis, el sistema sigue un flujo de procesamiento orientado a mantener la consistencia de los datos y decidir qué tipo de análisis aplicar en cada caso.


1. **Ingesta y validación**: el usuario registra una incidencia desde el frontend o directamente mediante la API. El `incident-service` valida el formato de los datos y realiza la persistencia inicial en la base de datos.

2. **Evaluación inicial**: el servicio principal analiza el contenido de la incidencia mediante un conjunto de reglas deterministas.

3. **Decisión de procesamiento**:
   - Si la incidencia encaja en patrones conocidos, se asignan directamente los campos necesarios (categoría, prioridad, resumen).
   - Si la información es ambigua o insuficiente, se delega el procesamiento al `llm-service`.

4. **Procesamiento del texto**: el `llm-service` analiza el contenido y devuelve una respuesta estructurada con los campos esperados.

5. **Validación de la respuesta**: el `incident-service` verifica que la información recibida cumple el formato esperado antes de integrarla en el sistema.

6. **Actualización y disponibilidad**: se actualiza la incidencia en la base de datos y los resultados quedan disponibles para su consulta a través de la API o del frontend.

Adicionalmente, el sistema contempla situaciones de error, como fallos en la comunicación con el servicio de análisis o respuestas inválidas. Para ello, se utilizan **mecanismos de control y errores personalizados** que permiten mantener el flujo de procesamiento sin comprometer la integridad de los datos.

Este flujo permite controlar **cuándo** resolver una incidencia mediante reglas y cuándo delegar el análisis al modelo de lenguaje, evitando el uso innecesario de recursos y manteniendo la consistencia de los resultados.


## 5. API REST

El sistema expone una API REST versionada (`/api/v1`) diseñada para gestionar incidencias, generar y consultar análisis.

El `incident-service` organiza sus endpoints mediante routers

Sus endpoints son:

- `POST /api/v1/incidents`: creación de nuevas incidencias.
- `GET /api/v1/incidents`: listado de incidencias.
- `GET /api/v1/incidents/{id}`: consulta detallada de una incidencia específica.
- `PATCH /api/v1/incidents/{id}`: actualización parcial de una incidencia.
- `DELETE /api/v1/incidents/{id}`: eliminación de una incidencia del sistema.
- `POST /api/v1/incidents/{id}/analysis`: solicitud de procesamiento y análisis.
- `GET /api/v1/incidents/{id}/analysis`: recuperación de los resultados del análisis realizado.
- `GET /health`: verificación del estado del servicio y conexión con la base de datos.

Las peticiones y respuestas siguen contratos definidos mediante esquemas, lo que permite validar la información y garantizar la consistencia entre servicios.

El microservicio `llm-service` también expone su propia API REST, pudiendo ser utilizado tanto por otros servicios como de forma independiente.

Sus endpoints principales son:

- `POST /api/v1/analysis/text`: procesamiento y análisis de texto para la extracción de metadatos (resumen, categoría, prioridad y nivel de confianza)
- `GET /health`: verificación del estado del servicio y disponibilidad del modelo cargado




## 6. Testing

El proyecto sigue una estrategia de testing basada en varios niveles, con el objetivo de asegurar la robustez del sistema y validar tanto la lógica interna como el comportamiento completo de la plataforma.

### Unit tests
Implementados con Pytest, se centran en validar la lógica del sistema de forma aislada, sin dependencias externas:

- Reglas deterministas de clasificación.
- Transformación de datos y lógica de dominio.
- Manejo de errores y excepciones personalizadas.

### Integration tests
Pruebas orientadas a verificar la interacción entre los distintos componentes de cada microservicio:

- Integración entre routers, controllers y servicios.
- Persistencia y consultas en base de datos mediante entornos de prueba controlados.
- Validación de contratos de API y esquemas de entrada/salida.

### End-to-End tests (E2E)
Para validar el funcionamiento completo del sistema, se utilizan contenedores específicos integrados en el entorno Docker y orientados a probar los flujos principales desde la interfaz web:

- **playwright-tests**: valida los flujos principales del sistema (happy path), asegurando la correcta interacción entre frontend, backend y servicio de análisis.
- **selenium-tests**: proporciona una capa adicional de validación, reforzando la estabilidad de los flujos y el comportamiento del frontend.

Este enfoque permite detectar errores en distintas capas del sistema, mejorar la calidad del código y garantizar que los distintos componentes funcionan correctamente tanto de forma aislada como integrada.


## 7. Ejecución del proyecto

El sistema está completamente contenedorizado mediante Docker, lo que permite ejecutar todos los servicios de forma orquestada y reproducible.

### Requisitos previos

- Docker
- Docker Compose

Clonar el repositorio y situarse en la raíz del proyecto.

### Configuración del entorno

Antes de ejecutar el sistema, es necesario configurar las variables de entorno:

```bash
cp .env.example .env
```

Ajustar los valores si es necesario (credenciales de base de datos, puertos, etc.).

### Ejecución

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Este comando construye las imágenes y levanta todos los servicios:

- `incident-service`: API principal (http://localhost:8000)
- `llm-service`: servicio de análisis (http://localhost:8001)
- `postgres`: base de datos relacional
- `frontend`: interfaz web (http://localhost:5500)
- contenedores de testing (`playwright-tests`, `selenium-tests`)

### Acceso a los servicios

- Frontend: http://localhost:5500
- Docs API `incident-service`: http://localhost:8000/docs
- Docs API `llm-service`: http://localhost:8001/docs
- Healthcheck del servicio de análisis: http://localhost:8001/health

### Consideraciones técnicas

- **Persistencia**: se utilizan volúmenes de Docker para mantener los datos de PostgreSQL entre ejecuciones.
- **Orquestación**: los contenedores de testing esperan a que los servicios críticos estén disponibles antes de ejecutarse.
- **Red interna**: los servicios se comunican a través de la red interna de Docker, sin exponer directamente la base de datos.


## 8. Decisiones de diseño

Durante el desarrollo del proyecto se han tomado varias decisiones para intentar mantener el sistema organizado, fácil de mantener y escalable:

- **Separación de responsabilidades**: El sistema está dividido en distintos servicios y capas para que cada parte tenga una función concreta, facilitando la comprensión y el mantenimiento del código.

- **Desacoplamiento de componentes**: La gestión de incidencias y el análisis de texto se han separado en servicios diferentes, de forma que puedan evolucionar de manera independiente. Este mismo enfoque también se aplica a los contenedores dedicados al testing E2E.

- **Estrategias de procesamiento**: En función del contenido de la incidencia, el sistema decide si aplicar reglas simples o utilizar el servicio de análisis, evitando usar el modelo cuando no es necesario.

- **Aislamiento de la persistencia**: El acceso a la base de datos se mantiene separado del resto de la lógica, lo que permite cambiar la forma de almacenamiento sin afectar al sistema completo.

- **Contratos de datos definidos**: Se utilizan esquemas para validar los datos que entran y salen del sistema, asegurando que la información tenga siempre el formato esperado.

- **Gestión de recursos externos**: Se ha intentado controlar el uso de conexiones a servicios externos para evitar creaciones innecesarias y mejorar el rendimiento.

- **Validación de resultados del análisis**: Antes de guardar los resultados del análisis, se comprueba que tienen el formato correcto, evitando inconsistencias en los datos.

- **Entorno reproducible**: El uso de Docker permite levantar todo el sistema de forma sencilla y consistente, independientemente del entorno.
