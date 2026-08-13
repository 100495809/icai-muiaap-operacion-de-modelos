# Semana 5 — Primera interfaz Streamlit para un modelo

La semana 5 convierte el bundle ejecutable de S4 en una primera interfaz web
usable. El objetivo no es construir todavía una aplicación compleja: el
alumnado aprende el modelo mental de Streamlit, dibuja un formulario, recoge
los once campos del contrato y presenta una predicción del modelo empaquetado.

La semana 6 partirá de esta aplicación y añadirá estado explícito, caché,
errores ricos, confianza, latencia y telemetría. Por eso en S5 no se pide aún
una máquina de estados ni una arquitectura avanzada de sesión.

## Continuidad

| Semana | Se conserva | Se añade en S5 |
| --- | --- | --- |
| [S1](../semana1/README.md) | La ficha de riesgos y la distinción entre prototipo y servicio | La interfaz hace visible un límite de confianza y un error recuperable. |
| S2 | Repositorio, dependencias y estructura modular | La app vive en el proyecto reproducible y no concentra la inferencia en el notebook. |
| [S3](../semana3/README.md) | `WineQualityRequest`, las once features y la salida validada | El formulario recoge los mismos nombres y no reimplementa el preprocesado. |
| [S4](../semana4/README.md) | `manifest.json`, `model.joblib`, versiones y `infer_wine_quality()` | Un gateway conecta el bundle con una interfaz Streamlit sin duplicar su carga. |
| S5 | Primera UI funcional | La app y su contrato visual se convierten en la entrada de S6. |

## Clases

### Clase 1 — Streamlit básico y modelo mental de rerun

Se explica cómo se ejecuta una app Streamlit, cómo se crean widgets y cómo un
formulario recoge una petición. La demo conecta un gateway determinista y, si
está disponible, el bundle de S4. No se introduce todavía `st.session_state`,
`st.cache_resource` ni una máquina de estados: esas decisiones son el foco de
S6.

[Material de la clase 1](modules/05-streamlit-basic-model-ui/sessions/01-streamlit-basics/README.md)

### Clase 2 — Taller: primera interfaz del modelo

La pareja implementa una pantalla mínima: formulario, botón, llamada al
gateway, resultado y mensaje de error básico. La app debe quedar lista para
ser refactorizada en S6.

[Material de la clase 2](modules/05-streamlit-basic-model-ui/sessions/02-first-model-ui/README.md)

## Prácticas y entregables

- [Práctica 01 — contrato del formulario](modules/05-streamlit-basic-model-ui/exercises/01-ui-form-contract/problem/README.md): decidir campos, labels y mapeo al contrato S4.
- [Práctica 02 — primera app Streamlit](modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/README.md): completar el starter y ejecutar una inferencia desde el navegador.
- [Solución docente](modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/README.md).

La entrega de S5 es:

- una app Streamlit que arranca desde un checkout limpio;
- un formulario con las once características del contrato;
- una predicción visible con categoría, confianza y versiones;
- un error básico comprensible cuando la inferencia no está disponible;
- una captura o registro de la app funcionando.

La app demo puede usar `DemoGateway` sin un modelo binario. El modo real se
activa con `MODEL_UI_BUNDLE`, apuntando al directorio del bundle de S4.

## Ejecución

Desde `semana5/`:

```bash
uv sync
uv run pytest
uv run ruff check modules/05-streamlit-basic-model-ui/solutions
uv run ruff format --check modules/05-streamlit-basic-model-ui/solutions
uv sync --extra app
uv run streamlit run modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/app.py
```

Desde el starter del alumnado:

```bash
cd modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter
uv sync
uv run pytest
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```
