"""S9.4 — Tests que escribe el alumnado.

La entrega se considera completa cuando toda la suite está en verde.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from wine_api.dependencies import get_predictor
from wine_api.export_openapi import render_openapi
from wine_api.predictor import UnavailablePredictor

CONTRACT_PATH = Path(__file__).parents[1] / "contracts" / "openapi.json"


def test_prediction_returns_503_when_model_is_unavailable(
    client: TestClient, valid_payload: dict
) -> None:
    client.app.dependency_overrides[get_predictor] = UnavailablePredictor
    try:
        response = client.post("/v1/predictions", json=valid_payload)
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "model_unavailable"
    finally:
        client.app.dependency_overrides.clear()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("alcohol", 4.9),
        ("alcohol", 20.1),
        ("ph", 2.4),
        ("density", 1.02),
        ("chlorides", -0.1),
    ],
)
def test_out_of_contract_values_are_rejected(
    client: TestClient, valid_payload: dict, field: str, value: object
) -> None:
    valid_payload["features"][field] = value
    response = client.post("/v1/predictions", json=valid_payload)

    assert response.status_code == 422
    fields = [f["field"] for f in response.json()["error"]["fields"]]
    assert fields == [f"features.{field}"]


@pytest.mark.parametrize("alcohol", [5, 20])
def test_range_limits_are_inclusive(
    client: TestClient, valid_payload: dict, alcohol: int
) -> None:
    valid_payload["features"]["alcohol"] = alcohol
    response = client.post("/v1/predictions", json=valid_payload)

    assert response.status_code == 200


def test_openapi_matches_versioned_contract() -> None:
    committed = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert json.loads(render_openapi()) == committed
