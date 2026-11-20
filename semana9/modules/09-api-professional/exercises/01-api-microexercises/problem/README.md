# Ejercicio 01 — Microejercicios de la clase 1

Cuatro microejercicios de 5 minutos, uno al final de cada bloque de teoría. Se
hacen sobre las demos de [`examples/`](../../../examples/README.md) y no
requieren escribir una API nueva.

Prepara el entorno una vez, desde `semana9/modules/09-api-professional`:

```bash
uv sync --locked
```

## M1 — Serialización (bloque 1)

Arranca `uv run fastapi dev examples/serialization_demo.py` y compara
`/v1/scores/leaky` con `/v1/scores/public`.

1. Anota qué campos aparecen en la primera respuesta y no en la segunda.
2. Explica en una frase por qué `/v1/scores/filtered` tampoco los devuelve,
   aunque la función devuelve un `dict` con todos ellos.
3. En `/docs`, abre el esquema `PublicScore`: ¿aparece `is_reliable`?

**Comprobación:** tu respuesta a la pregunta 2 menciona `response_model` y
qué hace con los campos que no declara.

## M2 — Errores (bloque 2)

Arranca `uv run fastapi dev examples/errors_demo.py` y envía, desde `/docs` o
con `curl`, tres peticiones a `POST /v1/scores`:

- `{"age": 30, "income": 1000}`
- `{"age": "treinta", "income": 1000}`
- `{"age": 30}`

Después llama a `GET /v1/nada` y a `GET /v1/boom`.

1. Rellena una tabla con status, `error.code` y `error.fields` de cada caso.
2. ¿Qué devolvería FastAPI en el segundo caso si borraras `handle_validation`?
   Pruébalo comentando el decorador y restáuralo después.

**Comprobación:** las cinco respuestas de error tienen la clave `error` en la
raíz y ninguna contiene el texto `TU_SECRETO`.

## M3 — OpenAPI (bloque 3)

Arranca `uv run fastapi dev examples/openapi_demo.py`.

1. Localiza en `/openapi.json` dónde terminan `summary`, el docstring y
   `responses` de `create_score`.
2. Ejecuta el ejemplo `minor` desde Swagger con «Try it out».
3. Añade un tercer ejemplo `no_income` sin el campo `income` y comprueba que
   aparece en el desplegable.

**Comprobación:** `uv run pytest -q` sigue en verde y el desplegable muestra
tres ejemplos. Deshaz el cambio al terminar o adapta el test que cuenta los
ejemplos.

## M4 — Tests (bloque 4)

Abre [`tests/test_examples.py`](../../../tests/test_examples.py).

1. Ejecuta `uv run pytest -q` y localiza el test que usa `dependency_overrides`.
2. Elimina temporalmente `raise_server_exceptions=False` del fixture
   `errors_client` y vuelve a ejecutar. Explica qué cambia.
3. Escribe un test nuevo que compruebe que `income: 0` devuelve `422` con
   `fields[0].field == "income"`.

**Comprobación:** la suite vuelve a estar en verde con tu test incluido.

La [solución comentada](../solution/README.md) se comparte al final de la clase.

---

## Respuestas

### M1 — Serialización
1. **Campos en /v1/scores/leaky que no están en /v1/scores/public**:
   - `raw_score`
   - `threshold_config`
2. **Por qué /v1/scores/filtered tampoco los devuelve**:
   - Porque tiene puesto `response_model=PublicScore`, así que FastAPI solo devuelve los campos que están en ese modelo y quita todo lo demás aunque la función devuelva un diccionario con más cosas.
3. **¿Aparece `is_reliable` en /docs para `PublicScore`?**:
   - Sí, porque tiene encima el `@computed_field` y por eso FastAPI lo mete en la documentación.

### M2 — Errores
1. **Tabla de respuestas**:

| Petición | Status | `error.code` | `error.fields` |
| :--- | :---: | :--- | :--- |
| `{"age": 30, "income": 1000}` | 200 | — | — |
| `{"age": "treinta", "income": 1000}` | 422 | `validation_error` | `[{"field": "age", ...}]` |
| `{"age": 30}` | 422 | `validation_error` | `[{"field": "income", ...}]` |
| `GET /v1/nada` | 404 | `not_found` | — |
| `GET /v1/boom` | 500 | `internal_error` | — |

2. **Respuesta sin `handle_validation`**:
   - Devuelve el JSON con `detail` que viene por defecto en FastAPI en vez de nuestra clave `error`. Además mete dentro el `"input": "treinta"` que ha mandado el usuario:
     ```json
     {"detail": [{"type": "int_parsing", "loc": ["body", "age"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "treinta"}]}
     ```

### M3 — OpenAPI
1. **Ubicación en `/openapi.json`**:
   - `summary`: en `paths["/v1/scores"]["post"]["summary"]`
   - Docstring: en `paths["/v1/scores"]["post"]["description"]`
   - `responses`: en `paths["/v1/scores"]["post"]["responses"]` (los errores 422 y 503 apuntando a `ErrorResponse`)
2. **Ejemplo `minor`**: probado desde la interfaz de Swagger dándole a "Try it out".
3. **Ejemplo `no_income`**: añadido a `examples/openapi_demo.py` y comprobado en el desplegable de Swagger.

### M4 — Tests
1. **Test con `dependency_overrides`**: `test_dependency_override_simulates_unavailable_model` (se usa para simular que el modelo está caído).
2. **Qué cambia al quitar `raise_server_exceptions=False`**:
   - El test de `/v1/boom` peta directamente con un `RuntimeError` en la consola porque la excepción salta a pytest en vez de ser manejada. Con `raise_server_exceptions=False` el test recibe el error HTTP 500 normal y comprueba que no se filtra ninguna contraseña o secreto.
3. **Test nuevo añadido**: `test_zero_income_is_rejected` añadido en `tests/test_examples.py` (comprueba el 422 y que el campo que falla sea `income`).

