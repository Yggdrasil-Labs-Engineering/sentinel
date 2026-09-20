from sentinel.engine.smoke_engine import SmokeEngine


def test_smoke_engine_positive_demo_without_authentication(demo_api_url):
    events = []
    result = SmokeEngine(
        base_url=demo_api_url,
        endpoint_path="/users",
        progress_callback=lambda check, status: events.append((check, status)),
    ).execute()

    assert result.overall_passed is True
    assert result.passed == 2
    assert result.failed == 0
    assert [check.name for check in result.checks] == [
        "Connectivity Check",
        "Endpoint Check",
    ]
    assert ("authentication", "skipped") in events
    assert events[-1] == ("endpoint", "pass")


def test_smoke_engine_positive_demo_with_authentication(demo_api_url):
    result = SmokeEngine(
        base_url=demo_api_url,
        username="demo",
        password="sentinel",
        endpoint_path="/users",
    ).execute()

    assert result.overall_passed is True
    assert result.passed == 3
    assert result.failed == 0


def test_smoke_engine_negative_demo_bad_endpoint(demo_api_url):
    result = SmokeEngine(
        base_url=demo_api_url,
        endpoint_path="/missing",
    ).execute()

    assert result.overall_passed is False
    assert result.passed == 1
    assert result.failed == 1
    assert result.checks[-1].status_code == 404


def test_smoke_engine_negative_demo_failed_authentication(demo_api_url):
    result = SmokeEngine(
        base_url=demo_api_url,
        username="demo",
        password="wrong",
        endpoint_path="/users",
    ).execute()

    assert result.overall_passed is False
    assert result.failed == 1
    assert result.checks[-1].name == "Authentication Check"
    assert result.checks[-1].status_code == 401


def test_smoke_engine_rejects_partial_authentication_configuration(demo_api_url):
    result = SmokeEngine(
        base_url=demo_api_url,
        username="demo",
        password="",
        endpoint_path="/users",
    ).execute()

    assert result.overall_passed is False
    assert result.failed == 1
    assert "incomplete" in result.checks[-1].message.lower()


def test_smoke_engine_stops_after_connectivity_failure():
    result = SmokeEngine(
        base_url="http://127.0.0.1:1",
        endpoint_path="/users",
    ).execute()

    assert result.overall_passed is False
    assert len(result.checks) == 1
    assert result.checks[0].name == "Connectivity Check"
