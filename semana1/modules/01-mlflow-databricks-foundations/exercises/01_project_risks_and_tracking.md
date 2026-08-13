# Práctica 01 — Evidencia antes de producción

**Duración:** 3–4 horas · **Modalidad:** individual o por parejas

## Objetivo

Transformar un entrenamiento en un ciclo observable: candidatos comparables,
selección sin contaminar test, versión registrada, API local del `model.joblib` ganador
y evidencia operativa. Completar después una traza y evaluación de agente.

## Antes de empezar

1. Abre tu notebook en Databricks Free Edition. MLflow crea automáticamente el
   experimento del notebook cuando inicias un run; ábrelo desde **Experiments**
   en la barra lateral.
2. Elige un alias de equipo que no revele información personal, por ejemplo
   `pareja-07`.
3. No pegues claves, tokens, correos, datos de pacientes ni contenido sensible
   en ninguna celda. MLflow registra lo que le entregas.

## Parte A — Ciclo de ML con MLflow (150–210 min)

1. Completa `notebooks/01_tracking_mlops.ipynb` siguiendo su guía específica.
2. Genera siete candidatos con evidencia completa y el mismo split.
3. Aplica el gate sobre validación y abre test sólo para el ganador.
4. Registra el ganador, asigna `Champion` y verifica carga por alias.
5. Sirve el `model.joblib` en localhost, prueba éxito/error, registra señales y apágalo.
6. Adapta `examples/s01_project_record.yaml` y regístralo como artefacto.

## Parte B — AgentOps y LLMOps (30–45 min)

1. Ejecuta `notebooks/02_agent_llmops.ipynb` con `USE_LLM = False`.
2. Abre una traza de `course_agent` y localiza sus pasos `route_question` y
   `retrieve_course_context`. Escribe qué paso habría permitido depurar una
   respuesta incorrecta.
3. Ejecuta la evaluación. Identifica un caso que el *scorer*
   `contains_expected_phrase` considera correcto y explica por qué ese criterio
   no basta para autorizar producción.
4. Sólo si el docente lo indica, habilita el endpoint de Foundation Model y
   repite una pregunta. No cambies la configuración de autenticación.

## Parte C — Entregable y debrief (20 min)

Entrega una ficha corta (Markdown, YAML o enlace a su artefacto de MLflow) con:

- alias de equipo, nombre y enlace del experimento;
- `batch.id`, tabla de candidatos y regla del gate;
- ganador, métricas de validación/test y evidencia que todavía falta;
- nombre, versión y alias del modelo registrado;
- run de deployment y resultados 200/200/400/400 de la API;
- tres riesgos priorizados y su propietario;
- enlace o identificador de una traza y el límite del *scorer* usado.

## Rúbrica (10 puntos)

| Criterio | Puntos |
| --- | ---: |
| Siete runs comparables con inputs, parámetros, métricas y artefactos | 2 |
| Gate reproducible y test reservado únicamente al ganador | 2 |
| Registry con firma, versión, tags y alias `Champion` | 2 |
| API local: pickle, contrato, pruebas, observabilidad y apagado | 2 |
| Trazas/evaluación y decisión prudente sin secretos ni uso clínico | 2 |

## Extensión si terminas antes

Propón un *scorer* adicional que detecte un riesgo que el actual no cubre
(por ejemplo, latencia, cita de fuentes, lenguaje inseguro o ausencia de una
respuesta de incertidumbre). Describe la entrada, la salida y un contraejemplo
que podría engañarlo.
