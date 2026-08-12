# Sesión 02 — Tracking, trazas y evaluación en Free Edition

**Duración:** 1 hora de demostración/concepto + 1 hora de práctica

## Resultado de aprendizaje

El alumnado crea un lote de runs comparables, aplica un gate, registra el
ganador y prueba su API local en Databricks Free Edition. También inspecciona
una traza de agente y ejecuta una evaluación LLMOps sin un endpoint de pago.

## Secuencia

### Concepto breve (15 min)

Explica por qué Free Edition usa experimentos de notebook: el compute es
serverless y limitado, y cada estudiante puede reproducir su evidencia sin
permisos sobre un experimento compartido. Distingue métrica de modelo, traza de
aplicación y *scorer* de evaluación.

### Construcción en directo (45 min)

Ejecuta las secciones 1–8 de
[`01_tracking_mlops_solucion.ipynb`](../../notebooks/01_tracking_mlops_solucion.ipynb)
y muestra datos, parámetros, artefactos, comparación y gate. Resume las
secciones Registry/API, que se terminarán como trabajo autónomo. Después
ejecuta el modo determinista de
[`02_agent_llmops_solucion.ipynb`](../../notebooks/02_agent_llmops_solucion.ipynb)
y abre la traza resultante.

### Extensión independiente (45 min)

El alumnado inicia las versiones sin resolver
[`01_tracking_mlops.ipynb`](../../notebooks/01_tracking_mlops.ipynb) y
[`02_agent_llmops.ipynb`](../../notebooks/02_agent_llmops.ipynb), siguiendo la
[práctica de semana 01](../../exercises/01_project_risks_and_tracking.md). El
ciclo ML completo requiere 2–3 horas adicionales fuera de clase.

### Debrief (15 min)

Compara el lote de candidatos, la versión `Champion`, el run de despliegue y
una evaluación. Cierra preguntando qué evidencia falta antes de producción y
qué limitación del *scorer* requiere otra capa de evaluación.
