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

import sys
from pathlib import Path


def _resource_path(relative_path: str) -> Path:
    """
    Resolve an application resource path.

    Supports both normal source execution and
    PyInstaller-packaged execution.
    """

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).resolve().parents[4] / relative_path


BANNER_PATH = _resource_path("assets/sentinel-hero-banner.png")

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
                "Hero Banner Missing\n\n"
                f"Path: {BANNER_PATH}\n"
                f"Exists: {BANNER_PATH.exists()}"
            )

        layout.addWidget(banner)

        self.setLayout(layout)
