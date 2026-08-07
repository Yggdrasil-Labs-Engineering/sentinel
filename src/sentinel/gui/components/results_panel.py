"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

results_panel.py

Purpose:
Smoke test results panel.

Displays the operational status and results of
Sentinel smoke tests.

Responsibilities:
- Display smoke test status.
- Display execution results.
- Display operational messages.

This panel is responsible only for presentation.
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

from sentinel.models.smoke_result import SmokeResult


class ResultsPanel(QFrame):
    """
    Displays smoke test results.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

    # =====================================================
    # User Interface
    # =====================================================

    def _initialize_ui(self):

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = QLabel("Results")
        header.setAlignment(Qt.AlignLeft)

        layout.addWidget(header)

        # -------------------------------------------------
        # Current Status
        # -------------------------------------------------

        self.status_label = QLabel("🟢 Ready")
        self.status_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.status_label)

        # -------------------------------------------------
        # Results Console
        # -------------------------------------------------

        self.console = QTextEdit()

        self.console.setReadOnly(True)

        self.console.setPlaceholderText(
            "Waiting for smoke test..."
        )

        layout.addWidget(self.console)

        self.setLayout(layout)

    # =====================================================
    # Public Methods
    # =====================================================

    def update_status(
        self,
        status: str,
    ):
        """
        Update the displayed status.
        """

        self.status_label.setText(status)

    def append_message(
        self,
        message: str,
    ):
        """
        Append a message to the results console.
        """

        self.console.append(message)

    def clear_results(self):
        """
        Clear all displayed results.
        """

        self.console.clear()

    def display_results(
        self,
        smoke_result: SmokeResult,
    ):
        """
        Display the results of a completed smoke test.
        """

        self.clear_results()

        overall = (
            "PASS"
            if smoke_result.overall_passed
            else "FAIL"
        )

        self.update_status(
            f"Overall Result: {overall}"
        )

        self.console.append(
            f"Passed   : {smoke_result.passed}"
        )

        self.console.append(
            f"Failed   : {smoke_result.failed}"
        )

        self.console.append(
            f"Duration : {smoke_result.duration_ms:.2f} ms"
        )

        self.console.append("")

        for result in smoke_result.checks:

            status = (
                "PASS"
                if result.passed
                else "FAIL"
            )

            self.console.append(
                f"[{status}] {result.name}"
            )

            self.console.append(
                f"    Message : {result.message}"
            )

            if result.status_code is not None:

                self.console.append(
                    f"    HTTP    : {result.status_code}"
                )

            if result.duration_ms is not None:

                self.console.append(
                    f"    Time    : {result.duration_ms:.2f} ms"
                )

            self.console.append("")