"""
Download module.
"""
import re
import hashlib

import requests

from .config import CREATION_DIR_NAME_MAX_LENGTH, IMG_OUTPUT_PATH, TIMEOUT


def _slugify(value: str) -> str:
    """
    Convert a value to lowercase alphanumeric and hyphens in place of spaces.
    """
    value = value.replace(" ", "-")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.lower()

    return value


def _as_folder_name(prompt: str) -> str:
    """
    Make a folder name as a short prompt and hash.

    The first part is a short slug form of the prompt to keep it readable.

    The end is a hash based on the entire prompt so that it is unique but
    every time you run the app for the same URL it will be the same. So we
    can re-download with new app logic. Or choose to skip URLs we already
    downloaded, so we can focus on new URLs or failed URLs.
    """
    prompt_slug = _slugify(prompt)
    prompt_slug = prompt_slug[:CREATION_DIR_NAME_MAX_LENGTH]

    hash_value = hashlib.sha1(prompt.encode("utf-8"))
    hash_str = hash_value.hexdigest()[:8]

    return f"{prompt_slug}-{hash_str}"


def _get_html(url: str, headers: dict[str, str]) -> str:
    """
    Request HTML for a URL and return as text.
    """
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    assert response.ok, f"{response.status_code} - {response.reason} - {url}"

    html = response.text

    return html


def get_html_for_urls(urls: list[str], headers: dict[str, str]) -> dict[str, str]:
    """
    Request URls return the HTML content for each URL.
    """
    html_content = {}

    for url in urls:
        print("URL", url)
        html = _get_html(url, headers)
        html_content[url] = html

    return html_content


def download_images(prompt: str, image_urls: list[str]) -> None:
    """
    Download image URLs for a creation page to a folder and make a text file
    containing the prompt.
    """
    folder_name = _as_folder_name(prompt)
    print("Folder name", folder_name)

    folder_path = IMG_OUTPUT_PATH / folder_name

    if not folder_path.exists():
        folder_path.mkdir(parents=True)
    else:
        print("Skipping", folder_path)
        return

    (folder_path / "prompt.txt").write_text(prompt)

    for i, image_url in enumerate(image_urls):
        # TBD format, maybe full name is useful when moving out of folder
        file_path = folder_path / f"{i + 1}.png"
        response = requests.get(image_url, timeout=TIMEOUT)
        file_path.write_bytes(response.content)
