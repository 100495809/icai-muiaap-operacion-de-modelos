# Operación de Modelos — MUIAAp

Material reproducible para las clases de Operación de Modelos del Máster
Universitario en Inteligencia Artificial Aplicada. Las prácticas usan `uv`,
Pydantic y pruebas automatizadas para avanzar de un experimento a un módulo de
inferencia reutilizable.

La semana 3 está en
[`modules/03-inference-contracts/`](modules/03-inference-contracts/): trabaja
con un modelo de calidad de vino ya entrenado, datos de inferencia de Kaggle y
una práctica de extensión en parejas.

## Desarrollo

```bash
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```
