"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

app.py

Purpose:
Application entry point.

Initializes the Qt application, applies the
application theme, creates the main window,
and starts the Sentinel user interface.

=========================================================
"""

import sys

from PySide6.QtWidgets import QApplication

from sentinel.gui.main_window import MainWindow


def main():
    """
    Sentinel application entry point.
    """

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()