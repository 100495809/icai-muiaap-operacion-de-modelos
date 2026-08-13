import pytest
from model_ui.contracts import PredictionPayload
from model_ui.errors import InputContractError
from model_ui.gateway import FEATURE_NAMES, DemoGateway

SAMPLE = {name: 1.0 for name in FEATURE_NAMES}


def test_demo_gateway_returns_the_s5_payload() -> None:
    prediction = DemoGateway().predict(SAMPLE)
    assert isinstance(prediction, PredictionPayload)
    assert prediction.model_version == "demo-ui-v1"
    assert prediction.preprocessing_version == "wine-red-features-v1"


@pytest.mark.parametrize("missing", ["fixed_acidity", "alcohol"])
def test_demo_gateway_rejects_a_missing_feature(missing: str) -> None:
    values = {name: 1.0 for name in FEATURE_NAMES if name != missing}
    with pytest.raises(InputContractError, match="faltan"):
        DemoGateway().predict(values)


def test_demo_gateway_rejects_an_unknown_feature() -> None:
    values = {**SAMPLE, "unexpected": 1.0}
    with pytest.raises(InputContractError, match="no permitidos"):
        DemoGateway().predict(values)
