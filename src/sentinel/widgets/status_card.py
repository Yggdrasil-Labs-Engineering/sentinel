"""
=========================================================
Yggdrasil Labs Engineering

Status Card

Purpose:
Reusable status card component for displaying
operational status information.

This widget is application agnostic and may be
used by any Yggdrasil Labs Engineering project.
=========================================================
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class StatusCard(QFrame):
    """
    Reusable operational status card.
    """

    def __init__(
        self,
        title: str,
    ):
        super().__init__()

        self._initialize_ui(
            title,
        )

    def _initialize_ui(
        self,
        title: str,
    ):
        """
        Build the Status Card UI.
        """

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("⚪ Waiting")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_waiting(self):
        self.status_label.setText("⚪ Waiting")

    def set_running(self):
        self.status_label.setText("🟡 Running")

    def set_pass(self):
        self.status_label.setText("🟢 PASS")

    def set_fail(self):
        self.status_label.setText("🔴 FAIL")
