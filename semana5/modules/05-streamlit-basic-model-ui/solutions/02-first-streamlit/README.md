# Solución — Primera interfaz Streamlit

La solución completa mantiene la app como adaptador del gateway:

- `app.py`: formulario y renderizado básico;
- `contracts.py`: payload validado;
- `gateway.py`: demo y bundle de S4;
- `presentation.py`: etiquetas y copy mínimo.

## Ejecución

Desde `semana5/`:

```bash
uv run pytest
uv run --extra app streamlit run modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/app.py
```

Sin `MODEL_UI_BUNDLE`, la pantalla usa `DemoGateway`. Para probar el bundle de
S4:

```bash
MODEL_UI_BUNDLE=/ruta/al/wine_quality_bundle \
  uv run --extra app streamlit run modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/app.py
```

Esta solución es el snapshot conceptual que S6 debe mejorar: no conserva la
última respuesta con `st.session_state`, no cachea el gateway de forma
explícita y no modela las transiciones como estados observables.
