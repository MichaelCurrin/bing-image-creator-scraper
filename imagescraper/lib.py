"""
Library module.
"""
import hashlib
import re

from .config import CREATION_DIR_NAME_MAX_LENGTH


def _slugify(value: str) -> str:
    """
    Convert a value to lowercase alphanumeric and hyphens in place of spaces.
    """
    value = value.replace(" ", "-")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.lower()

    return value


def as_folder_name(title: str) -> str:
    """
    Make a folder name as a short title and hash.

    The first part is a short slug form of the title to keep it readable.

    The end is a hash based on the entire title so that it is unique but
    every time you run the app for the same URL it will be the same. So we
    can re-download with new app logic. Or choose to skip URLs we already
    downloaded, so we can focus on new URLs or failed URLs.
    """
    title_slug = _slugify(title)
    title_slug = title_slug[:CREATION_DIR_NAME_MAX_LENGTH]

    hash_value = hashlib.sha1(title.encode("utf-8"))
    hash_str = hash_value.hexdigest()[:8]

    return f"{title_slug}-{hash_str}"
