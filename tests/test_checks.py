from sentinel.checks.authentication_check import AuthenticationCheck
from sentinel.checks.connectivity_check import ConnectivityCheck
from sentinel.checks.endpoint_check import EndpointCheck


def test_connectivity_check_passes_for_reachable_target(demo_api_url):
    result = ConnectivityCheck(demo_api_url).execute()

    assert result.passed is True
    assert result.status_code == 200
    assert result.endpoint == demo_api_url


def test_connectivity_check_fails_for_invalid_url():
    result = ConnectivityCheck("not-a-valid-url").execute()

    assert result.passed is False
    assert result.exception is not None


def test_endpoint_check_reports_missing_endpoint(demo_api_url):
    result = EndpointCheck(
        name="Missing Endpoint",
        endpoint=f"{demo_api_url}/missing",
    ).execute()

    assert result.passed is False
    assert result.status_code == 404
    assert "404" in result.message


def test_authentication_check_passes_with_valid_credentials(demo_api_url):
    check = AuthenticationCheck(
        f"{demo_api_url}/login",
        "demo",
        "sentinel",
    )

    result = check.execute()

    assert result.passed is True
    assert result.status_code == 200
    assert check.token == "demo-token"


def test_authentication_check_fails_with_bad_credentials(demo_api_url):
    check = AuthenticationCheck(
        f"{demo_api_url}/login",
        "demo",
        "wrong",
    )

    result = check.execute()

    assert result.passed is False
    assert result.status_code == 401
