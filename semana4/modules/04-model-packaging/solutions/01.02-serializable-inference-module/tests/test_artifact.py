import json
from pathlib import Path

import pytest
from model_packaging.artifact import (
    ArtifactManifest,
    LoadedModelBundle,
    create_manifest,
    infer_wine_quality,
    load_model_bundle,
    save_model_bundle,
)
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES
from sklearn.dummy import DummyClassifier

WINE_SAMPLE = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "ph": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
}


def make_estimator() -> DummyClassifier:
    """Crea un estimador pequeño y determinista para las pruebas."""

    estimator = DummyClassifier(strategy="constant", constant="acceptable")
    estimator.fit([[0.0] * len(FEATURE_NAMES)], ["acceptable"])
    return estimator


def make_request() -> WineQualityRequest:
    """Devuelve una solicitud válida de la muestra de la semana 3."""

    return WineQualityRequest.model_validate(WINE_SAMPLE)


def test_save_and_load_bundle_round_trip(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    estimator = make_estimator()
    manifest = create_manifest(estimator, "wine-quality-rf-v1")

    saved_manifest = save_model_bundle(bundle_path, estimator, manifest)
    loaded = load_model_bundle(bundle_path)
    prediction = infer_wine_quality(loaded, make_request())

    assert saved_manifest == manifest
    assert sorted(path.name for path in bundle_path.iterdir()) == [
        "manifest.json",
        "model.joblib",
    ]
    assert json.loads((bundle_path / "manifest.json").read_text()) == {
        "schema_version": "wine-quality-bundle-v1",
        "model_version": "wine-quality-rf-v1",
        "preprocessing_version": "wine-red-features-v1",
        "feature_names": list(FEATURE_NAMES),
        "output_labels": ["needs_review", "acceptable", "excellent"],
        "estimator_type": "DummyClassifier",
    }
    assert prediction.quality_band == "acceptable"
    assert prediction.confidence == 1.0
    assert prediction.model_version == "wine-quality-rf-v1"


def test_inference_accepts_multiclass_probability_arrays() -> None:
    estimator = DummyClassifier(strategy="prior")
    estimator.fit(
        [[0.0] * len(FEATURE_NAMES), [1.0] * len(FEATURE_NAMES)],
        ["acceptable", "excellent"],
    )
    bundle = LoadedModelBundle(
        estimator=estimator,
        manifest=create_manifest(estimator, "wine-quality-rf-v2"),
    )

    prediction = infer_wine_quality(bundle, make_request())

    assert prediction.quality_band in {"acceptable", "excellent"}
    assert prediction.confidence == 0.5


def test_load_rejects_a_reordered_feature_contract(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    save_model_bundle(
        bundle_path,
        make_estimator(),
        create_manifest(make_estimator(), "wine-quality-rf-v1"),
    )
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["feature_names"] = list(reversed(manifest["feature_names"]))
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="manifest.json inválido"):
        load_model_bundle(bundle_path)


def test_load_rejects_unknown_manifest_fields(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    save_model_bundle(
        bundle_path,
        make_estimator(),
        create_manifest(make_estimator(), "wine-quality-rf-v1"),
    )
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["unexpected"] = "not allowed"
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="manifest.json inválido"):
        load_model_bundle(bundle_path)


class UnknownLabelEstimator:
    """Estimador falso para demostrar la validación de la salida."""

    def predict(self, features: list[list[float]]) -> list[str]:
        return ["unknown"]

    def predict_proba(self, features: list[list[float]]) -> list[list[float]]:
        return [[1.0]]


def test_inference_rejects_an_unknown_model_label() -> None:
    estimator = UnknownLabelEstimator()
    bundle = LoadedModelBundle(
        estimator=estimator,
        manifest=create_manifest(estimator, "bad-output-v1"),
    )

    with pytest.raises(ValueError, match="salida del modelo"):
        infer_wine_quality(bundle, make_request())


class NonFiniteEstimator:
    """Estimador falso que devuelve una confianza no válida."""

    def predict(self, features: list[list[float]]) -> list[str]:
        return ["acceptable"]

    def predict_proba(self, features: list[list[float]]) -> list[list[float]]:
        return [[float("nan")]]


def test_inference_rejects_a_non_finite_confidence() -> None:
    estimator = NonFiniteEstimator()
    bundle = LoadedModelBundle(
        estimator=estimator,
        manifest=ArtifactManifest(
            schema_version="wine-quality-bundle-v1",
            model_version="bad-confidence-v1",
            preprocessing_version="wine-red-features-v1",
            feature_names=FEATURE_NAMES,
            output_labels=("needs_review", "acceptable", "excellent"),
            estimator_type=type(estimator).__name__,
        ),
    )

    with pytest.raises(ValueError, match="salida del modelo"):
        infer_wine_quality(bundle, make_request())
