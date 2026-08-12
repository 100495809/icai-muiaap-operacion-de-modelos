# Semana 01 — De un notebook a una operación observable

Este módulo está integrado en `semana1/` del repositorio ICAI MUIAAp. Abre la
carpeta `semana1/` como Git Folder para que los notebooks encuentren el dataset
en `data/raw/heart.csv`.

## Resultado de aprendizaje

Al terminar la semana, el alumnado distingue un prototipo de un sistema
operable y recorre en Databricks el ciclo de MLflow: tracking de datos,
parámetros, métricas, artefactos y modelos; elección mediante un gate; test
reservado; Registry con alias; y despliegue local del pickle ganador mediante
una API observable. Además registra una traza de agente y una evaluación mínima
de una aplicación con LLM.

## Secuencia didáctica

El detalle por sesión está en [Sesión 01](sessions/01-prototipo-a-operacion/README.md)
y [Sesión 02](sessions/02-mlflow-free-edition/README.md).

### 1. Concepto breve — Clase 1 (120 min)

- Prototipo frente a producción: qué cambia cuando hay usuarios, costes,
  fallos, datos sensibles y requisitos de reproducibilidad.
- Un experimento como unidad común de evidencia: *runs* de entrenamiento,
  trazas de aplicaciones y evaluaciones de GenAI.
- Riesgos iniciales: datos, sesgo, seguridad, coste, latencia, alucinación y
  ausencia de trazabilidad.
- Lectura guiada de un notebook heredado: localizar valores codificados,
  rutas personales, artefactos frágiles y ausencia de un contrato de entrada.

### 2. Construcción en directo — Clase 2, primera hora (60 min)

El docente ejecuta las celdas esenciales de
[`notebooks/01_tracking_mlops_solucion.ipynb`](notebooks/01_tracking_mlops_solucion.ipynb): usa el
experimento del notebook, crea seis candidatos reproducibles y muestra cómo los
inputs, firma, artefactos y métricas permiten comparar. Después aplica el gate,
registra `Champion` y prueba una API HTTP local que carga el pickle ganador.

### 3. Extensión independiente — Clase 2, segunda hora (60 min)

El alumnado inicia la [práctica](exercises/01_project_risks_and_tracking.md) en
clase y termina el ciclo profundo como trabajo autónomo. Después ejecuta el modo determinista de
[`notebooks/02_agent_llmops_solucion.ipynb`](notebooks/02_agent_llmops_solucion.ipynb), inspecciona la
traza y ejecuta el *scorer* de código. Si la cuenta tiene capacidad y el docente
lo indica, habilita la llamada a un endpoint como extensión; nunca con una clave
pegada en el notebook.

### 4. Debrief (20 min)

- ¿Qué evidencia permite reproducir o descartar un experimento?
- ¿Qué parte de la traza explica una respuesta incorrecta?
- ¿Qué métrica o *scorer* sería insuficiente para autorizar producción?
- ¿Cuál es el riesgo más urgente del caso y quién debe asumirlo?

## Material

| Recurso | Uso |
| --- | --- |
| `notebooks/01_tracking_mlops.ipynb` | Ciclo ML completo sin resolver; 3–4 horas. |
| `notebooks/01_tracking_mlops_solucion.ipynb` | Solución docente de MLOps. |
| `notebooks/02_agent_llmops.ipynb` | Práctica AgentOps/LLMOps sin resolver; 60–90 minutos. |
| `notebooks/02_agent_llmops_solucion.ipynb` | Solución docente de AgentOps/LLMOps. |
| `exercises/01_tracking_mlops/README.md` | Guía de alumno para el tracking clásico. |
| `exercises/02_agent_llmops/README.md` | Guía de alumno para trazas y evaluación. |
| `exercises/01_project_risks_and_tracking.md` | Entregable individual o por pareja. |
| `examples/s01_project_record.yaml` | Plantilla de la ficha de proyecto y riesgos. |
| `instructor/README.md` | Preparación y guion para el docente. |

## Convenciones de la semana

- En Free Edition cada notebook conserva su propio experimento; el nombre del
  *run* contiene el alias del estudiante, nunca su correo ni datos personales.
- El Registry usa Unity Catalog y nombres de tres niveles. El alias `Champion`
  representa la versión elegida; no implica aprobación para producción.
- La API se limita a `127.0.0.1` dentro del driver, usa un puerto efímero y se
  apaga al acabar. No es pública ni persistente y no consume un endpoint.
- Los secretos viven en Databricks Secrets o en la identidad del entorno; no
  se registran como parámetros, *tags*, artefactos ni salidas de trazas.
- Cada artefacto debe poder explicarse: finalidad, propietario, datos usados y
  criterio para pasar a la siguiente etapa.
- El modelo clásico, la aplicación de agente y la evaluación se observan desde
  el experimento del notebook para que se vea el ciclo completo; en producción
  se separarán por sistema y por permisos.

## Referencias técnicas

- [Experimentos de MLflow en Databricks](https://docs.databricks.com/aws/en/mlflow/experiments)
- [Tracking de modelos en Databricks](https://docs.databricks.com/aws/en/mlflow/tracking)
- [Ciclo de modelos en Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle)
- [Límites de Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations)
- [Trazas de agentes y LLMs en MLflow](https://mlflow.org/docs/latest/genai/tracing)
- [Evaluación de GenAI en MLflow](https://mlflow.org/docs/latest/genai/eval-monitor/)
