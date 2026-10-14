"""TODO: transformación de una muestra validada en el vector del modelo."""

from model_inference.contracts import WineQualityRequest
import numpy as np
from dataclasses import dataclass

PREPROCESSING_VERSION = "wine-red-features-v1"

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
@dataclass(frozen=True)
class WineFeatures:
    """Vector de características en el orden estable del modelo."""

    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

    def as_vector(self) -> list[float]:
        """Devuelve las once medidas en el orden acordado."""

        return [getattr(self, name) for name in FEATURE_NAMES]


def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    """Construye el vector que espera el estimador."""

    return WineFeatures(**request.model_dump())