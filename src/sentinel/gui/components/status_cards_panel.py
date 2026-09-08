"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

status_cards_panel.py

Purpose:
Display operational status cards for the
current smoke test execution.

Responsibilities:
    - Create reusable StatusCard widgets.
    - Arrange cards within the panel.
    - Provide a single interface for updating
      operational status.

The StatusCardsPanel organizes reusable
StatusCard widgets into a dashboard view.
=========================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
)

from sentinel.widgets.status_card import StatusCard


class StatusCardsPanel(QFrame):
    """
    Displays operational status cards.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

    def _initialize_ui(self):
        """
        Build the Status Cards Panel.
        """

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout()

        self.connectivity_card = StatusCard("Connectivity")

        self.authentication_card = StatusCard("Authentication")

        self.endpoint_card = StatusCard("Endpoint")

        self.overall_card = StatusCard("Overall")

        layout.addWidget(self.connectivity_card)

        layout.addWidget(self.authentication_card)

        layout.addWidget(self.endpoint_card)

        layout.addWidget(self.overall_card)

        self.setLayout(layout)
