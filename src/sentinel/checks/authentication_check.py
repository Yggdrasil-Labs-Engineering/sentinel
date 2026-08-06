"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

authentication_check.py

Purpose:
Verify that Sentinel can successfully authenticate
with the target application.

=========================================================
"""

import time

import requests

from sentinel.checks.base_check import BaseCheck
from sentinel.models.check_result import CheckResult


class AuthenticationCheck(BaseCheck):
    """
    Executes an authentication smoke test.
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
    ):

        super().__init__(
            "Authentication Check",
            "Verify application authentication."
        )

        self.url = url
        self.username = username
        self.password = password

        self.token = None

    def execute(self) -> CheckResult:
        """
        Execute the authentication check.
        """

        start = time.perf_counter()

        try:

            response = requests.post(

                self.url,

                json={
                    "username": self.username,
                    "password": self.password,
                },

                timeout=10,
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            if response.status_code == 200:

                try:
                    self.token = response.json().get(
                        "token"
                    )
                except Exception:
                    self.token = None

                return CheckResult(

                    name=self.name,

                    passed=True,

                    message="Authentication successful.",

                    status_code=response.status_code,

                    duration_ms=elapsed,

                    endpoint=self.url,

                )

            return CheckResult(

                name=self.name,

                passed=False,

                message="Authentication failed.",

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

                message="Unable to authenticate.",

                duration_ms=elapsed,

                endpoint=self.url,

                exception=str(ex),

            )