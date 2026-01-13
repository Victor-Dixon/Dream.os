import pytest


@pytest.mark.unit
def test_build_api_url_preserves_api_base_when_endpoint_has_leading_slash():
    from tools.verify_deployment_integration import DeploymentVerifier

    url = DeploymentVerifier._build_api_url(
        "https://tradingrobotplug.com",
        "/wp-json/tradingrobotplug/v1",
        "/stock-data",
    )
    assert url == "https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/stock-data"



