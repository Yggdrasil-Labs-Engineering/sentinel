"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

check_result.py

Purpose:
Represents the result of a single smoke test check.

Each check performed by Sentinel returns a CheckResult
object that describes the outcome of the operation.

=========================================================
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckResult:
    """
    Represents the outcome of a single smoke test check.
    """

    name: str
    passed: bool
    message: str

    status_code: Optional[int] = None

    duration_ms: Optional[float] = None

    endpoint: Optional[str] = None

    exception: Optional[str] = None