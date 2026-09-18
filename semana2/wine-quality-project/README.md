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



Ejecución y Verificación
Una vez instalado el entorno, puedes ejecutar las siguientes comprobaciones:

1. Ejecutar el entrenamiento como módulo
Lanza el entrenamiento de manera controlada utilizando el entorno bloqueado:


uv run --frozen python -m wine_quality.train

2. Ejecutar los tests unitarios
Comprueba que todo el código pasa las pruebas con Pytest:


uv run --frozen pytest

3. Verificar el linter (Ruff)
Comprueba que el código cumple con los estándares de calidad y estilo:


uv run --frozen ruff check 

Si recibes el mensaje de "All checks  passed!", está todo bien.