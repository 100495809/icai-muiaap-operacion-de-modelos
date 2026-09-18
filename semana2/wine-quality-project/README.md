Wine Quality Project - Operación de Modelos

Proyecto de Machine Learning modularizado y gestionado con uv para la predicción de la calidad del vino a partir de un entorno reproducible, testeado y verificado.

Estructura del Proyecto

Plaintext
wine-quality-project/
├── data/
│   └── raw/
│       └── WineQT.csv        # Dataset de partida de calidad del vino
├── src/
│   └── wine_quality/
│       ├── __init__.py
│       └── train.py          # Código principal de entrenamiento adaptado como módulo
├── tests/
│   └── test_train.py         # Tests unitarios con Pytest
├── pyproject.toml            # Configuración de dependencias y metadatos del proyecto
└── README.md                 # Documentación de la práctica
