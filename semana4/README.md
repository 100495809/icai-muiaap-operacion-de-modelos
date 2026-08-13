# Semana 4 — Serialización y validación de modelos

Material reproducible de Operación de Modelos para la cuarta semana del
MUIAAp. Esta semana continúa el módulo local de inferencia de ../semana3 y
convierte el modelo serializado en un artefacto explícito, inspeccionable y
ejecutable.

## Resultado de la semana

El alumnado termina con un bundle formado por:

~~~text
models/wine_quality_bundle/
├── manifest.json       # contrato legible y validable
└── model.joblib        # estimador serializado
~~~

La primera clase diseña el manifiesto y comprueba qué incompatibilidades deben
rechazarse. La segunda implementa el guardado, la carga, la validación de
inputs/outputs, una CLI local y pruebas básicas.

## Material

- [README y mapa de la unidad](modules/04-model-packaging/README.md)
- [Notebook guiado de clase 1](modules/04-model-packaging/sessions/01-serializacion-validacion/notebooks/01-serializacion-validacion-guiada.ipynb)
- [Guion de prácticas de clase 1](modules/04-model-packaging/guides/class-1-practices.md)
- [Guion del taller de clase 2](modules/04-model-packaging/guides/class-2-workshop.md)
- [Starter del taller](modules/04-model-packaging/exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter/)
- [Solución docente](modules/04-model-packaging/solutions/01.02-serializable-inference-module/)

Los datos de ejemplo se reutilizan desde
../semana3/assets/03-wine-quality/inference_samples.csv; no se duplica la
fuente de verdad entre semanas.

## Validación docente

Desde esta carpeta:

~~~bash
uv sync
uv run pytest
uv run ruff check modules/04-model-packaging/solutions
uv run ruff format --check modules/04-model-packaging/solutions
~~~

Para revisar el starter como lo recibe el alumnado:

~~~bash
cd modules/04-model-packaging/exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter
uv sync
uv run pytest
~~~

El starter empieza rojo porque conserva los TODO del taller; debe quedar
verde después de la implementación de la pareja.
