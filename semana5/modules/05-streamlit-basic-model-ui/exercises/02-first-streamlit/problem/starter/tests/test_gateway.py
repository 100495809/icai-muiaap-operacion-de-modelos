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


@pytest.mark.parametrize(
    "change",
    [
        {"unexpected": 1.0},
        {"fixed_acidity": None},
    ],
)
def test_demo_gateway_rejects_a_wrong_shape(change: dict[str, object]) -> None:
    values = dict(SAMPLE)
    if "unexpected" in change:
        values.update(change)
    else:
        values.pop("fixed_acidity")
    with pytest.raises(InputContractError):
        DemoGateway().predict(values)
