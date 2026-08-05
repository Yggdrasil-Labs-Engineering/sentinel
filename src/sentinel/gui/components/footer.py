"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

footer.py

Purpose:
Reusable application footer component.

Displays application status, version information,
and organizational branding.

This component is intended to be shared across
future Yggdrasil Labs desktop applications.

=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
)

from sentinel.gui.resources import (
    APP_VERSION,
    ORGANIZATION,
)


class Footer(QFrame):
    """
    Reusable application footer.

    Responsibilities:
        - Display application status.
        - Display organization branding.
        - Display application version.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

    def _initialize_ui(self):
        """
        Builds the footer user interface.
        """

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout()

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        self._status_label = QLabel("🟢 Ready")
        self._status_label.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        # -------------------------------------------------
        # Organization
        # -------------------------------------------------

        organization_label = QLabel(
            ORGANIZATION
        )

        organization_label.setAlignment(Qt.AlignCenter)

        # -------------------------------------------------
        # Version
        # -------------------------------------------------

        version_label = QLabel(
            f"Version {APP_VERSION}"
        )

        version_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addWidget(self._status_label)

        layout.addStretch()

        layout.addWidget(organization_label)

        layout.addStretch()

        layout.addWidget(version_label)

        self.setLayout(layout)

    def update_status(
        self,
        status: str
    ):
        """
        Updates the application status displayed
        in the footer.

        Parameters
        ----------
        status:
            New status message.
        """

        self._status_label.setText(status)