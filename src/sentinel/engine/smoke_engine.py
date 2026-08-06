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

from sentinel.checks.authentication_check import AuthenticationCheck
from sentinel.checks.endpoint_check import EndpointCheck
from sentinel.checks.health_check import HealthCheck


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

    def execute(self):
        """
        Execute the Sentinel smoke test sequence.

        Returns
        -------
        list
            List of CheckResult objects.
        """

        results = []

        # -------------------------------------------------
        # Health Check
        # -------------------------------------------------

        health = HealthCheck(
            f"{self.base_url}/health"
        )

        health_result = health.execute()

        results.append(
            health_result
        )

        if not health_result.passed:
            return results

        # -------------------------------------------------
        # Authentication
        # -------------------------------------------------

        auth = AuthenticationCheck(

            f"{self.base_url}/login",

            self.username,

            self.password,

        )

        auth_result = auth.execute()

        results.append(
            auth_result
        )

        if not auth_result.passed:
            return results

        # -------------------------------------------------
        # Endpoint Validation
        # -------------------------------------------------

        endpoint = EndpointCheck(

            name="Users Endpoint",

            endpoint=f"{self.base_url}/users",

            token=auth.token,

        )

        endpoint_result = endpoint.execute()

        results.append(
            endpoint_result
        )

        return results