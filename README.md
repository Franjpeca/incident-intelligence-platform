# Incident Intelligence Platform

## 1. Descripción del proyecto

Este proyecto consiste en una plataforma orientada a la gestión de incidencias y al análisis automático de su contenido. El sistema está diseñado con una arquitectura de microservicios para separar claramente la lógica de negocio principal del procesamiento de texto realizado por el servicio de análisis.

El objetivo del proyecto es construir una solución backend modular, mantenible y desplegable, capaz de registrar incidencias, gestionarlas a través de una API REST y completarlas con información adicional como resumen, categoría, prioridad y nivel de confianza.

Para ello, la plataforma combina reglas deterministas con análisis mediante modelos de lenguaje, de forma que el procesamiento automático solo se utiliza cuando realmente aporta valor al flujo del sistema.


## 2. Arquitectura

La plataforma sigue una arquitectura de microservicios orquestada por Docker, donde cada componente se ejecuta de forma independiente y se comunica a través de HTTP mediante APIs REST.

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
- **Infrastructure**: gestiona la persistencia y comunicación con servicios externos. Como la base de datos o la llamada a otros microservicios

Este enfoque favorece la mantenibilidad del código, la reutilización de componentes y la claridad en la separación de responsabilidades.

Adicionalmente, el proyecto incluye contenedores dedicados a testing de extremo a extremo (**E2E Testing**):

- **playwright-tests**: orientado a la validación de flujos completos de usuario de forma moderna y eficiente.
- **selenium-tests**: utilizado como alternativa adicional para garantizar estabilidad y compatibilidad en la automatización del frontend.

Ambos permiten validar el comportamiento completo del sistema dentro del entorno Docker.



## 3. Componentes del sistema

La plataforma está formada por varios servicios independientes, cada uno encargado de una parte específica del sistema.

- **incident-service**: gestiona las incidencias, incluyendo su creación, consulta, actualización y almacenamiento. Centraliza la lógica de negocio y es responsable de decidir cuándo aplicar reglas deterministas o cuándo delegar el procesamiento al servicio de análisis del modelo de lenguaje, en función del contenido de la incidencia.

- **llm-service**: servicio especializado en el procesamiento de texto. Recibe información estructurada y devuelve resultados normalizados como resumen, categoría, prioridad y nivel de confianza, asegurando que la salida cumple el formato esperado antes de devolverla.

- **postgres**: base de datos relacional encargada de persistir tanto las incidencias como los resultados derivados del procesamiento, manteniendo la consistencia de los datos.

- **frontend**: interfaz ligera que permite interactuar con el sistema, facilitando la creación de incidencias y la visualización de los resultados procesados.

- **playwright-tests**: contenedor dedicado a la ejecución de pruebas automatizadas de extremo a extremo, validando los flujos principales del sistema desde la perspectiva de uso.

- **selenium-tests**: contenedor adicional de pruebas automatizadas que complementa la validación del sistema, asegurando estabilidad y consistencia en los flujos del frontend.


## 4. Flujo del sistema

El funcionamiento del sistema sigue un flujo estructurado desde la creación de una incidencia hasta su enriquecimiento con información adicional.

1. El usuario crea una incidencia a través del frontend o directamente mediante la API.
2. El `incident-service` recibe la petición, valida los datos y persiste la información en la base de datos.
3. Cuando se solicita un análisis, el servicio principal evalúa el contenido de la incidencia mediante un conjunto de reglas deterministas.
4. En función del resultado de estas reglas:
   - Si la información es suficiente, se generan directamente los campos de salida (resumen, categoría, prioridad).
   - Si se requiere un análisis más complejo, se delega el procesamiento al `llm-service`.
5. El `llm-service` procesa el texto y devuelve una respuesta estructurada.
6. El `incident-service` valida la respuesta recibida y actualiza la incidencia en la base de datos.
7. El resultado final queda disponible para su consulta a través de la API o del frontend.

Este flujo permite controlar cuándo aplicar procesamiento automático, evitando el uso innecesario de recursos y manteniendo la consistencia de los resultados.