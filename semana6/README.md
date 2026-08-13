# Semana 6 — UX para IA, errores, latencia y confianza

Material reproducible de Operación de Modelos para la sexta semana del MUIAAp.
La semana mejora una interfaz de inferencia para que comunique estados, errores,
latencia, confianza y trazabilidad sin duplicar la lógica del modelo.

## Resultado de la semana

El alumnado termina con una demo de consumo más usable y robusta:

```text
formulario -> controlador de estados -> gateway de inferencia -> vista segura
                                  \-> telemetría agregada
```

La interfaz consume el contrato y el bundle de la semana 4. No entrena otro
modelo, no cambia el manifiesto y no expone todavía una API HTTP: el gateway es
la frontera que la semana 7 sustituirá por un cliente REST.

## Continuidad con las semanas anteriores

| Semana | Decisión que se conserva | Cómo se usa aquí |
| --- | --- | --- |
| [S1](../semana1/README.md) | Riesgos, evidencia y límites de interpretación | La confianza se presenta como señal orientativa, no como garantía; la UI no muestra payloads en la telemetría y cada error tiene una acción de recuperación. |
| [S3](../semana3/README.md) | `WineQualityRequest`, `WineQualityPrediction`, preprocesado y separación del módulo local | El formulario entrega los nombres de las once características al gateway; la UI no reimplementa `predict`, `predict_proba` ni el orden del vector. |
| [S4](../semana4/README.md) | `manifest.json`, `model.joblib`, versiones y validación de entrada/salida | El modo empaquetado carga el bundle de S4 y muestra `model_version` y `preprocessing_version` como trazabilidad. |

## Clases

### Clase 1 — UX para IA y diseño de estados

Se analiza la diferencia entre un resultado técnicamente válido y una
experiencia operable: carga, éxito, confianza baja, error de contrato, modelo
no disponible y latencia por encima del objetivo. La pareja completa una matriz
de estados y define mensajes, acciones y evidencias.

[Material de la clase 1](modules/06-ux-model-consumption/sessions/01-ux-estados-confianza/README.md)

### Clase 2 — Taller de interfaz robusta

Se implementa un controlador independiente de Streamlit, con traducción de
errores, política de confianza, objetivo de latencia y telemetría agregada. La
interfaz Streamlit queda como adaptador fino y el mismo gateway puede consumir
el bundle local de S4 o un backend de demostración.

[Material de la clase 2](modules/06-ux-model-consumption/sessions/02-interfaz-robusta/README.md)

## Prácticas y entregables

- [Práctica 01 — contrato UX y estados](modules/06-ux-model-consumption/exercises/01-ui-contract/problem/README.md): matriz de estados, mensajes y criterios de aceptación.
- [Práctica 02 — interfaz robusta](modules/06-ux-model-consumption/exercises/02-robust-streamlit/README.md): controlador, errores, confianza, latencia, telemetría y adaptador Streamlit.
- [Guion de la clase 1](modules/06-ux-model-consumption/guides/class-1-practices.md).
- [Guion de la clase 2](modules/06-ux-model-consumption/guides/class-2-workshop.md).

El entregable es la copia del starter de la práctica 02, la matriz de la
práctica 01 y una captura o registro de estas evidencias:

- estado de carga y estado de éxito;
- confianza baja comunicada sin lenguaje de garantía;
- error de entrada accionable y sin traceback para el usuario;
- latencia visible junto con las versiones del modelo y preprocesado;
- snapshot de telemetría sin valores de entrada.

## Ejecución y verificación

Desde esta carpeta:

```bash
uv sync
uv run pytest
uv run ruff check modules/06-ux-model-consumption/solutions
uv run ruff format --check modules/06-ux-model-consumption/solutions
```

Para revisar el proyecto que recibe el alumnado:

```bash
cd modules/06-ux-model-consumption/exercises/02-robust-streamlit/problem/starter
uv sync
uv run pytest
```

El starter empieza rojo porque sus puntos de extensión contienen `TODO`; debe
quedar verde después del taller.

Para ejecutar la solución Streamlit se necesita la dependencia opcional:

```bash
cd semana6
uv sync --extra app
uv run streamlit run modules/06-ux-model-consumption/solutions/02-robust-streamlit/app.py
```

Sin configurar nada, la app utiliza un gateway determinista de demostración. Para
consumir el bundle real de la semana 4, define `MODEL_UI_BUNDLE` con la ruta al
directorio `models/wine_quality_bundle/`. El artefacto sigue siendo local y de
confianza; no se incluyen modelos binarios en Git.
