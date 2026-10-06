# Wine Quality Project

Proyecto de Machine Learning modularizado y gestionado con `uv` para la predicción de la calidad del vino dentro de un entorno reproducible, testeado y verificable.

## Descripción

Este repositorio implementa un flujo básico de entrenamiento y validación para un modelo de regresión sobre el conjunto de datos `WineQT`, con una estructura orientada a la práctica de operación de modelos.

## Estructura del proyecto

```text
wine-quality-project/
├── data/
│   └── raw/
│       └── WineQT.csv            # Dataset de entrada para la calidad del vino
├── src/
│   └── wine_quality/
│       ├── __init__.py
│       └── train.py              # Código principal de entrenamiento adaptado como módulo
├── tests/
│   └── test_train.py             # Tests unitarios con Pytest
├── pyproject.toml                # Dependencias, metadata y configuración del proyecto
├── README.md                     # Documentación del proyecto
└── .venv/                        # Entorno virtual del proyecto (si se crea localmente)
```

## Requisitos

- Python 3.11+
- `uv` instalado
- Dependencias definidas en `pyproject.toml`

## Configuración inicial

```bash
uv sync
uv run pytest
```

## Objetivos del proyecto

- Reproducibilidad del entorno y del experimento.
- Organización del código en módulos reutilizables.
- Validación automática mediante tests.
- Estructura clara para escalar hacia inferencia, API o despliegue.
