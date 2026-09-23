# AI Usage Log — ADA-05 Spec-Driven Feature

Este documento registra las interacciones clave con la Inteligencia Artificial (Antigravity CLI / Asistente) a lo largo del ciclo de vida del desarrollo spec-driven, evidenciando propuestas del agente, decisiones del estudiante y su impacto concreto en los artefactos del producto.

---

## Entrada 1: Definición de Requisitos y Manejo de Acentos
- **Fecha / Etapa**: 2026-09-23 | Fase 1 & 2 (Requisitos y Especificación)
- **Contexto**: Definición de los criterios de búsqueda para nombres en español en `REQUIREMENTS.md` y `SPEC.md`.
- **Propuesta de la IA**:
  La IA propuso inicialmente usar una biblioteca externa de Python como `unidecode` para procesar y remover acentos y caracteres especiales en los nombres de los clientes.
- **Decisión del Estudiante / Desarrollador**:
  Se rechazó la dependencia externa para cumplir con la restricción `C-01` (solo biblioteca estándar de Python y herramientas sin costo). En su lugar, se instruyó a la IA a implementar una función de normalización basada en `unicodedata.normalize('NFKD', ...)` descartando marcas diacríticas de categoría `'Mn'`, resolviendo `Q-02` sin introducir dependencias externas.
- **Cambio en el Producto**:
  Se incorporó formalmente la regla de normalización Unicode nativa en `SPEC.md` (Search Rules) y la función `normalize_text` en `src/search_service.py`.

---

## Entrada 2: Arquitectura Desacoplada y Persistencia Liviana
- **Fecha / Etapa**: 2026-09-23 | Fase 3 (Arquitectura)
- **Contexto**: Diseño de los componentes y mecanismos de almacenamiento para Customer Search.
- **Propuesta de la IA**:
  La IA sugirió estructurar un servidor HTTP FastAPI con base de datos SQLite integrada mediante SQLAlchemy para exponer la búsqueda como endpoint web.
- **Decisión del Estudiante / Desarrollador**:
  Se decidió optar por la solución mínima recomendada por la guía de la práctica (Python CLI + persistencia en memoria y JSON local), argumentando que evita sobreingeniería y maximiza la velocidad de ejecución y testabilidad sin dependencias pesadas. Además, se exigió una arquitectura en 3 capas donde el repositorio admita tanto archivos JSON como listas en memoria para facilitar las pruebas unitarias.
- **Cambio en el Producto**:
  `ARCHITECTURE.md` reflejó una arquitectura en 3 capas (`CLI` -> `CustomerSearchService` -> `CustomerRepository`) con persistencia en `data/customers.json` y soporte directo de inyección en memoria.

---

## Entrada 3: Desglose de Tareas y Restricción de Baseline Git
- **Fecha / Etapa**: 2026-09-23 | Fase 4, 5 & 6 (Tareas, Reglas de Agente y Git Baseline)
- **Contexto**: Definición de la secuencia de ejecución de tareas `TASKS.md` y reglas en `AGENTS.md`.
- **Propuesta de la IA**:
  La IA propuso generar los archivos de código fuente (`src/models.py` y `src/search_service.py`) de forma concurrente con la redacción de especificaciones para avanzar más rápido.
- **Decisión del Estudiante / Desarrollador**:
  Se denegó la implementación anticipada. Se requirió seguir estrictamente la Fase 6 de la rúbrica: completar primero `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md` y `AGENTS.md`, generar el commit baseline `spec: define customer search feature`, y solo después iniciar la implementación secuencial tarea por tarea.
- **Cambio en el Producto**:
  Se generó el commit base `2a1ea40` conteniendo exclusivamente artefactos de especificación antes de escribir una sola línea de lógica de negocio.

---

## Entrada 4: Jerarquía de Excepciones y Códigos de Salida CLI
- **Fecha / Etapa**: 2026-09-23 | Fase 7 (Implementación - T-04 y T-06)
- **Contexto**: Manejo de validaciones cuando el usuario ingresa consultas inválidas o menores a 2 caracteres.
- **Propuesta de la IA**:
  La IA propuso retornar un string de error o una lista vacía cuando el término no cumpliera la longitud mínima requerida.
- **Decisión del Estudiante / Desarrollador**:
  Se solicitó adherirse al principio de diseño especificado en `SPEC.md`: las reglas de validación deben elevar excepciones tipadas (`EmptyQueryError`, `QueryTooShortError`) en la capa de servicio, y la CLI debe capturarlas para imprimir mensajes explicativos en `stderr` con código de salida `2` (convención UNIX para errores de uso/validación).
- **Cambio en el Producto**:
  Se crearon las excepciones en `src/exceptions.py`, las validaciones en `src/search_service.py` y la captura con código 2 en `src/cli.py`.

---

## Entrada 5: Validación de Rendimiento NFR-01 y Cobertura Exhaustiva
- **Fecha / Etapa**: 2026-09-23 | Fase 9 (Pruebas y Verificación)
- **Contexto**: Comprobación del requerimiento no funcional `NFR-01` (tiempo de búsqueda < 50ms para 1,000 registros).
- **Propuesta de la IA**:
  La IA sugirió una prueba rápida midiendo la búsqueda sobre el archivo JSON de 8 clientes de ejemplo.
- **Decisión del Estudiante / Desarrollador**:
  Se corrigió el enfoque: se ordenó crear un test de rendimiento dedicado (`tests/test_performance.py`) que genere sintéticamente 1,000 objetos `Customer` reales con variaciones de nombres, correos y estados, cronometrando la ejecución con `time.perf_counter()` y asegurando una aserción estricta de `< 50ms`.
- **Cambio en el Producto**:
  Se añadió `tests/test_performance.py`, demostrando que 1,000 registros son procesados y ordenados en menos de 15ms.
