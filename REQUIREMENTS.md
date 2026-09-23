# Requirements — Customer Search

## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements
FR-01: El sistema debe permitir la búsqueda de clientes por nombre utilizando coincidencia parcial (substring match), sin distinguir entre mayúsculas y minúsculas (case-insensitive) y siendo insensible a acentos o marcas diacríticas (e.g., "Jose" debe coincidir con "José").
FR-02: El sistema debe permitir la búsqueda de clientes por correo electrónico utilizando coincidencia parcial (substring match), sin distinguir entre mayúsculas y minúsculas (case-insensitive).
FR-03: El sistema debe permitir una búsqueda global unificada por término (`query`) que evalúe simultáneamente los campos de nombre y correo electrónico, retornando los registros que coincidan en cualquiera de los dos.
FR-04: El sistema debe validar que el término de búsqueda no esté vacío ni compuesto únicamente por espacios en blanco, y que posea una longitud mínima de al menos 2 caracteres significativos tras aplicar trim.
FR-05: El sistema debe permitir filtrar los resultados según el estado de la cuenta del cliente: únicamente clientes activos (`active`), únicamente inactivos (`inactive`), o todos los clientes sin distinción.
FR-06: El sistema debe proveer una interfaz de línea de comandos (CLI) que permita ingresar los criterios de búsqueda (término, campo específico, filtro de estado) y visualizar los resultados de manera tabular y estructurada en la consola.

## Non-Functional Requirements
NFR-01: Desempeño: La ejecución de una búsqueda sobre un conjunto de hasta 1,000 registros en memoria o archivo JSON local debe completarse en un tiempo menor a 50 milisegundos.
NFR-02: Arquitectura y Mantenibilidad: El código debe estructurarse siguiendo una separación de responsabilidades clara y desacoplada (capa de presentación CLI, capa de lógica/servicio de búsqueda, capa de repositorio/datos y modelo de dominio).
NFR-03: Calidad y Verificabilidad: La solución debe contar con una suite de pruebas automatizadas con `pytest` que cubra al menos el 90% de las ramas de la lógica de búsqueda y validaciones, incluyendo casos de éxito, bordes y errores.

## Open Questions
Q-01: ¿Qué comportamiento debe tener el sistema si la búsqueda no encuentra ningún cliente que coincida con el criterio?
- Decisión/Respuesta: Debe retornar una lista vacía de resultados y el CLI debe mostrar un mensaje amigable indicando que no se encontraron coincidencias, sin elevar una excepción de error.
Q-02: ¿Cómo debe comportarse la normalización de caracteres especiales o acentos en la búsqueda?
- Decisión/Respuesta: Se normalizarán las cadenas mediante descomposición canónica (forma NFKD de Unicode) ignorando marcas diacríticas antes de comparar, garantizando consistencia en nombres en español.

## Constraints / Assumptions
C-01: La solución debe utilizar exclusivamente la biblioteca estándar de Python 3.11+ para la implementación del núcleo y CLI, y `pytest` como única dependencia externa de desarrollo/pruebas.
A-01: Los datos iniciales de clientes se cargarán desde un archivo local JSON (`data/customers.json`), sirviendo como fuente de persistencia local o precarga en memoria.
