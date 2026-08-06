"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

menu_bar.py

Purpose:
Application menu bar.

Provides the standard desktop menu used throughout
the Sentinel application.

Future Yggdrasil Labs desktop applications should
reuse this design.

=========================================================
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class SentinelMenuBar(QMenuBar):
    """
    Main application menu bar.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._initialize_actions()
        self._build_menu()

    # =====================================================
    # Initialization
    # =====================================================

    def _initialize_actions(self):
        """
        Create all menu actions.
        """

        # -----------------------------
        # File
        # -----------------------------

        self.new_session_action = QAction(
            "New Session",
            self
        )

        self.open_configuration_action = QAction(
            "Open Configuration...",
            self
        )

        self.save_configuration_action = QAction(
            "Save Configuration...",
            self
        )

        self.exit_action = QAction(
            "Exit",
            self
        )

        # -----------------------------
        # View
        # -----------------------------

        self.toggle_toolbar_action = QAction(
            "Toggle Toolbar",
            self
        )

        self.toggle_console_action = QAction(
            "Toggle Console",
            self
        )

        self.reset_layout_action = QAction(
            "Reset Layout",
            self
        )

        # -----------------------------
        # Tools
        # -----------------------------

        self.settings_action = QAction(
            "Settings...",
            self
        )

        self.developer_tools_action = QAction(
            "Developer Tools...",
            self
        )

        # -----------------------------
        # Help
        # -----------------------------

        self.documentation_action = QAction(
            "Documentation",
            self
        )

        self.github_action = QAction(
            "GitHub Repository",
            self
        )

        self.about_action = QAction(
            "About OVERWATCH Sentinel",
            self
        )

    # =====================================================
    # Menu Construction
    # =====================================================

    def _build_menu(self):
        """
        Build the application menu.
        """

        # -------------------------------------------------
        # File
        # -------------------------------------------------

        file_menu = self.addMenu("&File")

        file_menu.addAction(self.new_session_action)

        file_menu.addSeparator()

        file_menu.addAction(
            self.open_configuration_action
        )

        file_menu.addAction(
            self.save_configuration_action
        )

        file_menu.addSeparator()

        file_menu.addAction(
            self.exit_action
        )

        # -------------------------------------------------
        # View
        # -------------------------------------------------

        view_menu = self.addMenu("&View")

        view_menu.addAction(
            self.toggle_toolbar_action
        )

        view_menu.addAction(
            self.toggle_console_action
        )

        view_menu.addSeparator()

        view_menu.addAction(
            self.reset_layout_action
        )

        # -------------------------------------------------
        # Tools
        # -------------------------------------------------

        tools_menu = self.addMenu("&Tools")

        tools_menu.addAction(
            self.settings_action
        )

        tools_menu.addAction(
            self.developer_tools_action
        )

        # -------------------------------------------------
        # Help
        # -------------------------------------------------

        help_menu = self.addMenu("&Help")

        help_menu.addAction(
            self.documentation_action
        )

        help_menu.addAction(
            self.github_action
        )

        help_menu.addSeparator()

        help_menu.addAction(
            self.about_action
        )