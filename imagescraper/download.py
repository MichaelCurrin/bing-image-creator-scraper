"""
Download module.

Request HTML and download images and metadata.
"""
import re

import requests

from .config import CREATION_DIR_NAME_MAX_LENGTH, IMG_OUTPUT_DIR, TIMEOUT


METADATA_NAME = "metadata.txt"


def _uuid_from_url(url: str):
    """
    Get UUID from Bing Image Creation URL.

    https://www.bing.com/images/create/a-beautiful-...-dr/651328ae9a6646c9b1b66c9a26c1bf2f
    => 651328ae9a6646c9b1b66c9a26c1bf2f
    """
    assert "?" not in url, (
        "Query parameters are not allowed in the URL."
        " Fix the URL. Or new logic has to be added for this."
    )

    parts = url.rsplit("/", maxsplit=1)

    assert parts, f"Could not split URL to find UUID. url: {url}"

    return parts[-1]


def _slugify(value: str) -> str:
    """
    Convert a value to lowercase alphanumeric and hyphens in place of spaces.
    """
    value = value.replace(" ", "-")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.lower()

    return value


def _as_folder_name(prompt: str, uuid: str) -> str:
    """
    Make a folder name as a short prompt and Bing's creation UUID.

    The first part is a short slug form of the prompt to keep it readable.
    Note some URLs are much longer and also Chrome history has dash as encoded
    character. So this is a standard slug, instead of relying on the text within
    a URL.

    There may be some duplication across creations where the front part is the
    same, so to ensure they are kept unique where separate based on the
    Bing creation UUID. Note that slicing the UUID to be short was not sufficient
    in an earlier attempt as Bing repeats the start of a UUID for creations
    which have similar prompts.
    """
    prompt_slug = _slugify(prompt)
    prompt_slug = prompt_slug[:CREATION_DIR_NAME_MAX_LENGTH]

    return f"{prompt_slug}-{uuid}"


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


def download_images(prompt: str, url: str, image_urls: list[str]) -> None:
    """
    Download image URLs for a creation page to a folder and make a text file
    containing the metadata.
    """
    uuid = _uuid_from_url(url)

    folder_name = _as_folder_name(prompt, uuid)
    print("Folder name", folder_name)

    folder_path = IMG_OUTPUT_DIR / folder_name

    folder_path.mkdir(parents=True, exist_ok=True)

    metadata_txt = f"{url}\n{prompt.strip()}"
    metadata_path = folder_path / METADATA_NAME
    metadata_path.write_text(metadata_txt)

    for i, image_url in enumerate(image_urls):
        file_path = folder_path / f"{uuid}_{i + 1}.png"
        response = requests.get(image_url, timeout=TIMEOUT)
        file_path.write_bytes(response.content)
