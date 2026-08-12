# Guía del alumno — Práctica 02: AgentOps y LLMOps

## Qué vas a conseguir

Construirás un asistente didáctico mínimo para el caso cardiovascular de la
semana y observarás cómo MLflow guarda sus pasos como trazas anidadas. Añadirás
tags de versión/ruta/modo, buscarás trazas, observarás un fallo y evaluarás ocho
casos con tres *scorers* de código.

La práctica usa `USE_LLM = False`: enseña el flujo de AgentOps y LLMOps sin
consumir cuota de un endpoint. El agente no proporciona consejo clínico.

Tiempo recomendado: 60–90 minutos.

## Antes de empezar

1. Trabaja en el mismo Databricks Git Folder que usaste para la práctica 01.
2. Abre `notebooks/02_agent_llmops.ipynb`, la libreta sin resolver.
3. Ejecuta la instalación de MLflow sólo si el runtime lo requiere. Si se
   reinicia Python, vuelve a ejecutar las celdas desde imports.
4. Mantén `USE_LLM = False`. No instales `databricks-openai`, no pegues tokens
   ni inventes nombres de endpoints salvo que el docente indique la demo.

## Orden de trabajo

1. Revisa `COURSE_CONTEXT`. Es el único contexto que el agente puede usar;
   contiene información didáctica y un límite explícito de uso clínico.
2. Completa `route_question` con las tres rutas indicadas: `mlflow`, `security`
   y `risk`. Conserva el decorador `@mlflow.trace`.
3. Completa `retrieve_course_context` para devolver el texto asociado a la ruta.
4. Completa `course_agent` en este orden: ruta → contexto → tags/metadata →
   respuesta. Usa `mlflow.update_current_trace()` para `agent.version`,
   `agent.route`, `agent.mode` y la versión de la base de conocimiento.
5. Abre **Experiments** en la barra lateral y selecciona una traza de
   `course_agent`. Identifica las trazas hijas de ruta y recuperación de
   contexto.
6. Amplía `EVALUATION_DATA` a ocho casos, con dos negativas clínicas y casos de
   seguridad, privacidad, MLflow y producción.
7. Implementa `contains_expected_phrase`, `safety_refusal` y
   `response_is_concise`. Ejecuta `mlflow.genai.evaluate(...)` con los tres.
8. Busca las trazas de `AGENT_VERSION` por tag. Provoca un `KeyError` en una
   herramienta trazada, captúralo y localiza su traza con estado `ERROR`.
9. Recupera el run de evaluación, revisa las métricas agregadas y propone un
   gate para comparar una segunda versión.

## Qué debes observar en MLflow

La traza raíz debe contener la pregunta y la respuesta. Dentro de ella deben
aparecer los pasos `route_question` y `retrieve_course_context`, además de los
tags de versión, ruta y modo. La evaluación crea evidencia por pregunta y
métricas agregadas; el fallo controlado muestra cómo distinguir `OK` de
`ERROR`. Tres heurísticas siguen sin demostrar verdad, utilidad o seguridad.

## Demo real de LLM (sólo cuando lo indique el docente)

El docente puede activar `USE_LLM = True` en la libreta resuelta y consultar un
Foundation Model API visible en **Serving**. En ese caso inspecciona el span
adicional de LLM, su latencia y el uso de tokens. No es necesario ni obligatorio
configurarlo en tu cuenta Free Edition: la cuota, los endpoints disponibles y la
capacidad pueden variar.

## Problemas habituales

| Situación | Qué hacer |
| --- | --- |
| La respuesta no sigue la ruta esperada | Imprime el resultado de `route_question(question)` y comprueba las palabras clave y el orden de condiciones. |
| No aparece una traza | Vuelve a ejecutar las definiciones con `@mlflow.trace` y después una pregunta de prueba. |
| La evaluación falla | Revisa `predict_fn`, los tres scorers y que todos los casos tengan `must_include`. |
| La búsqueda no devuelve trazas | Comprueba el tag exacto `agent.version` y ejecuta antes el conjunto de evaluación. |
| El endpoint no está disponible | Mantén `USE_LLM = False`; la práctica y el entregable siguen completos. |

## Qué entregar

Añade a la ficha común una traza `OK`, una `ERROR`, el run de evaluación, sus
tres métricas agregadas, el gate propuesto y una limitación concreta de cada
scorer. Propón un control adicional de seguridad, grounding o revisión humana.
