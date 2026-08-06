"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

base_check.py

Purpose:
Defines the abstract base class for all Sentinel
smoke test checks.

Every check inherits from BaseCheck and implements
the execute() method.

=========================================================
"""

from abc import ABC, abstractmethod

from sentinel.models.check_result import CheckResult


class BaseCheck(ABC):
    """
    Base class for all Sentinel smoke tests.
    """

    def __init__(
            self,
            name: str, 
            description: str = "", 
    ): 
        """
        Initialize a smoke test. 

        Parameters
        ----------

        name : str
            Display name of the smoke test. 

        description : str, optional 
            Human-readable description of the smoke test.
        """

        self.name = name

        self.description = description
        
    @abstractmethod
    def execute(self) -> CheckResult:
        """
        Execute the smoke test.

        Returns
        -------
        CheckResult
            The outcome of the smoke test.
        """
        pass