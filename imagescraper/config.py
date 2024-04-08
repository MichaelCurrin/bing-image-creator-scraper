"""
Config module.
"""

from pathlib import Path


APP_DIR = Path(__file__).parent
VAR_DIR = APP_DIR / "var"
HISTORY_PROCESSED_DIR = VAR_DIR / "history_processed"
IMG_OUTPUT_DIR = VAR_DIR / "creations"
LOG_PATH = VAR_DIR / "log" / "activity.log"

WEB_APP_DIR = APP_DIR.parent / "public"
WEB_APP_DATA = WEB_APP_DIR / "creation-data.json"

BING_CREATE_URL = "https://www.bing.com/images/create/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101"
    " Firefox/117.0",
}

# Based on Bing's URLs.
CREATION_DIR_NAME_MAX_LENGTH = 50

TIMEOUT = 5
