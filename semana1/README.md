# Semana 1 — Fundamentos de MLOps con MLflow

Esta semana introduce el paso de un notebook experimental a una operación
observable con MLflow y Databricks Free Edition.

El material completo está en
[`modules/01-mlflow-databricks-foundations/`](modules/01-mlflow-databricks-foundations/).
Incluye dos clases, dos prácticas de notebook, una ficha de proyecto, una guía
docente y el dataset didáctico en `data/raw/heart.csv`.

## Clase 1 — Del prototipo a la operación

Contenido conceptual y de diseño: diferencia entre prototipo y producción,
unidades de evidencia de MLflow, riesgos iniciales y lectura crítica de un
notebook heredado.

La práctica consiste en completar la ficha de proyecto con una decisión, los
límites del dato y riesgos con propietario y mitigación.

[Material de la clase 1](modules/01-mlflow-databricks-foundations/sessions/01-prototipo-a-operacion/README.md)

## Clase 2 — Tracking, trazas y evaluación

Construcción práctica del ciclo de MLflow: runs comparables, métricas,
artefactos, gate, Registry, alias `Champion`, API local y observabilidad.
También se trabaja AgentOps/LLMOps con trazas y evaluación determinista.

[Material de la clase 2](modules/01-mlflow-databricks-foundations/sessions/02-mlflow-free-edition/README.md)

## Prácticas y entregables

- [Práctica de ciclo de vida de ML](modules/01-mlflow-databricks-foundations/exercises/01_tracking_mlops/README.md): runs, gate, Registry y API local.
- [Práctica de AgentOps y LLMOps](modules/01-mlflow-databricks-foundations/exercises/02_agent_llmops/README.md): trazas, evaluación y fallos controlados.
- [Ficha de proyecto y riesgos](modules/01-mlflow-databricks-foundations/exercises/01_project_risks_and_tracking.md): entregable común de la semana.

## Entorno

Las prácticas están diseñadas para abrirse como Git Folder en Databricks Free
Edition. El notebook de ciclo de vida usa el dataset relativo a esta semana:

```text
semana1/data/raw/heart.csv
```

No se necesitan credenciales, endpoints de pago ni datos reales de pacientes.
El resultado es exclusivamente didáctico y no debe utilizarse para diagnóstico
ni para tomar decisiones sobre pacientes.

## Cómo comprobar la semana

La semana 1 no tiene una suite `pytest` local: sus prácticas son notebooks
pensados para Databricks Free Edition. Desde la raíz de esta semana se pueden
validar la estructura, el dataset y el formato JSON de todas las libretas:

```bash
cd semana1
test -f data/raw/heart.csv
find modules -name '*.ipynb' -print0 | xargs -0 -n1 jq empty
```

Para comprobar el comportamiento didáctico, abre la carpeta `semana1/` como
Git Folder en Databricks y ejecuta las versiones `_solucion.ipynb`. Después
ejecuta las versiones sin resolver para que el alumnado complete sus `TODO`.
