# Customer Search Feature

## Goal
Proveer un motor de búsqueda local de clientes rápido, flexible y desacoplado, accesible mediante línea de comandos (CLI), que permita localizar registros por nombre o correo electrónico mediante coincidencia parcial insensible a mayúsculas y acentos, aplicando validaciones estrictas y presentando resultados claros.

## Requirements Covered
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- NFR-01
- NFR-02
- NFR-03

## Scope
- Búsqueda parcial (`substring match`) de clientes en campos de nombre y correo electrónico.
- Búsqueda unificada en ambos campos simultáneamente o por campo individual.
- Normalización diacrítica (eliminación de acentos para comparación) y normalización de mayúsculas/minúsculas.
- Validación de términos de búsqueda (longitud mínima de 2 caracteres sin espacios, detección de cadenas vacías o solo espacios).
- Filtrado opcional por estado de cliente (`all`, `active`, `inactive`).
- Formato de presentación tabular en consola a través de CLI.
- Carga de datos desde archivo JSON local (`data/customers.json`) y soporte para repositorio en memoria en pruebas.
- Pruebas automatizadas con `pytest` que verifiquen lógica de dominio, validaciones y CLI.

## Out of Scope
- Interfaz gráfica web (GUI) o API HTTP REST con frameworks pesados (reservada para futuras iteraciones según requerimiento mínimo de ADA-05).
- Base de datos relacional externa (PostgreSQL, MySQL) o servidores externos de búsqueda (Elasticsearch).
- Operaciones de modificación (creación, edición, eliminación de clientes); la feature se enfoca exclusivamente en Customer Search.
- Autenticación o control de acceso multiusuario.

## Domain Model
El modelo central de dominio representa a la entidad `Customer`:
- `id` (str): Identificador único del cliente (UUID o cadena numérica/alfanumérica, e.g., "CUST-001").
- `name` (str): Nombre completo del cliente (e.g., "María José González").
- `email` (str): Correo electrónico del cliente (e.g., "maria.gonzalez@example.com").
- `phone` (str, opcional): Número de teléfono de contacto (e.g., "+52 999 123 4567").
- `is_active` (bool): Estado de la cuenta (True para activo, False para inactivo).
- `created_at` (str): Fecha de registro en formato ISO-8601 (e.g., "2024-01-15T10:30:00Z").

El modelo de consulta de búsqueda `SearchCriteria`:
- `query` (str): Término de búsqueda textual.
- `field` (str): Campo objetivo ("all", "name", "email"). Por defecto: "all".
- `status_filter` (str): Filtro de estado ("all", "active", "inactive"). Por defecto: "all".

## Search Rules
1. **Normalización Diacrítica y Case-Folding**:
   - Antes de comparar, tanto el término de búsqueda como los campos del cliente se convierten a minúsculas y se normalizan con Unicode NFKD, descartando marcas diacríticas (`Mn`).
   - Ejemplo: La búsqueda `"jose"` coincidirá con `"José"`, `"JOSÉ"` y `"jose"`.
2. **Coincidencia Parcial (Substring Matching)**:
   - Un registro es considerado coincidente si la versión normalizada del término de búsqueda es subcadena de la versión normalizada del campo evaluado (`query_norm in field_norm`).
3. **Búsqueda por Campo vs. Búsqueda Unificada**:
   - Si `field == "name"`, solo se evalúa el campo `name`.
   - Si `field == "email"`, solo se evalúa el campo `email`.
   - Si `field == "all"`, el cliente coincide si la subcadena está presente en `name` O en `email`.
4. **Filtro de Estado**:
   - Si `status_filter == "active"`, solo se retornan clientes con `is_active == True`.
   - Si `status_filter == "inactive"`, solo se retornan clientes con `is_active == False`.
   - Si `status_filter == "all"`, no se aplica restricción sobre `is_active`.
5. **Ordenamiento de Resultados**:
   - Los resultados se ordenan alfabéticamente por nombre de manera ascendente para mantener consistencia y previsibilidad.

## Validation Rules
1. **Regla V-01 (Término no vacío)**: El término de búsqueda no puede ser `None`, cadena vacía `""`, ni contener únicamente espacios en blanco. En caso de violar esta regla, se debe lanzar `EmptyQueryError`.
2. **Regla V-02 (Longitud mínima)**: El término de búsqueda tras remover espacios al inicio y final (`strip()`) debe tener una longitud de al menos 2 caracteres. Si tiene menos de 2 caracteres, se debe lanzar `QueryTooShortError`.
3. **Regla V-03 (Campo válido)**: El campo de búsqueda debe pertenecer a `{"all", "name", "email"}`. Cualquier otro valor lanzará `InvalidFieldError`.
4. **Regla V-04 (Filtro de estado válido)**: El filtro de estado debe pertenecer a `{"all", "active", "inactive"}`. Cualquier otro valor lanzará `InvalidStatusFilterError`.

## Error Handling
- Jerarquía de excepciones:
  - `CustomerSearchError(Exception)`: Excepción base del dominio de búsqueda.
    - `ValidationError(CustomerSearchError)`: Excepción base para fallas de validación.
      - `EmptyQueryError(ValidationError)`: Indica que el término de búsqueda está vacío.
      - `QueryTooShortError(ValidationError)`: Indica que el término tiene menos de 2 caracteres válidos.
      - `InvalidFieldError(ValidationError)`: Campo de búsqueda no soportado.
      - `InvalidStatusFilterError(ValidationError)`: Filtro de estado no reconocido.
    - `CustomerRepositoryError(CustomerSearchError)`: Fallas al leer o parsear el archivo JSON de datos.
- En la interfaz CLI: Las excepciones de validación son capturadas y presentadas al usuario con un mensaje de error claro en `stderr` (código de salida 2 para errores de uso/validación, 1 para errores de datos/sistema, 0 para ejecución exitosa).

## Acceptance Criteria
- **AC-01 (Búsqueda por Nombre con Coincidencia Parcial y Acentos)**:
  - Dado un término como `"garcia"`, el sistema encuentra a `"Carlos García"` y `"Ana Sofía Garcia"`.
- **AC-02 (Búsqueda por Correo con Coincidencia Parcial)**:
  - Dado un término como `"corp.com"`, el sistema retorna todos los clientes cuyo correo contenga ese dominio o fragmento.
- **AC-03 (Búsqueda Global Unificada)**:
  - Dado un término como `"alex"`, el sistema retorna tanto a `"Alex Morales"` (coincidencia en nombre) como a `"Roberto Gómez"` con correo `"alex.gomez@mail.com"` (coincidencia en correo).
- **AC-04 (Validaciones de Entrada)**:
  - Si el usuario busca `"   "` o `""`, se genera un error `EmptyQueryError` con mensaje `"El término de búsqueda no puede estar vacío."`.
  - Si el usuario busca `"a"`, se genera un error `QueryTooShortError` con mensaje `"El término de búsqueda debe tener al menos 2 caracteres."`.
- **AC-05 (Filtro por Estado)**:
  - Con criterio de búsqueda coincidente para clientes activos e inactivos, si se especifica `--status active`, solo los clientes activos son retornados.
- **AC-06 (Salida CLI Estructurada)**:
  - El comando CLI muestra una tabla formateada con columnas `ID`, `Nombre`, `Correo`, `Teléfono`, `Estado` y un resumen del total de coincidencias. Si no hay coincidencias, muestra un mensaje explícito sin fallar.

## Test Scenarios
- **Escenario 1**: Búsqueda exitosa por nombre parcial con acento.
  - *Given*: Repositorio con cliente "María Gómez".
  - *When*: Se busca `query="maria"`, `field="name"`.
  - *Then*: Se retorna el registro de "María Gómez".
- **Escenario 2**: Búsqueda por correo parcial insensible a mayúsculas.
  - *Given*: Repositorio con cliente `email="juan.perez@Empresa.com"`.
  - *When*: Se busca `query="EMPRESA"`, `field="email"`.
  - *Then*: Se retorna el registro de Juan Pérez.
- **Escenario 3**: Búsqueda combinada campo `all`.
  - *Given*: Clientes donde uno coincide por nombre y otro por correo.
  - *When*: Se ejecuta búsqueda con `field="all"`.
  - *Then*: Ambos clientes son retornados sin duplicados.
- **Escenario 4**: Validación de query con espacios y 1 carácter.
  - *Given*: Entrada de usuario `" x  "`.
  - *When*: Se valida la entrada.
  - *Then*: Se eleva `QueryTooShortError`.
- **Escenario 5**: Filtro de clientes inactivos.
  - *Given*: Dos clientes con nombre "López", uno activo y uno inactivo.
  - *When*: Se busca "lopez" con `status_filter="inactive"`.
  - *Then*: Solo se incluye el cliente inactivo.
- **Escenario 6**: Búsqueda sin coincidencias.
  - *Given*: Repositorio sin registros coincidentes con "Zzzzz".
  - *When*: Se ejecuta la búsqueda.
  - *Then*: Se retorna lista vacía `[]`.
- **Escenario 7**: Prueba de latencia (< 50ms para 1,000 clientes).
  - *Given*: Conjunto sintético de 1,000 clientes.
  - *When*: Se ejecuta la búsqueda sobre el repositorio.
  - *Then*: El tiempo de ejecución es estrictamente menor a 50 ms.

## Constraints
- Se debe utilizar Python estándar (`dataclasses`, `argparse`, `unicodedata`, `json`, `time`) sin dependencias de terceros para producción.
- No se utilizan bases de datos externas; la persistencia se apoya en JSON local.

## Open Questions
- N/A: Todas las preguntas abiertas identificadas en REQUIREMENTS.md (`Q-01` y `Q-02`) han sido resueltas en los criterios de aceptación y reglas de búsqueda.
