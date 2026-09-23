# Tasks

## T-01 Project setup
- Goal: Establecer la estructura base del proyecto, directorios `src/`, `tests/`, `docs/`, `data/`, `results/`, archivo `.gitignore`, configuración inicial de pytest y dataset de prueba inicial `data/customers.json`.
- Files: `.gitignore`, `pytest.ini`, `data/customers.json`, `src/__init__.py`, `tests/__init__.py`.
- Acceptance: La estructura de carpetas existe, `data/customers.json` contiene clientes de ejemplo con acentos y estados variados, y `pytest` ejecuta sin errores de configuración.
- Verification: `python -m pytest` se ejecuta correctamente (aunque no haya tests aún) y el archivo JSON es sintácticamente válido.

## T-02 Domain model
- Goal: Implementar la entidad de dominio `Customer` y los contenedores de datos necesarios para la representación inmutable y serialización de clientes.
- Files: `src/models.py`.
- Acceptance: Clase `Customer` con atributos (`id`, `name`, `email`, `phone`, `is_active`, `created_at`), métodos de conversión `from_dict` y `to_dict`, y validaciones de tipos básicos.
- Verification: Pruebas unitarias de instanciación y serialización de `Customer`.

## T-03 Search logic
- Goal: Implementar el repositorio de clientes `CustomerRepository` y el servicio central de búsqueda `CustomerSearchService` con normalización diacrítica y soporte de búsqueda parcial por nombre, correo y unificada.
- Files: `src/repository.py`, `src/search_service.py`.
- Acceptance: `CustomerRepository` carga datos desde JSON o lista en memoria. `CustomerSearchService` filtra clientes por coincidencia parcial case-insensitive e insensible a acentos en `name`, `email` o ambos, y respeta el filtro de estado `is_active`.
- Verification: Pruebas unitarias ejecutando búsquedas con acentos, coincidencias intermedias y filtrado por estado.

## T-04 Validation and errors
- Goal: Implementar la jerarquía de excepciones de dominio y las reglas de validación para los términos de búsqueda y parámetros de entrada.
- Files: `src/exceptions.py`, `src/search_service.py`.
- Acceptance: Excepciones `ValidationError`, `EmptyQueryError`, `QueryTooShortError`, `InvalidFieldError`, `InvalidStatusFilterError`. Validación que rechace cadenas vacías, espacios en blanco o longitud menor a 2 caracteres tras strip.
- Verification: Pruebas unitarias que aseguren que se lanzan las excepciones esperadas ante entradas inválidas.

## T-05 Tests
- Goal: Desarrollar la suite completa y exhaustiva de pruebas automatizadas con pytest, cubriendo todos los criterios de aceptación y escenarios definidos en SPEC.md (unitarias, validaciones, bordes y latencia).
- Files: `tests/test_domain.py`, `tests/test_search_service.py`, `tests/test_validation.py`, `tests/test_performance.py`.
- Acceptance: Cobertura de pruebas superior al 90%, verificación de latencia < 50ms para 1,000 registros, 100% de tests pasando en verde.
- Verification: `pytest -v` pasa sin ningún fallo ni advertencia crítica.

## T-06 Documentation
- Goal: Implementar la interfaz CLI interactiva y por argumentos, redactar la matriz de trazabilidad `docs/traceability.md`, el reporte del agente `results/agent-report.md`, el log de IA `AI_USAGE_LOG.md` y el manual de uso en `README.md` con respuestas a las reflexiones de la sección 18.
- Files: `src/cli.py`, `tests/test_cli.py`, `docs/traceability.md`, `results/agent-report.md`, `AI_USAGE_LOG.md`, `README.md`.
- Acceptance: La CLI permite ejecutar búsquedas desde la terminal y formatea resultados tabulares; la documentación y trazabilidad están completas y conectadas con los IDs de requerimientos.
- Verification: Ejecución manual de comandos CLI, verificación de existencia y contenido de todos los entregables requeridos.
