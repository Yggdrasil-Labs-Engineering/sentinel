"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

endpoint_check.py

Purpose:
Verify that an API endpoint is reachable and
responding successfully.

=========================================================
"""

import time

import requests

from sentinel.checks.base_check import BaseCheck
from sentinel.models.check_result import CheckResult


class EndpointCheck(BaseCheck):
    """
    Executes a generic API endpoint smoke test.
    """

    def __init__(
        self,
        name: str,
        endpoint: str,
        token: str | None = None,
    ):

        super().__init__(
            name,
            f"Verify endpoint: {endpoint}"
        )

        self.endpoint = endpoint
        self.token = token

    def execute(self) -> CheckResult:
        """
        Execute the endpoint check.
        """

        start = time.perf_counter()

        try:

            headers = {}

            if self.token:

                headers["Authorization"] = (
                    f"Bearer {self.token}"
                )

            response = requests.get(

                self.endpoint,

                headers=headers,

                timeout=10,

            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            if response.status_code == 200:

                return CheckResult(

                    name=self.name,

                    passed=True,

                    message="Endpoint responded successfully.",

                    status_code=response.status_code,

                    duration_ms=elapsed,

                    endpoint=self.endpoint,

                )

            return CheckResult(

                name=self.name,

                passed=False,

                message=f"Unexpected HTTP status: {response.status_code}",

                status_code=response.status_code,

                duration_ms=elapsed,

                endpoint=self.endpoint,

            )

        except Exception as ex:

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            return CheckResult(

                name=self.name,

                passed=False,

                message="Unable to reach endpoint.",

                duration_ms=elapsed,

                endpoint=self.endpoint,

                exception=str(ex),

            )