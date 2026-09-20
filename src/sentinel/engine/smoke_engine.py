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
Individual checks are responsible for their
own execution.
=========================================================
"""

import time

from datetime import datetime

from sentinel.models.smoke_result import SmokeResult

from sentinel.checks.authentication_check import AuthenticationCheck
from sentinel.checks.endpoint_check import EndpointCheck
from sentinel.checks.connectivity_check import ConnectivityCheck


class SmokeEngine:
    """
    Coordinates Sentinel smoke tests.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        progress_callback=None,
    ):

        self.base_url = base_url.rstrip("/")

        self.username = username

        self.password = password

        # -------------------------------------------------
        # Progress Callback
        # -------------------------------------------------

        self.progress_callback = progress_callback

    def _build_result(
        self,
        results,
        start,
    ):
        """
        Build a SmokeResult from the executed checks.
        """

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

    def _report_progress(
        self,
        check_name: str,
        status: str,
    ):
        """
        Report smoke test progress to interested listeners.

        The SmokeEngine does not know who receives these updates. It simply
        repots operational progress as checks execute.
        """

        if self.progress_callback is not None:
            self.progress_callback(
                check_name,
                status,
            )

    def execute(self):
        """
        Execute the Sentinel smoke test sequence.

        Returns
        -------
        SmokeResult
            Results of the complete smoke test execution.
        """

        start = time.perf_counter()

        results = []

        # -------------------------------------------------
        # Connectivivty Check
        # -------------------------------------------------

        self._report_progress(
            "connectivity",
            "running",
        )

        connectivity = ConnectivityCheck(self.base_url)

        connectivity_result = connectivity.execute()

        if connectivity_result.passed:

            self._report_progress(
                "connectivity",
                "pass",
            )

        else:

            self._report_progress(
                "connectivity",
                "fail",
            )

        results.append(connectivity_result)

        if not connectivity_result.passed:
            return self._build_result(
                results,
                start,
            )

        # -------------------------------------------------
        # Future Enhancement
        #
        # Health Endpoint Check
        #
        # Validate application-specific health endpoints
        # (e.g. /health, /status, /actuator/health).
        # -------------------------------------------------

        # -------------------------------------------------
        # Authentication
        # -------------------------------------------------

        self._report_progress(
            "authentication",
            "running",
        )

        auth = AuthenticationCheck(
            f"{self.base_url}/login",
            self.username,
            self.password,
        )

        auth_result = auth.execute()

        if not auth_result.passed:

            self._report_progress(
                "authentication",
                "fail",
            )

            results.append(auth_result)

            if not auth_result.passed:
                return self._build_result(
                    results,
                    start,
                )

        # -------------------------------------------------
        # Endpoint Validation
        # -------------------------------------------------

        self._report_progress(
            "endpoint",
            "running",
        )

        endpoint = EndpointCheck(
            name="Users Endpoint",
            endpoint=f"{self.base_url}/users",
            token=auth.token,
        )

        endpoint_result = endpoint.execute()

        if endpoint_result.passed:

            self._report_progress(
                "endpoint",
                "pass",
            )

        else:

            self._report_progress(
                "endpoint",
                "fail",
            )

        results.append(endpoint_result)
