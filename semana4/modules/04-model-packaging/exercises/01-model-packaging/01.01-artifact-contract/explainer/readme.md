# Explainer — Qué debe viajar con un modelo

Un archivo joblib puede contener un estimador, pero no explica por sí solo qué
representación espera, qué versión de preprocesado se aplicó ni qué etiquetas
son válidas para el consumidor.

En esta práctica, el manifiesto funciona como un contrato legible:

| Campo | Pregunta que responde |
| --- | --- |
| schema_version | ¿Qué forma tiene este manifiesto? |
| model_version | ¿Qué versión del estimador se está ejecutando? |
| preprocessing_version | ¿Qué transformación debe coincidir con la inferencia? |
| feature_names | ¿Qué columnas y qué orden consume el modelo? |
| output_labels | ¿Qué categorías puede devolver la interfaz? |
| estimator_type | ¿Qué clase de estimador se ha empaquetado? |

La comprobación no convierte un binario no confiable en seguro: la carga de un
objeto serializado debe limitarse a artefactos obtenidos de una fuente de
confianza.
