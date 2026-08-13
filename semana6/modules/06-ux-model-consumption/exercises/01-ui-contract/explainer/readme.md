# Explicación — Contrato de experiencia para una inferencia

Una interfaz de IA tiene un contrato además del contrato de datos. Debe
explicar qué estado atraviesa la petición, qué significa la salida, qué puede
hacer la persona ante un error y qué evidencia técnica acompaña al resultado.

La práctica no modifica el modelo. Usa las decisiones de S3 y S4 como límites:

- las once features siguen siendo responsabilidad del contrato de entrada;
- `quality_band`, `confidence`, `model_version` y
  `preprocessing_version` son la salida disponible;
- el manifiesto identifica el bundle, pero no convierte una predicción en una
  garantía;
- la telemetría de la interfaz registra agregados, no valores del formulario.
