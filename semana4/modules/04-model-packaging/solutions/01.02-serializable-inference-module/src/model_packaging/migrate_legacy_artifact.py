"""Migra el payload de la semana 3 a un bundle con manifiesto."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping
from pathlib import Path

import joblib

from model_packaging.artifact import create_manifest, save_model_bundle
from model_packaging.preprocess import FEATURE_NAMES


def migrate_legacy_artifact(input_path: Path, output_path: Path) -> None:
    """Convierte estimator, feature_names y model_version al nuevo formato."""

    if not input_path.is_file():
        raise FileNotFoundError(f"No se encontró el artefacto legado: {input_path}")

    payload = joblib.load(input_path)
    if not isinstance(payload, Mapping):
        raise ValueError("El artefacto legado debe ser un mapa.")
    if tuple(payload.get("feature_names", [])) != FEATURE_NAMES:
        raise ValueError("El artefacto legado no coincide con FEATURE_NAMES.")

    model_version = payload.get("model_version")
    if not isinstance(model_version, str):
        raise ValueError("El artefacto legado no declara model_version.")

    estimator = payload.get("estimator")
    manifest = create_manifest(estimator, model_version=model_version)
    save_model_bundle(output_path, estimator, manifest)


def parse_args() -> argparse.Namespace:
    """Declara las rutas de entrada y salida de la migración."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    """Ejecuta la migración con errores legibles para el docente."""

    arguments = parse_args()
    try:
        migrate_legacy_artifact(arguments.input, arguments.output)
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"Bundle escrito en: {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
