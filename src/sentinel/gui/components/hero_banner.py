"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

hero_banner.py

Purpose:
Reusable Hero Banner component.

Displays the Sentinel product banner at the top of the
application window.

This component is responsible only for loading,
scaling, and displaying the banner image.

=========================================================
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]

BANNER_PATH = (PROJECT_ROOT / "assets" / "sentinel-hero-banner.png")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class HeroBanner(QWidget):
    """
    Displays the Sentinel application hero banner.

    Responsibilities:
        - Load the application banner image.
        - Scale the image while preserving aspect ratio.
        - Display the banner at the top of the application.
    """

    def __init__(self):
        super().__init__()

        self._initialize_ui()

    def _initialize_ui(self):
        """
        Builds the banner user interface.
        """

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        banner = QLabel()
        banner.setAlignment(Qt.AlignCenter)

        banner_path = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "assets"
            / "sentinel-hero-banner.png"
        )

        pixmap = QPixmap(str(BANNER_PATH))

        if not pixmap.isNull():

            banner.setPixmap(
                pixmap.scaled(
                    1000,
                    250,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        else:

            banner.setText(
                "OVERWATCH Sentinel\n"
                "Hero Banner Missing"
            )

        layout.addWidget(banner)

        self.setLayout(layout)