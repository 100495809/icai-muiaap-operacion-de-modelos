# Solución orientativa — Contrato del artefacto

Una respuesta válida separa el binario del estimador de los metadatos que una
persona y un cargador pueden revisar:

~~~text
model.joblib  -> {"estimator": ...}
manifest.json -> schema_version, versiones, feature_names,
                 output_labels y estimator_type
~~~

Invariantes mínimas:

1. feature_names coincide exactamente con el orden de FEATURE_NAMES de la
   semana 3.
2. preprocessing_version coincide con el preprocesado que construye el vector.
3. El estimador expone predict y predict_proba, y sus respuestas cumplen el
   contrato de salida.

Una columna desconocida, una versión incompatible o una etiqueta no permitida
deben fallar antes de generar el CSV de salida. Las predicciones se acumulan en
memoria y se escribe el fichero solo cuando todas las filas son válidas.
