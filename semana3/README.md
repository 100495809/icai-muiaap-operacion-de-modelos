# Operación de Modelos — MUIAAp

Material reproducible para las clases de Operación de Modelos del Máster
Universitario en Inteligencia Artificial Aplicada. Las prácticas usan `uv`,
Pydantic y pruebas automatizadas para avanzar de un experimento a un módulo de
inferencia reutilizable.

La semana 3 está en
[`modules/03-inference-contracts/`](modules/03-inference-contracts/): trabaja
con un modelo de calidad de vino ya entrenado, datos de inferencia de Kaggle y
dos prácticas en parejas.

El alumnado recibe los proyectos de `exercises/**/problem/starter/`. Las
implementaciones completas sólo se consultan en `solutions/` tras el taller.

## Clase 1 — Inferencia, contratos y preprocesado

Se diferencia entrenamiento, artefacto e inferencia; se diseña el contrato de
entrada y salida; y se fija el orden reproducible de las once características.
La práctica es guiada y no implementa todavía el módulo de producción.

[Material y práctica de la clase 1](modules/03-inference-contracts/sessions/01-inferencia-contratos/README.md)

## Clase 2 — Taller de módulo local de inferencia

Se implementa sobre el `starter` un módulo local con `uv`: contratos Pydantic,
preprocesado, carga segura del `.joblib`, inferencia y CLI CSV. Se prueban los
casos válidos y los errores sin dejar salidas parciales.

[Material y práctica de la clase 2](modules/03-inference-contracts/sessions/02-modulo-inferencia-local/README.md)

## Entregables

- [Guion de prácticas de la clase 1](modules/03-inference-contracts/guides/class-1-practices.md): lienzo de contrato y preprocesado.
- [Guion del taller de la clase 2](modules/03-inference-contracts/guides/class-2-workshop.md): módulo local, CLI y tests.
- [Proyecto starter](modules/03-inference-contracts/exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter/): implementación del alumnado.

## Desarrollo

```bash
uv sync
uv run pytest
uv run ruff check modules/03-inference-contracts/solutions
uv run ruff format --check modules/03-inference-contracts/solutions
```
