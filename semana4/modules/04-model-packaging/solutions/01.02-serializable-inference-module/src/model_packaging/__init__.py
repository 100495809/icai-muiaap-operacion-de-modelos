"""Bundle serializado para inferencia local de calidad de vino."""

from model_packaging.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    DEFAULT_BUNDLE_PATH,
    ArtifactManifest,
    LoadedModelBundle,
    create_manifest,
    infer_wine_quality,
    load_model_bundle,
    save_model_bundle,
)
from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

__all__ = [
    "ARTIFACT_SCHEMA_VERSION",
    "DEFAULT_BUNDLE_PATH",
    "ArtifactManifest",
    "LoadedModelBundle",
    "QualityBand",
    "WineQualityPrediction",
    "WineQualityRequest",
    "create_manifest",
    "infer_wine_quality",
    "load_model_bundle",
    "save_model_bundle",
]
