"""Prepara el artefacto de clase; no forma parte del taller de la semana 3."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from model_inference.inference import artifact_payload
from model_inference.preprocess import FEATURE_NAMES

MODEL_VERSION = "wine-quality-rf-v1"

CSV_COLUMN_NAMES = {
    name: "pH" if name == "ph" else name.replace("_", " ") for name in FEATURE_NAMES
}


def quality_band(quality_score: int) -> str:
    """Agrupa la valoración sensorial para reducir una salida desbalanceada."""

    if quality_score <= 5:
        return "needs_review"
    if quality_score == 6:
        return "acceptable"
    return "excellent"


def load_training_data(csv_path: Path) -> tuple[list[list[float]], list[str]]:
    """Lee las filas de Kaggle y separa características de la etiqueta de calidad."""

    with csv_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    features = [
        [float(row[CSV_COLUMN_NAMES[name]]) for name in FEATURE_NAMES] for row in rows
    ]
    labels = [quality_band(int(row["quality"])) for row in rows]

    return features, labels


def train_and_save(csv_path: Path, output_path: Path) -> None:
    """Entrena de forma determinista y guarda el formato consumido por la API."""

    features, labels = load_training_data(csv_path)
    train_features, _, train_labels, _ = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )
    estimator = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=2,
        class_weight="balanced_subsample",
        random_state=42,
    )
    estimator.fit(train_features, train_labels)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact_payload(estimator, MODEL_VERSION), output_path)


def parse_args() -> argparse.Namespace:
    """Obtiene las rutas de datos de entrenamiento y artefacto de instructor."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    train_and_save(arguments.input, arguments.output)
