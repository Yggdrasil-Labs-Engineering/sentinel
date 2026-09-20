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
- Preserve session run history.
- Allow displayed results to be cleared.
- Display operational messages.

This panel is responsible only for presentation.
=========================================================
"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from sentinel.models.smoke_result import SmokeResult


class ResultsPanel(QFrame):
    """
    Displays smoke test results and session history.
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

        header_layout = QHBoxLayout()

        header = QLabel("Results")
        header.setAlignment(Qt.AlignLeft)

        self.clear_button = QPushButton("Clear Results")
        self.clear_button.clicked.connect(self.clear_results)

        header_layout.addWidget(header)

        header_layout.addStretch()

        header_layout.addWidget(self.clear_button)

        layout.addLayout(header_layout)

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

        self.console.setPlaceholderText("Waiting for smoke test...")

        self.console.setLineWrapMode(QTextEdit.WidgetWidth)

        self.console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.console.setMinimumHeight(280)

        layout.addWidget(
            self.console,
            stretch=1,
        )

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

        self._scroll_to_latest()

    def start_run(self):
        """
        Begin a new timestamped smoke-test run.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        if self.console.toPlainText().strip():

            self.console.append("")

        self.console.append("────────────────────────────────────────")

        self.console.append(f"Run Executed: {timestamp}")

        self.console.append("────────────────────────────────────────")

        self.console.append("")

        self._scroll_to_latest()

    def clear_results(self):
        """
        Clear displayed session history.
        """

        self.console.clear()

        self.update_status("🟢 Ready")

    def display_results(
        self,
        smoke_result: SmokeResult,
    ):
        """
        Append completed smoke-test results.

        Existing session history is preserved.
        """

        overall = "🟢 PASS" if smoke_result.overall_passed else "🔴 FAIL"

        self.update_status(overall)

        self._display_header()

        self._display_summary(
            smoke_result,
            overall,
        )

        self._display_checks(
            smoke_result,
        )

        self._display_footer()

        self._scroll_to_latest()

    # =====================================================
    # Private Methods
    # =====================================================

    def _display_header(self):
        """
        Display the report header.
        """

        self.console.append("OVERWATCH Sentinel Smoke Test Report")

        self.console.append("")

    def _display_summary(
        self,
        smoke_result: SmokeResult,
        overall: str,
    ):
        """
        Display the smoke-test summary.
        """

        self.console.append(f"Overall Result : {overall}")

        self.console.append(f"Checks Passed  : {smoke_result.passed}")

        self.console.append(f"Checks Failed  : {smoke_result.failed}")

        self.console.append(f"Execution Time : " f"{smoke_result.duration_ms:.2f} ms")

        self.console.append("")

        self.console.append("Execution Results")

        self.console.append("")

    def _display_checks(
        self,
        smoke_result: SmokeResult,
    ):
        """
        Display all executed checks.
        """

        for result in smoke_result.checks:

            self._display_check(result)

    def _display_check(
        self,
        result,
    ):
        """
        Display an individual check.
        """

        status = "🟢 PASS" if result.passed else "🔴 FAIL"

        self.console.append(f"[{status}] {result.name}")

        self.console.append(f"Message: {result.message}")

        if result.status_code is not None:

            self.console.append(f"HTTP Status: " f"{result.status_code}")

        if result.duration_ms is not None:

            self.console.append(f"Response Time: " f"{result.duration_ms:.2f} ms")

        self.console.append("")

    def _display_footer(self):
        """
        Display the report footer.
        """

        self.console.append("Report Generated Successfully")

    def _scroll_to_latest(self):
        """
        Scroll the console to the newest output.
        """

        scrollbar = self.console.verticalScrollBar()

        scrollbar.setValue(scrollbar.maximum())
