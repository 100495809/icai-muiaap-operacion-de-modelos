# Guía del alumno — Práctica 01: ciclo de vida de ML con MLflow

## Qué vas a conseguir

Llevarás el dataset didáctico Wine Quality (`data/raw/WineQT.csv`) por un ciclo
de vida completo:

`datos → siete candidatos → comparación → gate → test → Registry → API → métricas de servicio`

Cada candidato contendrá inputs de datos, parámetros, métricas de validación,
matriz de confusión, reporte por clase, gobierno, modelo MLflow con firma y un
`model.joblib`. La etiqueta de trabajo será `quality_high`: vale 1 si
`quality >= 6` y 0 en otro caso. Compararás candidatos `ExtraTreesClassifier` y
`XGBClassifier` bajo el mismo contrato. Después registrarás únicamente el ganador, le asignarás el alias
`Champion` y servirás su `model.joblib` mediante una API HTTP local.

El resultado es evidencia didáctica: el umbral no es una norma comercial ni
autoriza decisiones sobre la calidad de un producto real.

## Smoke test local sin MLflow

Desde la raíz del repositorio puedes comprobar el entrenamiento sin credenciales
ni Databricks. El arnés usa el mismo split, incluye el candidato XGBoost y sólo
abre test después de elegir por validación:

```bash
uv run --no-project \
  --with pandas==2.2.3 \
  --with scikit-learn==1.9.0 \
  --with xgboost==3.0.5 \
  tools/local_wine_training.py
```

En macOS puede ser necesario disponer del runtime OpenMP que requiere XGBoost.

## Duración y organización

- Construcción guiada: 45–60 minutos.
- Trabajo autónomo: 120–180 minutos.
- Debrief y defensa: 20–30 minutos.

La parte guiada cabe en la clase de semana 01. El ciclo completo se termina
como trabajo autónomo. Conserva el mismo `BATCH_ID` durante un intento; si
reinicias desde el principio se generará otro lote.

## Antes de abrir la libreta

1. Entra en tu workspace personal de Databricks Free Edition y espera al
   compute serverless.
2. Abre la carpeta `semana1/` como Databricks Git Folder para conservar la ruta
   a `data/raw/WineQT.csv`.
3. Abre `notebooks/01_tracking_mlops.ipynb`, la versión sin resolver. Consulta
   la solución sólo después de entregar tu intento.
4. Si subiste la libreta manualmente, sube también el CSV y cambia
   `DATASET_PATH`. Nunca uses información real de pacientes.

## Fase 1 — Datos y diseño experimental

1. Ejecuta `%pip`. Si Databricks reinicia Python, sigue desde los imports.
2. Usa un alias anónimo de 3–24 caracteres; no uses correo, nombre o matrícula.
3. Valida columnas, target, filas, duplicados y nulos. Los nulos se aceptan
   porque el pipeline los imputa; una columna obligatoria ausente no.
4. Divide de forma estratificada: 60 % train, 20 % validación y 20 % test.
   **No leas test** antes de elegir el ganador.
5. Construye un `Pipeline` que incluya imputación y el estimador de cada
   candidato (`ExtraTreesClassifier` o `XGBClassifier`). El mismo objeto debe
   llegar al serving.
6. Define al menos siete configuraciones, incluyendo la configuración
   `ExtraTrees(300, max_depth=None, min_samples_leaf=1, max_features=1.0)` y al
   menos un XGBoost. Mantén constantes el dataset, split, métricas y semilla
   para que la comparación tenga sentido.

## Fase 2 — Tracking y artefactos

Para cada candidato comprueba que el run incluye:

- tags `student.alias`, `batch.id`, `lifecycle.phase`, `use_case` y riesgo;
- hiperparámetros, semillas, tamaños de split y versiones de librerías;
- inputs de train/validación mediante `mlflow.log_input()`;
- accuracy, precision, recall, F1 macro, tiempo de fit, latencia por fila y
  tamaño de `model.joblib`;
- tarjeta de datos, calidad, riesgos, reporte por clase y matriz de confusión;
- modelo MLflow con firma e `input_example`;
- `deployment/model.joblib` y `deployment/inference_contract.json`.

El registro es manual para entender qué evidencia es responsabilidad del
equipo. En sesiones posteriores podrás compararlo con `autolog`.

## Fase 3 — Elección y test

1. Recupera sólo runs de tu alias, lote y fase con `mlflow.search_runs()`.
2. Aplica la regla acordada antes de ver resultados: `validation.f1_macro >=
   0,70`; después F1 macro descendente, accuracy descendente y latencia
   ascendente.
3. Si nadie supera el gate, detente. Rebajar el umbral después de observar los
   resultados convierte el gate en decoración.
4. Guarda el `model_info.model_uri` de cada candidato como tag, carga el ganador
   desde su URI `models:/<model_id>`, evalúa test una vez y añade `test.*`,
   `selection.status=winner` y la decisión como artefacto.

## Fase 4 — Registry

1. Configura `databricks-uc` y descubre catálogo/esquema activos con Spark.
2. Registra el modelo con nombre `<catalog>.<schema>.wine_quality_classifier_<alias>`.
3. Registra una referencia de rollback y el ganador como segunda versión;
   añade descripciones y tags de uso/validación.
4. Asigna `Challenger` al ganador, haz un smoke test, promociónalo a
   `Champion`, practica rollback y re-promociona el ganador. Verifica cada alias.
5. Carga `models:/<nombre>@Champion` sin conocer el número de versión.

Registrar crea una versión gobernada; no publica una API. Si aparece
`PERMISSION_DENIED`, abre **Catalog Explorer**, confirma el catálogo y esquema
activos y que puedes crear modelos. En un workspace personal suele ser
`main.default`. No pegues credenciales ni abras una cuenta de pago.

## Fase 5 — API local y observabilidad

1. Resuelve el run de `Champion` y descarga `deployment/model.joblib` con MLflow.
2. Levanta `ThreadingHTTPServer` en `127.0.0.1` y puerto automático. Expón
   `GET /health` y `POST /predict`.
3. El contrato es `{"instances": [{...}]}` con todas y sólo las features
   esperadas. Devuelve clases, probabilidades y versión.
4. Verifica health 200, predicción 200, petición incompleta 400 y JSON de nivel
   superior incorrecto 400. Los contadores deben medir peticiones reales.
5. Registra un run `deployment-test` con contadores, latencias, versión, run
   origen y evidencia. No registres el payload de entrada.
6. Apaga el servidor para liberar recursos.

La URL local sólo existe dentro del driver durante la sesión. No tiene
autenticación, SLA, escalado ni acceso externo: es una simulación gratuita del
límite entre artefacto y servicio, no un endpoint de producción.

## Cómo comprobar tu trabajo

En **Experiments** y **Catalog Explorer** debes ver:

- al menos siete candidatos en el mismo lote;
- test únicamente en el ganador;
- dos versiones, `Challenger`, promoción, rollback y `Champion` final;
- un run de despliegue con una petición rechazada de forma controlada;
- ningún token, dato personal, payload sensible ni afirmación de uso clínico.

## Problemas habituales

| Situación | Qué hacer |
| --- | --- |
| `FileNotFoundError` al leer el CSV | Abre un Git Folder o actualiza `DATASET_PATH` al CSV subido. |
| Aparecen runs anteriores | Filtra por el `batch.id` impreso al inicio; no borres evidencia para ocultar resultados. |
| `PERMISSION_DENIED` en Registry | Comprueba catálogo/esquema y permiso `CREATE MODEL`; usa tu espacio personal, normalmente `main.default`. |
| El modelo ya existe | Registrar de nuevo crea una versión. No ejecutes la celda varias veces mientras procesa. |
| La API no responde | Inicia antes el hilo y usa el `API_PORT` automático desde el mismo notebook. |
| El puerto sigue vivo tras un error | Ejecuta `shutdown()` y `server_close()` si existen las variables, o reinicia Python. |
| No hay compute | Free Edition tiene cuotas. Conserva el notebook y espera; no crees recursos de pago. |

## Qué entregar

Completa [`s01_project_record.yaml`](../../examples/s01_project_record.yaml) con
experimento, lote, candidatos, gate, ganador, métricas finales,
modelo/versión/alias, run de deployment, pruebas de API y riesgos. Incluye una
captura de comparación y otra del modelo en Catalog Explorer.

La evaluación premia la trazabilidad y la defensa de la decisión. Un F1 alto no
compensa haber usado test para seleccionar, omitir el contrato o dejar el
servidor sin apagar.
