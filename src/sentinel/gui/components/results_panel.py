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
    - Display smoke test status
    - Display execution results
    - Display operational messages

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


class ResultsPanel(QFrame):
    """
    Displays smoke test results.

    Responsibilities:
        - Display execution status.
        - Display smoke test output.
        - Display operational messages.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

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

    def update_status(
        self,
        status: str
    ):
        """
        Updates the displayed status.
        """

        self.status_label.setText(status)

    def append_message(
        self,
        message: str
    ):
        """
        Appends a message to the results console.
        """

        self.console.append(message)

    def clear_results(self):
        """
        Clears all displayed results.
        """

        self.console.clear()

    def display_results(
        self,
        text: str
    ):
        """
        Replaces the current results with new output.
        """

        self.console.setPlainText(text)