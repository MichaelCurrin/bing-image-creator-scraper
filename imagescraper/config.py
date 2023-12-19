"""
Config module.
"""
from pathlib import Path


APP_DIR = Path(__file__).parent
VAR_DIR = APP_DIR / Path("var")
HISTORY_PROCESSED_DIR = VAR_DIR / "history_processed"
IMG_OUTPUT_DIR = VAR_DIR / "creations"

BING_CREATE_URL = "https://www.bing.com/images/create/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101"
    " Firefox/117.0",
}

CREATION_DIR_NAME_MAX_LENGTH = 40
TIMEOUT = 5
