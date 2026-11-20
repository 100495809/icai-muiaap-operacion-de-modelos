from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Body

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import (
    VALID_FEATURES_EXAMPLE,
    ErrorResponse,
    Prediction,
    PredictionRequest,
    PredictionResponse,
)

PREDICTION_EXAMPLES = {
    "valid": {
        "summary": "Vino válido",
        "description": "Cuerpo con las 11 variables dentro de rango.",
        "value": {"features": VALID_FEATURES_EXAMPLE},
    },
    "out_of_range": {
        "summary": "Fuera de rango: 422",
        "description": "El alcohol supera el límite máximo de 20.",
        "value": {"features": {**VALID_FEATURES_EXAMPLE, "alcohol": 25.0}},
    },
    "missing_field": {
        "summary": "Campo faltante: 422",
        "description": "Falta la acidez fija requerida.",
        "value": {
            "features": {
                k: v for k, v in VALID_FEATURES_EXAMPLE.items() if k != "fixed_acidity"
            }
        },
    },
}

# TODO S9.3a: mueve aquí `prefix="/v1/predictions"` y `tags=["predictions"]`.
# TODO S9.3c: declara a nivel de router `responses=` para 400, 422 y 503 con
# `{"model": ErrorResponse, "description": ...}`. Así el 422 deja de
# documentarse como `HTTPValidationError`, que ya no es lo que devolvemos.
router = APIRouter(
    prefix="/v1/predictions",
    tags=["predictions"],
    responses={
        400: {"model": ErrorResponse, "description": "El cuerpo no es JSON válido."},
        422: {
            "model": ErrorResponse,
            "description": "JSON válido que incumple campos, tipos o rangos.",
        },
        503: {"model": ErrorResponse, "description": "El modelo no está cargado."},
    },
)


@router.post(
    "",
    summary="Predecir la banda de calidad de un vino",
    response_description="Predicción con banda de calidad, confianza y metadatos.",
)
def create_prediction(
    payload: Annotated[PredictionRequest, Body(openapi_examples=PREDICTION_EXAMPLES)],
    predictor: PredictorDep,
    request_id: RequestIdDep,
) -> PredictionResponse:
    # TODO S9.3e: añade summary, response_description y un docstring útil para
    # quien consume la API (campos, rangos, decimales de confidence).
    # TODO S9.3f: ofrece en Swagger al menos tres ejemplos de cuerpo (uno válido
    # y dos inválidos). Investiga `Annotated[PredictionRequest, Body(...)]` con
    # `openapi_examples=`; usa VALID_FEATURES_EXAMPLE como base.
    """Estima la banda de calidad a partir de once variables fisicoquímicas.

    - Requiere todos los campos numéricos dentro de sus rangos válidos.
    - La confianza estimada se devuelve redondeada a dos decimales.
    - Guarda el `request_id` si necesitas reportar alguna incidencia.
    """
    output = predictor.predict(payload.features)

    # TODO S9.1e: este dict expone `raw_score` y la confianza sin redondear.
    # Declara `-> PredictionResponse` y construye el modelo; para pasar de la
    # dataclass ModelOutput a Prediction investiga `from_attributes=True`.
    return PredictionResponse(
        prediction=Prediction.model_validate(output, from_attributes=True),
        request_id=request_id,
        served_at=datetime.now(UTC),
    )
