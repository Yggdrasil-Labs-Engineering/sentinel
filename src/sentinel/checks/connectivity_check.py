"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

connectivity_check.py

Purpose:
Verify that the application's health endpoint
is reachable and responding successfully.

=========================================================
"""

import time

import requests

from sentinel.checks.base_check import BaseCheck
from sentinel.models.check_result import CheckResult
from requests.exceptions import (
    ConnectionError,
    Timeout,
    SSLError,
    InvalidURL,
    RequestException,
)


class ConnectivityCheck(BaseCheck):
    """
    Executes a health endpoint smoke test.
    """

    def __init__(self, url: str):

        super().__init__(
            "Connectivity Check", "Verify connectivity to the target application."
        )

        self.url = url

    def _classify_http_status(
        self,
        status_code: int,
    ) -> tuple[bool, str]:
        """
        Classify an HTTP response status.

        Returns

        ------
        tuple
            (passed, message)
        """

        if 200 <= status_code < 300:

            return (
                True,
                "HTTP 200 OK\n\n" "Observation:\n" "The target responded successfully.",
            )

        if 300 <= status_code < 400:

            return (
                False,
                f"HTTP {status_code} Redirect\n\n"
                "Observation:\n"
                "The target redirected the request.",
            )

        if status_code == 401:

            return (
                False,
                "HTTP 401 Unauthorized\n\n"
                "Observation:\n"
                "Authentication is required to access this resource.",
            )

        if status_code == 403:

            return (
                False,
                "HTTP 403 Forbidden\n\n"
                "Observation:\n"
                "The server understood the request but denied access.",
            )

        if status_code == 404:

            return (
                False,
                "HTTP 404 Not Found\n\n"
                "Observation:\n"
                "The requested resource could not be found.",
            )

        if 400 <= status_code < 500:

            return (
                False,
                f"HTTP {status_code} Client Error\n\n"
                "Observation:\n"
                "The server rejected the request.",
            )

        if 500 <= status_code < 600:

            return (
                False,
                f"HTTP {status_code} Server Error\n\n"
                "Observation:\n"
                "The server encountered an internal error.",
            )

        return (
            False,
            f"HTTP {status_code}\n\n"
            "Observation:\n"
            "Unexpected HTTP response received.",
        )

    def execute(self) -> CheckResult:
        """
        Execute the connectivity check.
        """

        start = time.perf_counter()

        try:

            response = requests.get(
                self.url,
                timeout=10,
            )

            elapsed = (time.perf_counter() - start) * 1000

            passed, message = self._classify_http_status(response.status_code)

            return CheckResult(
                name=self.name,
                passed=passed,
                message=message,
                status_code=response.status_code,
                duration_ms=elapsed,
                endpoint=self.url,
            )

        except ConnectionError as ex:

            elapsed = (time.perf_counter() - start) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="Unable to connect to the target. Connection was refused.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )

        except Timeout as ex:

            elapsed = (time.perf_counter() - start) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="Connection timed out while waiting for a response from  the target.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )
        except SSLError as ex:

            elapsed = (time.perf_counter() - start) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="TLS/SSL negotiation failed.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )
        except InvalidURL as ex:

            elapsed = (time.perf_counter() - start) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="The target URL is invalid.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )

        except RequestException as ex:

            elapsed = (time.perf_counter() - start) * 1000

            return CheckResult(
                name=self.name,
                passed=False,
                message="Unable to communicate with the target application.",
                duration_ms=elapsed,
                endpoint=self.url,
                exception=str(ex),
            )
