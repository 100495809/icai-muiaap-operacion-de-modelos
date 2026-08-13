# Solución — Bundle serializado de calidad de vino

Esta es la referencia docente de la práctica 01.02. La solución parte de los
contratos de la semana 3 y añade:

- un ArtifactManifest validado con Pydantic;
- guardado atómico de manifest.json y model.joblib;
- carga que valida metadatos antes de deserializar;
- validación de etiqueta, confianza y versiones de la respuesta;
- CLI que no deja CSV parcial si una fila posterior es inválida;
- migración opcional del payload joblib de la semana 3.

## Validación

Desde la raíz del repositorio:

~~~bash
uv run pytest
uv run ruff check modules/04-model-packaging/solutions/01.02-serializable-inference-module
uv run ruff format --check modules/04-model-packaging/solutions/01.02-serializable-inference-module
~~~

Para migrar el artefacto de la semana 3:

~~~bash
uv run python -m model_packaging.migrate_legacy_artifact \
  --input models/wine_quality_classifier.joblib \
  --output models/wine_quality_bundle
~~~
