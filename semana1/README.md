# Semana 1 — Fundamentos de MLOps con MLflow

Esta semana introduce el paso de un notebook experimental a una operación
observable con MLflow y Databricks Free Edition.

El material completo está en
[`modules/01-mlflow-databricks-foundations/`](modules/01-mlflow-databricks-foundations/).
Incluye dos sesiones, dos prácticas de notebook, una ficha de proyecto, una
guía docente y el dataset didáctico en `data/raw/heart.csv`.

## Recorrido

1. [Del prototipo a la operación](modules/01-mlflow-databricks-foundations/sessions/01-prototipo-a-operacion/README.md)
2. [Tracking, trazas y evaluación en Free Edition](modules/01-mlflow-databricks-foundations/sessions/02-mlflow-free-edition/README.md)
3. [Guía de la práctica de ciclo de vida](modules/01-mlflow-databricks-foundations/exercises/01_tracking_mlops/README.md)
4. [Guía de AgentOps y LLMOps](modules/01-mlflow-databricks-foundations/exercises/02_agent_llmops/README.md)

## Entorno

Las prácticas están diseñadas para abrirse como Git Folder en Databricks Free
Edition. El notebook de ciclo de vida usa el dataset relativo a esta semana:

```text
semana1/data/raw/heart.csv
```

No se necesitan credenciales, endpoints de pago ni datos reales de pacientes.
El resultado es exclusivamente didáctico y no debe utilizarse para diagnóstico
ni para tomar decisiones sobre pacientes.
