"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field, field_validator

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)
from model_packaging.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    preprocess_wine_request,
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""


class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        """Valida que la versión del esquema sea la esperada."""
        if value != ARTIFACT_SCHEMA_VERSION:
            raise ValueError(
                f"Versión de esquema inválida. Se esperaba {ARTIFACT_SCHEMA_VERSION}."
            )
        return value

    @field_validator("preprocessing_version")
    @classmethod
    def validate_preprocessing_version(cls, value: str) -> str:
        """Valida que la versión de preprocesamiento sea la esperada."""
        if value != PREPROCESSING_VERSION:
            raise ValueError(
                "preprocessing_version incompatible: "
                f"se esperaba {PREPROCESSING_VERSION}"
            )
        return value

    @field_validator("feature_names")
    @classmethod
    def validate_feature_names(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Comprueba los nombres de características del contrato."""
        if tuple(value) != FEATURE_NAMES:
            raise ValueError("feature_names no coincide con el orden del contrato.")
        return value

    @field_validator("output_labels")
    @classmethod
    def validate_output_labels(
        cls, value: tuple[QualityBand, ...]
    ) -> tuple[QualityBand, ...]:
        """Comprueba que las etiquetas de salida coincidan con el contrato."""
        if tuple(value) != OUTPUT_LABELS:
            raise ValueError("output_labels no coincide con las categorías válidas.")
        return value

    @field_validator("model_version")
    @classmethod
    def validate_model_version(cls, value: str) -> str:
        """Comprueba que la versión del modelo no esté vacía."""
        if not value.strip():
            raise ValueError("model_version no puede estar vacío.")
        return value


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest



def _validate_estimator(estimator: object) -> None:
    """Comprueba que el estimador tenga la interfaz necesaria."""

    if not callable(getattr(estimator, "predict", None)):
        raise ValueError("El estimador debe tener un método predict().")

    if not callable(getattr(estimator, "predict_proba", None)):
        raise ValueError("El estimador debe tener un método predict_proba().")


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""
    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version=PREPROCESSING_VERSION,
        feature_names=FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__,
    )


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """Escribe el manifiesto y el estimador serializado en un bundle."""
    
    _validate_estimator(estimator)

    if manifest is not None:
        validated_manifest = ArtifactManifest.model_validate(manifest.model_dump())
    else:
        validated_manifest = create_manifest(estimator, model_version="unknown")

    bundle_path.mkdir(parents=True, exist_ok=True)
    manifest_path = bundle_path / MANIFEST_FILENAME
    if manifest_path.exists():
        raise FileExistsError(
            f"El manifiesto {manifest_path} ya existe. El bundle no se sobrescribirá."
        )
    manifest_path.write_text(
        json.dumps(validated_manifest.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
    joblib.dump(estimator, bundle_path / MODEL_FILENAME)
    return validated_manifest


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """Carga un bundle después de validar primero sus metadatos."""

    manifest_path = bundle_path / MANIFEST_FILENAME
    if not manifest_path.exists():
        raise FileNotFoundError(f"No se encontró el manifiesto en {manifest_path}.")

    model_path = bundle_path / MODEL_FILENAME

    if not model_path.exists():
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}.")
    
    try:
        manifest = ArtifactManifest.model_validate_json(
            manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"manifest.json inválido: {error}") from error

    estimator = joblib.load(bundle_path / MODEL_FILENAME)
    _validate_estimator(estimator)
    return LoadedModelBundle(estimator=estimator, manifest=manifest)


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """Preprocesa, ejecuta el estimador y devuelve la predicción."""

    features = preprocess_wine_request(request).as_vector()
    labels = bundle.estimator.predict([features])

    if len(labels) != 1:
        raise ValueError("El estimador debe devolver exactamente una etiqueta.")

    quality_band = str(labels[0])
    if quality_band not in bundle.manifest.output_labels:
        raise ValueError(f"Etiqueta de salida desconocida: {quality_band}.")

    probabilities = bundle.estimator.predict_proba([features])
    if len(probabilities) != 1 or len(probabilities[0]) == 0:
        raise ValueError("El estimador debe devolver probabilidades válidas.")

    confidence = float(max(probabilities[0]))

    return WineQualityPrediction(
        quality_band=quality_band,
        confidence=confidence,
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version,
    )
