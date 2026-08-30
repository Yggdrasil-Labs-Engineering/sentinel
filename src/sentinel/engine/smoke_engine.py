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
    ):

        self.base_url = base_url.rstrip("/")

        self.username = username

        self.password = password

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

        connectivity = ConnectivityCheck(self.base_url)

        connectivity_result = connectivity.execute()

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

        auth = AuthenticationCheck(
            f"{self.base_url}/login",
            self.username,
            self.password,
        )

        auth_result = auth.execute()

        results.append(auth_result)

        if not auth_result.passed:
            return self._build_result(
                results,
                start,
            )

        # -------------------------------------------------
        # Endpoint Validation
        # -------------------------------------------------

        endpoint = EndpointCheck(
            name="Users Endpoint",
            endpoint=f"{self.base_url}/users",
            token=auth.token,
        )

        endpoint_result = endpoint.execute()

        results.append(endpoint_result)

        return self._build_result(
            results,
            start,
        )
