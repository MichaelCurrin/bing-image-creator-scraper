"""
Config module.
"""
from pathlib import Path


APP_DIR = Path(__file__)
VAR_DIR = APP_DIR / Path("var")
FIREFOX_URLS_PATH = VAR_DIR / "history_processed" / "firefox_urls.txt"
IMG_OUTPUT_PATH = VAR_DIR / "creations"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101"
    " Firefox/117.0",
}

CREATION_DIR_NAME_MAX_LENGTH = 40
TIMEOUT = 5
