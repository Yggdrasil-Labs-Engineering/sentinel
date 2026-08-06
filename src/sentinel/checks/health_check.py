"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

health_check.py

Purpose:
Verify that the application's health endpoint
is reachable and responding successfully.

=========================================================
"""

import time

import requests

from sentinel.checks.base_check import BaseCheck
from sentinel.models.check_result import CheckResult


class HealthCheck(BaseCheck):
    """
    Executes a health endpoint smoke test.
    """

    def __init__(self, url: str):

        super().__init__(
            "Health Check",
            "Verify application health endpoint."
        )

        self.url = url

    def execute(self) -> CheckResult:
        """
        Execute the health check.
        """

        start = time.perf_counter()

        try:

            response = requests.get(
                self.url,
                timeout=10,
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            if response.status_code == 200:

                return CheckResult(
                    name=self.name,
                    passed=True,
                    message="Health endpoint responded successfully.",
                    status_code=response.status_code,
                    duration_ms=elapsed,
                    endpoint=self.url,
                )

            return CheckResult(
                name=self.name,
                passed=False,
                message=f"Unexpected HTTP status: {response.status_code}",
                status_code=response.status_code,
                duration_ms=elapsed,
                endpoint=self.url,
            )

        except Exception as ex:

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="Unable to reach health endpoint.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )