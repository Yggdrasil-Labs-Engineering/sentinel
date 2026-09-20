"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

smoke_engine.py

Purpose:
Coordinate execution of Sentinel smoke test checks.

Responsibilities:
    - Execute smoke tests in sequence.
    - Stop execution on critical failures.
    - Collect CheckResult objects.
    - Return execution results.

The Smoke Engine does not contain API logic.
Individual checks are responsible for their own execution.
=========================================================
"""

import time
from datetime import datetime

from sentinel.checks.authentication_check import AuthenticationCheck
from sentinel.checks.connectivity_check import ConnectivityCheck
from sentinel.checks.endpoint_check import EndpointCheck
from sentinel.models.check_result import CheckResult
from sentinel.models.smoke_result import SmokeResult


class SmokeEngine:
    """Coordinates Sentinel smoke tests."""

    def __init__(
        self,
        base_url: str,
        username: str = "",
        password: str = "",
        endpoint_path: str = "/users",
        progress_callback=None,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.endpoint_path = endpoint_path.strip() or "/"
        self.progress_callback = progress_callback

    def _build_result(self, results: list[CheckResult], start: float) -> SmokeResult:
        """Build a SmokeResult from the executed checks."""
        duration_ms = (time.perf_counter() - start) * 1000
        passed = sum(result.passed for result in results)
        failed = len(results) - passed

        return SmokeResult(
            checks=results,
            passed=passed,
            failed=failed,
            duration_ms=duration_ms,
            timestamp=datetime.now(),
            overall_passed=(failed == 0),
        )

    def _report_progress(self, check_name: str, status: str) -> None:
        """Report progress without coupling the engine to the GUI."""
        if self.progress_callback is not None:
            self.progress_callback(check_name, status)

    def _target_url(self, path: str) -> str:
        """Build a URL beneath the configured base target."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def execute(self) -> SmokeResult:
        """Execute the Sentinel smoke test sequence."""
        start = time.perf_counter()
        results: list[CheckResult] = []

        # Connectivity is the gate for every later check.
        self._report_progress("connectivity", "running")
        connectivity_result = ConnectivityCheck(self.base_url).execute()
        self._report_progress(
            "connectivity", "pass" if connectivity_result.passed else "fail"
        )
        results.append(connectivity_result)

        if not connectivity_result.passed:
            return self._build_result(results, start)

        # Authentication is optional for the MVP. It runs only when
        # credentials are explicitly supplied.
        credentials_supplied = bool(self.username or self.password)

        if credentials_supplied:
            self._report_progress("authentication", "running")

            if not (self.username and self.password):
                auth_result = CheckResult(
                    name="Authentication Check",
                    passed=False,
                    message=(
                        "Authentication configuration is incomplete. "
                        "Provide both username and password, or leave both blank."
                    ),
                    endpoint=self._target_url("/login"),
                )
                self._report_progress("authentication", "fail")
                results.append(auth_result)
                return self._build_result(results, start)

            auth = AuthenticationCheck(
                self._target_url("/login"),
                self.username,
                self.password,
            )
            auth_result = auth.execute()
            self._report_progress(
                "authentication", "pass" if auth_result.passed else "fail"
            )
            results.append(auth_result)

            if not auth_result.passed:
                return self._build_result(results, start)

            token = auth.token
        else:
            self._report_progress("authentication", "skipped")
            token = None

        # Endpoint validation.
        self._report_progress("endpoint", "running")
        endpoint_result = EndpointCheck(
            name="Endpoint Check",
            endpoint=self._target_url(self.endpoint_path),
            token=token,
        ).execute()
        self._report_progress("endpoint", "pass" if endpoint_result.passed else "fail")
        results.append(endpoint_result)

        return self._build_result(results, start)
