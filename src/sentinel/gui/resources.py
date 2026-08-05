"""
=========================================================
Yggdrasil Labs Engineering

OVERWATCH Sentinel

resources.py

Purpose:
Application metadata and resource definitions.

This module centralizes application information used
throughout the Sentinel desktop application.

Keeping these values in one location ensures consistency
across the user interface, reporting, and future releases.
=========================================================
"""

# =========================================================
# Application Information
# =========================================================

APP_NAME = "OVERWATCH Sentinel"

APP_VERSION = "0.1.0"

WINDOW_TITLE = "OVERWATCH Sentinel"

ORGANIZATION = "Yggdrasil Labs Engineering"

PRODUCT_FAMILY = "OVERWATCH"

APPLICATION_CATEGORY = "Rapid API Operational Readiness"

MOTTO = (
    "Rapid API Validation. "
    "Immediate Operational Confidence."
)

COPYRIGHT = "© 2026 Yggdrasil Labs Engineering"

# =========================================================
# Window Defaults
# =========================================================

WINDOW_WIDTH = 1200

WINDOW_HEIGHT = 800

MINIMUM_WIDTH = 1000

MINIMUM_HEIGHT = 700

# =========================================================
# Application Assets
# =========================================================

HERO_BANNER = "assets/sentinel-hero-banner.png"

WINDOW_ICON = "assets/icon.png"

# =========================================================
# About Dialog
# =========================================================

ABOUT_TEXT = f"""
{APP_NAME}

Version: {APP_VERSION}

{APPLICATION_CATEGORY}

{MOTTO}

Developed by
{ORGANIZATION}
"""