"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

configuration_panel.py

Purpose:
Configuration input panel.

Collects the information required to execute a
Sentinel smoke test.

Responsibilities:
    - Collect target URL
    - Collect authentication credentials
    - Provide smoke test execution button

This panel does not execute smoke tests.
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class ConfigurationPanel(QFrame):
    """
    Configuration input panel.

    Responsibilities:
        - Collect user input.
        - Expose configuration values.
        - Provide Run Smoke Test button.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

    def _initialize_ui(self):

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()

        form = QFormLayout()

        # -------------------------------------------------
        # Target URL
        # -------------------------------------------------

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "http://localhost:8888"
        )

        form.addRow(
            "Target URL:",
            self.url_input
        )

        # -------------------------------------------------
        # Username
        # -------------------------------------------------

        self.username_input = QLineEdit()

        form.addRow(
            "Username:",
            self.username_input
        )

        # -------------------------------------------------
        # Password
        # -------------------------------------------------

        self.password_input = QLineEdit()

        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        form.addRow(
            "Password:",
            self.password_input
        )

        layout.addLayout(form)

        # -------------------------------------------------
        # Run Button
        # -------------------------------------------------

        self.run_button = QPushButton(
            "Run Smoke Test"
        )

        layout.addWidget(
            self.run_button,
            alignment=Qt.AlignCenter
        )

        self.setLayout(layout)

    def configuration(self):
        """
        Returns the current configuration.

        Returns
        -------
        dict
            Smoke test configuration.
        """

        return {

            "url": self.url_input.text(),

            "username": self.username_input.text(),

            "password": self.password_input.text(),

        }