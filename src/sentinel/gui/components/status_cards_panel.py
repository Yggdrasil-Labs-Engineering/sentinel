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

    VALID_STATES = {
        "waiting",
        "running",
        "pass",
        "fail",
    }

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

        # -------------------------------------------------
        # Status Card Registry
        # -------------------------------------------------

        self._cards = {
            "connectivity": self.connectivity_card,
            "authentication": self.authentication_card,
            "endpoint": self.endpoint_card,
            "overall": self.overall_card,
        }

        layout.addWidget(self.connectivity_card)

        layout.addWidget(self.authentication_card)

        layout.addWidget(self.endpoint_card)

        layout.addWidget(self.overall_card)

        self.setLayout(layout)

    def reset(self):
        """
        Reset every status card to Waiting.
        """

        for card in self._cards.values():
            card.set_waiting()

    def update_card(
        self,
        card_name: str,
        status: str,
    ):
        """
        Update a registered status card.

        Args:
            card_name:
                Name of the registered status card.

            status:
                Operational state to display.

                Supported values:
                    - waiting
                    - running
                    - pass
                    - fail
        """

        card = self._cards.get(card_name)

        if card is None:
            raise ValueError(f"Unknown registered card: {card_name}")

        if status not in self.VALID_STATES:
            raise ValueError(f"Unknown status: {status}")

        actions = {
            "waiting": card.set_waiting,
            "running": card.set_running,
            "pass": card.set_pass,
            "fail": card.set_fail,
        }

        actions[status]()
