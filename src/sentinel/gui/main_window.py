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

from sentinel.engine.smoke_engine import SmokeEngine

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

from urllib.parse import urlparse

from sentinel.gui.components.configuration_panel import ConfigurationPanel
from sentinel.gui.components.footer import Footer
from sentinel.gui.components.hero_banner import HeroBanner
from sentinel.gui.components.results_panel import ResultsPanel
from sentinel.gui.menu_bar import SentinelMenuBar

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
        - Coordinate high-level UI events.
        - Provide the primary application shell.
    """

    def __init__(self):
        super().__init__()

        self._initialize_window()
        self._initialize_ui()

    # =====================================================
    # Window Initialization
    # =====================================================

    def _initialize_window(self):
        """
        Configure the main application window.
        """

        self.setWindowTitle(WINDOW_TITLE)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        # -------------------------------------------------
        # Menu Bar
        # -------------------------------------------------

        self.menu_bar = SentinelMenuBar(self)

        self.setMenuBar(self.menu_bar)

        # Connect menu actions

        self.menu_bar.exit_action.triggered.connect(self.close)

    # =====================================================
    # User Interface
    # =====================================================

    def _initialize_ui(self):
        """
        Build the application interface.
        """

        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(16)

        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        # -------------------------------------------------
        # Hero Banner
        # -------------------------------------------------

        self.hero_banner = HeroBanner()

        layout.addWidget(self.hero_banner)

        # -------------------------------------------------
        # Configuration Panel
        # -------------------------------------------------

        self.configuration_panel = ConfigurationPanel()

        layout.addWidget(self.configuration_panel)

        # -------------------------------------------------
        # Connect Events
        # -------------------------------------------------

        self.configuration_panel.run_button.clicked.connect(self._run_smoke_test)

        # -------------------------------------------------
        # Results Panel
        # -------------------------------------------------

        self.results_panel = ResultsPanel()

        layout.addWidget(self.results_panel)

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        self.footer = Footer()

        layout.addWidget(self.footer)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _is_valid_url(
        self,
        url: str,
    ) -> bool:
        """
        Validate a target URL.
        """

        parsed = urlparse(url)

        return parsed.scheme in ("http", "https") and bool(parsed.netloc)

    def _run_smoke_test(self):
        """
        Execute the Sentinel smoke test.
        """

        # -------------------------------------------------

        # Prepare Results Panel
        # -------------------------------------------------

        self.results_panel.clear_results()

        self.results_panel.update_status("🔵 Running Smoke Test...")

        self.results_panel.append_message("Initializing smoke test...")

        # -------------------------------------------------
        # Prevent multiple executions
        # -------------------------------------------------

        self.configuration_panel.run_button.setEnabled(False)
        self.configuration_panel.run_button.setText("Running...")

        # -------------------------------------------------
        # Collect Configuration
        # -------------------------------------------------

        config = self.configuration_panel.get_configuration()

        # -------------------------------------------------
        # Validate Target URL
        # -------------------------------------------------

        if not config["url"]:

            self.results_panel.clear_results()

            self.results_panel.update_status("🟡 Validation Failed")

            self.results_panel.append_message(
                "Target URL is required before a smoke test can be executed."
            )

            self.statusBar().showMessage("🟡 Target URL Required")

            self.configuration_panel.run_button.setEnabled(True)

            self.configuration_panel.run_button.setText("Run Smoke Test")

            return

        # -------------------------------------------------
        # Validate URL Format
        # -------------------------------------------------

        if not self._is_valid_url(config["url"]):

            self.results_panel.clear_results()

            self.results_panel.update_status("🟡 Validation Failed")

            self.results_panel.append_message("Please enter a valid HTTP or HTTPS URL.")

            self.results_panel.append_message("")

            self.results_panel.append_message("Examples:")

            self.results_panel.append_message("   http://localhost:8888")

            self.results_panel.append_message("   https://demo.crapi.apisec.ai")

            self.statusBar().showMessage("🟡 Invalid URL")

            self.configuration_panel.run_button.setEnabled(True)

            self.configuration_panel.run_button.setText("Run Smoke Test")

            return
        # -------------------------------------------------
        # Create Smoke Engine
        # -------------------------------------------------

        engine = SmokeEngine(
            base_url=config["url"],
            username=config["username"],
            password=config["password"],
        )

        # -------------------------------------------------
        # Execute Smoke Test
        # -------------------------------------------------

        try:
            smoke_result = engine.execute()

            # -------------------------------------------------
            # Display Results
            # -------------------------------------------------

            self.results_panel.display_results(smoke_result)

            if smoke_result.overall_passed:
                self.statusBar().showMessage("🟢 Smoke Test Passed")
            else:
                self.statusBar().showMessage("🔴 Smoke Test Failed")

        except Exception as ex:

            self.results_panel.clear_results()

            self.results_panel.update_status("🔴 Smoke Test Failed")

            self.results_panel.append_message("An unexpected error occurred.")

            self.results_panel.append_message("")

            self.results_panel.append_message(str(ex))

            self.statusBar().showMessage("🔴 Smoke Test Failed")

        finally:

            # -------------------------------------------------
            # Restore UI
            # -------------------------------------------------

            self.configuration_panel.run_button.setEnabled(True)

            self.configuration_panel.run_button.setText("Run Smoke Test")
