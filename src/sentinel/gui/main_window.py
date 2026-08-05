"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

main_window.py

Purpose:
Main application window.

Assembles the Sentinel user interface from reusable
components.

Responsibilities:
    - Build the primary application window.
    - Arrange interface components.
    - Coordinate high-level user interaction.

Business logic belongs elsewhere.
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

from sentinel.gui.components.configuration_panel import ConfigurationPanel
from sentinel.gui.components.footer import Footer
from sentinel.gui.components.hero_banner import HeroBanner
from sentinel.gui.components.results_panel import ResultsPanel

from sentinel.gui.resources import (
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


class MainWindow(QMainWindow):
    """
    Main Sentinel application window.

    Responsibilities:
        - Assemble reusable UI components.
        - Provide the primary application shell.
        - Coordinate user interaction.

    This class intentionally contains very little
    business logic.
    """

    def __init__(self):
        super().__init__()

        self._initialize_window()
        self._initialize_ui()

    def _initialize_window(self):
        """
        Configure the main application window.
        """

        self.setWindowTitle(WINDOW_TITLE)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

    def _initialize_ui(self):
        """
        Build the application interface.
        """

        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(12)

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        # -------------------------------------------------
        # Hero Banner
        # -------------------------------------------------

        self.hero_banner = HeroBanner()

        layout.addWidget(
            self.hero_banner
        )

        # -------------------------------------------------
        # Configuration Panel
        # -------------------------------------------------

        self.configuration_panel = (
            ConfigurationPanel()
        )

        layout.addWidget(
            self.configuration_panel
        )

        # -------------------------------------------------
        # Results Panel
        # -------------------------------------------------

        self.results_panel = (
            ResultsPanel()
        )

        layout.addWidget(
            self.results_panel
        )

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        self.footer = Footer()

        layout.addWidget(
            self.footer
        )

        central_widget.setLayout(layout)

        self.setCentralWidget(
            central_widget
        )