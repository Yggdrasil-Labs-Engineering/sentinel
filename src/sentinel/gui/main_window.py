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

        self.setMenuBar(
            self.menu_bar
        )

        # Connect menu actions

        self.menu_bar.exit_action.triggered.connect(
            self.close
        )

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

        layout.addWidget(
            self.hero_banner
        )

        # -------------------------------------------------
        # Configuration Panel
        # -------------------------------------------------

        self.configuration_panel = ConfigurationPanel()

        layout.addWidget(
            self.configuration_panel
        )


        #-------------------------------------------------
        # Connect Events
        #-------------------------------------------------

        self.configuration_panel.run_button.clicked.connect(
            self._run_smoke_test
        )

        # -------------------------------------------------
        # Results Panel
        # -------------------------------------------------

        self.results_panel = ResultsPanel()

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

        central_widget.setLayout(
            layout
        )

        self.setCentralWidget(
            central_widget
        )

    def _run_smoke_test(self):

        """

        Execute the Sentinel smoke test. 

        """

        config = self.configuration_panel.get_configuration()

        engine = SmokeEngine(

            base_url=config["url"],

            username=config["username"],

            password=config["password"],
        )

        results = engine.execute()

        print("\n==============================")
        print(" Sentinel Results")
        print("==============================")

        for result in results:

            status = "PASS" if result.passed else "FAIL"

            print(f"[{status}] {result.name}")

            print (f"  Message       :  {result.message}")

            if result.status_code is not None: 

                print(f" HTTP        :  {result.status_code}")

            if result.duration_ms is not None:

                print(f" Duration    :  {result.duration_ms:.2f} ms")

            print() 


    