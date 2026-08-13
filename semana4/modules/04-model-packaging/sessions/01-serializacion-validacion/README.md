# Clase 1 — Serialización, formatos y validación

Resultado de aprendizaje: diferenciar el binario del modelo de los metadatos que
lo hacen interpretable y diseñar un manifiesto que permita rechazar artefactos
incompatibles antes de inferir.

La sesión parte del módulo local de la semana 3 y del payload que ya valida
feature_names y model_version. El notebook guiado crea un clasificador pequeño,
inspecciona el formato legado y construye un bundle con manifiesto.

La práctica de parejas es el lienzo del contrato:
exercises/01-model-packaging/01.01-artifact-contract/problem/readme.md:
concepto breve, inspección guiada, extensión autónoma con un manifiesto alterado
y debrief de los invariantes. No se implementa todavía el módulo completo.

## Secuencia de la sesión

1. Recordar el recorrido de la semana 3 y localizar qué decisiones no viajan
   con el joblib.
2. Comparar binario, JSON y código como lugares de almacenamiento.
3. Completar ArtifactManifest en el lienzo.
4. Guardar/cargar un bundle pequeño y provocar errores de compatibilidad.
5. Preparar el orden de implementación del taller de la clase 2.

## Preparación y ejecución

Desde la raíz:

~~~bash
uv sync
~~~

Abre el notebook con el kernel del entorno del proyecto. La ejecución no
descarga un modelo ni genera artefactos versionables: todo queda en .tmp/.
