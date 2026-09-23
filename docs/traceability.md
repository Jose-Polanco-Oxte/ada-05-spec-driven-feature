# Matriz de Trazabilidad — Customer Search

La trazabilidad conecta cada requisito definido en `REQUIREMENTS.md` con su especificación verificable en `SPEC.md`, las tareas ejecutadas en `TASKS.md`, los archivos de código fuente generados y sus respectivas pruebas automatizadas.

| Requirement | SPEC / AC | Task | Files | Test | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** | AC-01, Regla de búsqueda 1 y 2 | T-03, T-05 | `src/search_service.py` | `tests/test_search_service.py::test_search_by_name_partial_case_insensitive_and_accents` | OK | Soporta coincidencia parcial, insensible a mayúsculas y acentos con `unicodedata NFKD`. |
| **FR-02** | AC-02, Regla de búsqueda 1 y 2 | T-03, T-05 | `src/search_service.py` | `tests/test_search_service.py::test_search_by_email_partial` | OK | Búsqueda por subcadena en email insensible a mayúsculas. |
| **FR-03** | AC-03, Regla de búsqueda 3 | T-03, T-05 | `src/search_service.py` | `tests/test_search_service.py::test_search_global_all_fields` | OK | Búsqueda unificada en campos nombre y email simultáneamente (`field="all"`). |
| **FR-04** | AC-04, Reglas V-01 y V-02 | T-04, T-05 | `src/exceptions.py`, `src/search_service.py` | `tests/test_validation.py::test_empty_query_error`, `tests/test_validation.py::test_query_too_short_error` | OK | Lanza `EmptyQueryError` ante vacíos/espacios y `QueryTooShortError` para < 2 caracteres. |
| **FR-05** | AC-05, Regla de búsqueda 4 | T-03, T-05 | `src/search_service.py` | `tests/test_search_service.py::test_search_status_filter` | OK | Filtro por cliente activo (`active`), inactivo (`inactive`) o todos (`all`). |
| **FR-06** | AC-06, CLI Spec | T-06, T-05 | `src/cli.py` | `tests/test_cli.py::test_cli_search_success`, `tests/test_cli.py::test_format_table_with_results` | OK | CLI interactiva y por banderas (`-q`, `-f`, `-s`, `--active-only`), tabla ASCII formateada. |
| **NFR-01** | Escenario 7 | T-05 | `src/search_service.py`, `src/repository.py` | `tests/test_performance.py::test_search_latency_under_50ms_for_1000_customers` | OK | Medición automatizada: 1,000 registros procesados en < 15ms (umbral máximo permitido 50ms). |
| **NFR-02** | Arquitectura en 3 capas | T-01, T-02, T-03, T-06 | `src/models.py`, `src/repository.py`, `src/search_service.py`, `src/cli.py` | Pruebas modulares independientes en `tests/` | OK | Desacoplamiento estricto entre UI (CLI), Servicio de Negocio y Repositorio de Datos. |
| **NFR-03** | Suite automatizada | T-05 | Todos los archivos de prueba en `tests/` | 32 pruebas automatizadas en `tests/` | OK | Cobertura integral de caminos lógicos, casos borde y validaciones con `pytest`. |
