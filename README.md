# ADA-05: Spec-Driven Feature — Customer Search
*Ingeniería de Software Asistida por IA · UADY*

Este proyecto implementa la funcionalidad de **Customer Search** (búsqueda parcial de clientes por nombre o correo electrónico, normalización diacrítica, validaciones, interfaz CLI y pruebas automatizadas) siguiendo estrictamente el flujo *spec-driven*:
`REQUIREMENTS.md` → `SPEC.md` → `ARCHITECTURE.md` → `TASKS.md` → `AGENTS.md` → `Git Baseline` → `Implementation` → `Tests` → `Traceability` → `Review`.

---

## Estructura del Repositorio

```
ada-05-spec-driven-feature/
├── README.md                 # Guía general, ejecución y respuestas de reflexión
├── REQUIREMENTS.md           # Fuente de verdad de requisitos (FR/NFR)
├── SPEC.md                   # Comportamiento verificable, reglas y criterios de aceptación
├── ARCHITECTURE.md           # Diseño de componentes, interfaces y diagrama Mermaid
├── TASKS.md                  # Desglose de tareas T-01 a T-06
├── AGENTS.md                 # Instrucciones y reglas de gobernanza para el coding agent
├── AI_USAGE_LOG.md           # Registro de interacciones significativas con la IA
├── pytest.ini                # Configuración de ejecución de pytest
├── data/
│   └── customers.json        # Dataset inicial de clientes
├── src/
│   ├── __init__.py
│   ├── models.py             # Entidad de dominio Customer
│   ├── exceptions.py         # Excepciones del dominio
│   ├── repository.py         # Acceso a datos (JSON y memoria)
│   ├── search_service.py     # Lógica de búsqueda y normalización de texto
│   └── cli.py                # Interfaz de línea de comandos
├── tests/
│   ├── __init__.py
│   ├── test_domain.py        # Pruebas del modelo Customer
│   ├── test_search_service.py# Pruebas del motor de búsqueda y acentos
│   ├── test_validation.py    # Pruebas de validaciones y errores
│   ├── test_performance.py   # Pruebas de latencia (<50ms para 1,000 clientes)
│   └── test_cli.py           # Pruebas de integración de la CLI
├── docs/
│   └── traceability.md       # Matriz completa de trazabilidad
└── results/
    └── agent-report.md       # Reporte detallado del trabajo del agente
```

---

## Requisitos y Configuración

- **Python**: 3.11 o superior (probado en Python 3.14).
- **Dependencias**:
  - Runtime: Ninguna externa (utiliza exclusivamente la biblioteca estándar de Python).
  - Pruebas: `pytest` (>= 8.0.0).

### Instalación de Dependencias
```bash
pip install pytest
```

---

## Uso de la CLI

El comando se ejecuta mediante el módulo `src.cli`:

### 1. Búsqueda por término general (busca en nombre y correo)
```bash
python -m src.cli --query "garcia"
```

### 2. Búsqueda con acentos y mayúsculas/minúsculas
El motor normaliza diacríticos; `"jose"` encuentra `"José"`, y `"GÓMEZ"` encuentra `"Gómez"`:
```bash
python -m src.cli --query "jose"
```

### 3. Búsqueda por campo específico
```bash
# Solo en nombres
python -m src.cli --query "carlos" --field name

# Solo en correos
python -m src.cli --query "uady.mx" --field email
```

### 4. Filtrado por estado de cuenta
```bash
# Solo clientes activos
python -m src.cli --query "gomez" --active-only
# O usando --status
python -m src.cli --query "morales" --status inactive
```

### 5. Modo Interactivo
Si se ejecuta sin `--query`, la CLI solicita interactivamente el término de búsqueda:
```bash
python -m src.cli
```

### 6. Ayuda de la CLI
```bash
python -m src.cli --help
```

---

## Ejecución de Pruebas

Para ejecutar la suite completa de pruebas automatizadas (32 pruebas):
```bash
python -m pytest -v
```

Para ejecutar pruebas individuales por módulo:
```bash
python -m pytest tests/test_domain.py -v
python -m pytest tests/test_search_service.py -v
python -m pytest tests/test_validation.py -v
python -m pytest tests/test_performance.py -v
python -m pytest tests/test_cli.py -v
```

---

## Sección 18: Preguntas de Reflexión

### 1. ¿Qué diferencia hay entre requirement, specification y prompt?
- **Requirement (Requisito)**: Expresa **qué** necesita el usuario o el negocio desde una perspectiva de alto nivel (e.g., "El sistema debe permitir buscar clientes por nombre o correo"). Define la necesidad sin entrar en algoritmos o formatos.
- **Specification (Especificación)**: Define el contrato verificable, preciso y formal de **cómo debe comportarse** el sistema para satisfacer los requisitos (e.g., normalización Unicode NFKD, criterios de aceptación Given-When-Then, excepciones tipadas y reglas de validación de 2 caracteres).
- **Prompt**: Es la **instrucción operativa directa** enviada al modelo de lenguaje o agente para guiar su ejecución en un paso determinado, enmarcándolo en el contexto de las especificaciones y reglas del proyecto.

### 2. ¿Qué información fue indispensable antes de programar?
Fue indispensable contar con:
1. El modelo de datos de `Customer` (atributos exactos, tipos y restricciones de nulabilidad).
2. Las reglas de coincidencia (si la búsqueda era exacta o parcial, y cómo manejar mayúsculas y acentos en español).
3. Las reglas de validación (qué hacer con términos vacíos o de un solo carácter).
4. El mecanismo de manejo de errores (excepciones tipadas y códigos de salida del CLI).

### 3. ¿Qué decisiones debieron resolverse antes de programar?
- Resolver cómo normalizar las tildes sin dependencias externas (decisión: usar `unicodedata.normalize('NFKD', ...)`).
- Definir qué hacer cuando no hay resultados (decisión: retornar lista vacía y mensaje informativo, no lanzar error).
- Establecer la longitud mínima del término (decisión: 2 caracteres tras strip).
- Decidir el desacoplamiento de almacenamiento para admitir tanto JSON local como repositorios en memoria durante las pruebas.

### 4. ¿Qué errores evitó SPEC.md?
Evitó que el agente:
- Asumiera que la búsqueda requería una coincidencia exacta de palabras en lugar de coincidencia parcial (`substring`).
- Dejara de lado el soporte de acentos en nombres en español (un error común al usar solo `.lower()`).
- Implementara retornos ambiguos (e.g., retornar `None` o strings en lugar de una lista tipada de entidades).
- Diseñara pruebas débiles o genéricas desconectadas de los criterios de aceptación reales.

### 5. ¿Qué problema evita separar REQUIREMENTS.md de SPEC.md?
Evita la **duplicación y deriva de requisitos**. Al mantener los requisitos en `REQUIREMENTS.md` y referenciarlos por ID (`FR-01`, etc.) en `SPEC.md`, se previene que la especificación técnica modifique inadvertidamente la intención del usuario. Si un requisito cambia, la fuente de verdad es una sola, evitando contradicciones entre documentos.

### 6. ¿Qué papel tuvo AGENTS.md?
Actuó como la **constitución y gobernanza del agente**, prohibiéndole explícitamente:
- Inventar requisitos de negocio por conveniencia.
- Modificar las especificaciones o debilitar los tests para "hacerlos pasar".
- Agregar dependencias innecesarias sin justificación.
- Modificar archivos no relacionados.
Esto mantuvo al agente disciplinado y enfocado en tareas atómicas y verificables.

### 7. ¿Qué cambió durante la revisión humana?
La revisión humana detectó y corrigió:
- El intento de incluir librerías externas para normalizar texto (`unidecode`), redirigiendo a la solución con la biblioteca estándar.
- La sugerencia de montar una API HTTP pesada con base de datos, manteniéndose en la solución mínima y elegante recomendada por la práctica (CLI + JSON).
- La necesidad de una prueba de rendimiento estricta y sintética con 1,000 registros para validar objetivamente `NFR-01`.

### 8. ¿La arquitectura coincidió con el código final?
**Sí, coincidió al 100%**. La implementación final preservó exactamente la separación en tres capas proyectada en `ARCHITECTURE.md`:
- Presentación: `src/cli.py`
- Negocio/Dominio: `src/search_service.py`, `src/models.py`, `src/exceptions.py`
- Persistencia: `src/repository.py` y `data/customers.json`
El flujo de datos y las interfaces coincidieron íntegramente con el diagrama Mermaid diseñado.

### 9. ¿Qué requisito fue más difícil de probar?
El requisito **FR-06 / NFR-01** (integración CLI y rendimiento). Probar el CLI requirió simular argumentos de terminal, capturar flujos estándar (`stdout`/`stderr`), interceptar `input()` con monkeypatching y verificar códigos de salida (0, 1, 2) sin bloquear la consola. Asimismo, validar `NFR-01` requirió generar 1,000 clientes con datos pseudo-reales para asegurar mediciones de tiempo de CPU fidedignas.

### 10. ¿Qué mejorarías en tu proceso spec-driven?
En futuras iteraciones, agregaría una etapa explícita de diseño de contratos mediante esquemas formales (como dataclasses con tipado estricto `mypy` o `pydantic`) antes de la arquitectura, e incluiría matrices de cobertura de mutación de código (*mutation testing*) para asegurar que ningún criterio de aceptación sea ignorado por las pruebas.

### 11. ¿Por qué SPEC.md puede funcionar como contrato verificable sin duplicar los requisitos?
Porque `SPEC.md` utiliza una técnica de **referencia cruzada unívoca**: asocia cada criterio de aceptación (`AC-01`, `AC-02`...) a un identificador estable (`FR-01`, `FR-02`...) definido en `REQUIREMENTS.md`. De esta manera, `SPEC.md` no redefine qué se quiere lograr, sino que describe los estados del sistema, las precondiciones, entradas, salidas y excepciones (Given-When-Then), actuando como la base formal para las aserciones de `pytest`.

### 12. ¿Qué decisiones importantes aparecen en tu AI Usage Log y cómo cambió tu criterio después de revisar las sugerencias de la IA?
Aparecen decisiones cruciales como la eliminación de dependencias innecesarias, la adopción de normalización diacrítica nativa con Unicode NFKD, la preservación de la separación de capas en lugar de scripts monolíticos, y la insistencia en pruebas de estrés con 1,000 registros. Mi criterio se fortaleció al comprender que las sugerencias de la IA tienden a favorecer atajos o librerías externas de uso común que aumentan la complejidad accidental, por lo que el rol del desarrollador es guiar a la IA hacia la simplicidad, apego a estándares y respeto riguroso de la especificación.
