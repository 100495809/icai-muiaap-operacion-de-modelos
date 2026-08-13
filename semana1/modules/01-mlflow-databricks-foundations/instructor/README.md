# Preparación docente — Semana 01 (Databricks Free Edition)

## Objetivo operativo

La práctica está diseñada para que cada estudiante o pareja use su workspace
personal de Databricks Free Edition. No necesita un cluster administrado, un
experimento compartido ni un endpoint de pago. MLflow guarda
los *runs*, trazas y evaluaciones en el experimento asociado a cada notebook.

El recorrido de ML incluye tracking, selección, test reservado, Model Registry
en Unity Catalog y una API local efímera que carga el `model.joblib` ganador. La API
sólo escucha en el driver y no consume Model Serving. Registry puede requerir
un catálogo/esquema personal con permiso `CREATE MODEL`.

## Lista de comprobación (hacer antes de clase)

1. Envía al alumnado el enlace de registro de Databricks Free Edition y pide que
   accedan a su workspace antes de la sesión. Free Edition es un entorno
   serverless con cuota; deja un margen para que se active el compute.
2. Comparte este repositorio. Cada estudiante puede importarlo como Databricks
   Git Folder. Así los notebooks encuentran el caso existente `data/raw/WineQT.csv`.
   Si se suben manualmente, sube también el CSV y actualiza `DATASET_PATH`.
3. Entrega los notebooks sin resolver y conserva los pares `_solucion.ipynb`
   para la demostración y la corrección. Prueba las soluciones desde una cuenta
   Free Edition. Ejecuta sólo las
   secciones deterministas; confirma que aparece **Experiments**, que puedes
   crear un modelo en el catálogo/esquema activos y que la API local supera tres
   checks antes de apagarse.
4. No presupongas que todos tienen un endpoint de Foundation Model disponible.
   `USE_LLM = False` es el modo obligatorio y produce las trazas de herramientas
   y el flujo de evaluación. Para enseñar el span de LLM real, realiza una
   demostración breve desde tu cuenta: en **Serving** copia el nombre de un
   Foundation Model API de chat que esté visible, instala `databricks-openai`,
   asígnalo a `MODEL_ENDPOINT` y ejecuta una sola pregunta. La solución indica
   cómo inspeccionar su latencia y uso de tokens en la traza.
5. No repartas tokens personales. Dentro de un notebook de Databricks la
   autenticación del entorno es suficiente para los servicios autorizados. No
   deben aparecer secretos, correos o datos sensibles en celdas, artefactos,
   parámetros ni trazas.

## Guion de la hora práctica presencial (60 min)

| Minutos | Acción | Pregunta que guía la discusión |
| ---: | --- | --- |
| 0–10 | Localiza Experiments y explica run, input, artefacto y modelo. | ¿Qué se pierde si sólo compartimos el notebook? |
| 10–30 | Ejecuta los candidatos con train/valid/test separado. | ¿Por qué test no aparece en todos los runs? |
| 30–45 | Compara, aplica el gate y abre test una sola vez. | ¿Qué ocurre si nadie supera el gate? |
| 45–55 | Demuestra Registry y la API con una ejecución preparada. | ¿Registrar es desplegar o aprobar? |
| 55–60 | Presenta el trabajo autónomo y el entregable. | ¿Qué señal exigirías para rollback? |

## Bloque autónomo posterior (2–3 h)

El alumnado completa tracking, gate, test, `Challenger`, promoción, rollback,
`Champion`, API, pruebas, telemetría y apagado. AgentOps/LLMOps puede mostrarse
en la hora teórica o completarse como segundo bloque autónomo.

## Decisiones pedagógicas

- El modo determinista es intencionado: permite enseñar observabilidad y
  evaluación sin depender de coste, cuota o disponibilidad de un LLM.
- Cada alumno tiene un experimento propio. Para comparar resultados en clase,
  pide que compartan capturas de la tabla de runs o los valores de la ficha; no
  solicites acceso a sus workspaces personales.
- Una llamada real al endpoint es una demo de producto, no un requisito para
  aprobar la práctica. El alumnado debe poder reproducir el entregable sin
  consumir tokens.
- Free Edition es excelente para aprender el ciclo. Antes de producción, los
  experimentos, permisos, retención y datos de trazas deben diseñarse por
  sistema y riesgo, con gobernanza adicional.
- No presentes el servidor HTTP local como alternativa a Model Serving: sirve
  para practicar contrato, carga del pickle, health checks, errores, métricas y
  apagado sin crear infraestructura de pago.

## Referencias de configuración

- [Databricks Free Edition: capacidades y registro](https://docs.databricks.com/aws/en/getting-started/free-edition)
- [Límites de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations)
- [Tracking de modelos en Databricks](https://docs.databricks.com/aws/en/mlflow/tracking)
- [Model Registry en Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle)
- [Trazas de agentes y LLMs](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/)
