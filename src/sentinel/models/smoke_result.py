"""
=========================================================

Yggdrasil Labs Engineering

OVERWATCH Sentinel

smoke_result.py

Purpose:
Represents the results of an entire Sentinel
smoke test execution.

=========================================================
"""

from dataclasses import dataclass

from datetime import datetime

from sentinel.models.check_result import CheckResult


@dataclass
class SmokeResult:
    """
    Represents the results of an entire
    Sentinel smoke test run.
    """

    checks: list[CheckResult]

    passed: int

    failed: int

    duration_ms: float

    timestamp: datetime

    overall_passed: bool