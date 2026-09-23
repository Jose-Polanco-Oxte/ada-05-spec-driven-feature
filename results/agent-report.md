# Agent Report

## Agent / Version
- **Agent Name**: Antigravity Coding Agent (powered by Gemini 3.8 Flash High)
- **Environment**: Windows 11, PowerShell, Python 3.14.6, Git 2.55.0, pytest 9.1.1
- **Working Directory**: `ada-05-spec-driven-feature`

## Initial Context
El objetivo del proyecto fue desarrollar la funcionalidad de **Customer Search** desde cero, siguiendo de manera disciplinada un flujo dirigido por especificación (*spec-driven*): `requirements` → `specification` → `architecture` → `tasks` → `git baseline` → `implementation` → `tests` → `traceability` → `review`.
Antes de la ejecución, el repositorio se encontraba vacío y sin dependencias previas. Se establecieron las reglas en `AGENTS.md` para evitar que el agente inventara requisitos de negocio o alterara las especificaciones para forzar el paso de pruebas.

## Task Sequence

### T-01 Project setup
- **What the agent did**:
  Configuró el archivo `.gitignore`, `pytest.ini`, los paquetes base `src/__init__.py` y `tests/__init__.py`, y el conjunto de datos de prueba `data/customers.json` con 8 clientes representativos (acentos, nombres compuestos, clientes activos e inactivos).
- **Human review**:
  Se revisó la estructura de directorios y la consistencia del archivo JSON con los campos requeridos en el modelo de dominio.
- **Tests**:
  Verificación de parseo JSON con Python nativo y comprobación de inicialización de sesión en `pytest`.

### T-02 Domain model
- **What the agent did**:
  Implementó la dataclass inmutable `Customer` en `src/models.py` con validaciones de tipos, atributos (`id`, `name`, `email`, `phone`, `is_active`, `created_at`) y métodos auxiliares `from_dict` y `to_dict`. Creó `tests/test_domain.py`.
- **Human review**:
  Se verificó la inmutabilidad (`frozen=True`) para proteger la integridad de los datos en memoria y la correcta conversión de diccionarios.
- **Tests**:
  6 pruebas unitarias en `tests/test_domain.py` pasaron exitosamente (`100% passed`).

### T-03 Search logic
- **What the agent did**:
  Implementó `CustomerRepository` en `src/repository.py` y `CustomerSearchService` en `src/search_service.py` junto con la función `normalize_text` (normalización Unicode NFKD y remoción de acentos). Añadió soporte para búsqueda por `name`, `email` y global `all`, así como ordenamiento alfabético y filtro por estado.
- **Human review**:
  Se confirmó que la normalización no dependiera de paquetes externos y funcionara adecuadamente para nombres en español (e.g., "García", "José").
- **Tests**:
  Pruebas de búsqueda parcial, mayúsculas/minúsculas, acentos y ordenamiento en `tests/test_search_service.py`.

### T-04 Validation and errors
- **What the agent did**:
  Creó la jerarquía de excepciones en `src/exceptions.py` (`CustomerSearchError`, `ValidationError`, `EmptyQueryError`, `QueryTooShortError`, `InvalidFieldError`, `InvalidStatusFilterError`, `CustomerRepositoryError`). Agregó los métodos `validate_query` y `validate_criteria` en `src/search_service.py`.
- **Human review**:
  Se comprobó que las búsquedas con cadenas vacías o solo espacios lanzaran `EmptyQueryError` y cadenas de 1 solo carácter lanzaran `QueryTooShortError`.
- **Tests**:
  Pruebas de validación y de fallo de repositorio en `tests/test_validation.py`.

### T-05 Tests
- **What the agent did**:
  Consolidó la suite de pruebas unitarias y creó `tests/test_performance.py` para evaluar el requisito `NFR-01`. El test genera 1,000 clientes sintéticos y mide el tiempo de búsqueda y filtrado.
- **Human review**:
  Se verificó que los tiempos de búsqueda se mantuvieran por debajo de los 50 ms requeridos. En las mediciones reales, el tiempo fue de ~12 ms.
- **Tests**:
  Suite completa de 32 pruebas pasando en verde (`pytest -v`).

### T-06 Documentation
- **What the agent did**:
  Implementó la interfaz de línea de comandos `src/cli.py` con `argparse`, renderizado de tablas ASCII y códigos de salida apropiados (0, 1, 2). Creó `tests/test_cli.py`, `docs/traceability.md`, `AI_USAGE_LOG.md`, `README.md` y este informe.
- **Human review**:
  Se validó manualmente la ejecución del CLI con diversos comandos y banderas, así como la coherencia de la matriz de trazabilidad y las respuestas de reflexión.
- **Tests**:
  10 pruebas de integración de CLI en `tests/test_cli.py`.

## Problems Encountered
1. **Manejo de tildes y diacríticos en Python sin librerías externas**:
   - *Problema*: Librerías como `unidecode` hubieran facilitado la tarea pero habrían violado la restricción `C-01` de no añadir dependencias externas innecesarias.
   - *Solución*: Se utilizó el módulo estándar `unicodedata` con descomposición canónica `NFKD` filtrando los caracteres con categoría `Mn` (Mark, Nonspacing).
2. **Pruebas de CLI interactivas en entornos no interactivos**:
   - *Problema*: La ejecución de pruebas automatizadas sobre `src/cli.py` requería simular tanto banderas de línea de comandos como entradas interactivas por `stdin`.
   - *Solución*: Se utilizó el fixture `monkeypatch` de `pytest` para interceptar `builtins.input` y el fixture `capsys` para capturar `stdout` y `stderr`.

## Human Interventions
- Rechazo a la inclusión de librerías externas para normalización de texto y APIs HTTP innecesarias.
- Exigencia de un commit baseline estricto (`git commit -m "spec: define customer search feature"`) antes de generar cualquier archivo de código ejecutable.
- Definición rigurosa de las pruebas de rendimiento con 1,000 registros sintéticos para asegurar la verificabilidad de `NFR-01`.

## Requirement / Specification Changes
No se requirieron cambios en los requisitos ni en las especificaciones durante la fase de implementación. Gracias a la definición completa y detallada de `REQUIREMENTS.md` y `SPEC.md` en las Fases 1 y 2, todos los criterios de aceptación fueron unívocos y verificables desde el inicio.

## Final Verification
- **Pruebas Automatizadas**: 32 pruebas ejecutadas y aprobadas en 0.21 segundos.
- **Latencia NFR-01**: < 15 ms para 1,000 registros (límite: 50 ms).
- **Códigos de Salida CLI**: 0 (éxito), 1 (fallo de datos/sistema), 2 (error de validación).
- **Trazabilidad**: 100% de los requisitos `FR-01` a `FR-06` y `NFR-01` a `NFR-03` cuentan con mapeo directo a criterios de aceptación, tareas, código y tests.

## Lessons Learned
1. Separar los requerimientos (`REQUIREMENTS.md`) de la especificación técnica verificable (`SPEC.md`) evita la ambigüedad y permite al agente implementar código sin inventar reglas de negocio.
2. Contar con un archivo de gobernanza (`AGENTS.md`) define límites claros para el agente de codificación, evitando modificaciones indebidas a los requisitos cuando un test no pasa inicialmente.
3. El enfoque *spec-driven* reduce drásticamente el tiempo de refactorización y depuración: el código se escribe una sola vez con los contratos de entrada y salida claramente delimitados.
