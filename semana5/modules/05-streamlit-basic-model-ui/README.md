# Módulo — Streamlit básico para consumo de modelos

Este módulo enseña la primera capa visual sobre la inferencia de S4. La
interfaz es deliberadamente sencilla para que S6 pueda convertirla en una app
con estado y comportamiento avanzado.

## Responsabilidades

```text
widgets/formulario -> valores del contrato -> gateway S4 -> resultado -> pantalla
```

- `app.py` conoce Streamlit y presenta la pantalla.
- `gateway.py` adapta el bundle de S4 o el gateway demo.
- `contracts.py` valida el payload que entra en la UI.
- `presentation.py` convierte categorías y metadatos en texto corto.

La estructura y las dependencias siguen el repositorio preparado en S2; los
riesgos identificados en S1 se convierten aquí en mensajes visibles y límites
de interpretación. S5 no crea un contrato nuevo: reutiliza la entrada de S3 y
la salida empaquetada de S4.

La app de S5 no carga `joblib` desde la capa visual, no reconstruye el vector de
features y no convierte todavía el rerun de Streamlit en una máquina de
estados. La siguiente semana extraerá esas decisiones.

## Resultado esperado

Otra persona puede arrancar la app, introducir una muestra, pulsar un botón,
ver una predicción y entender qué versión del modelo la produjo.
