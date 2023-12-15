"""
Download module.
"""
import requests

from . import lib
from .config import IMG_OUTPUT_PATH, TIMEOUT


def get_html(url: str, headers: dict[str, str]) -> str:
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
        html = get_html(url, headers)
        html_content[url] = html

    return html_content


def download_images(title: str, image_urls: list[str]) -> None:
    """
    Download image URLs for a creation page to a folder and make a text file
    containing the prompt.
    """
    folder_name = lib.as_folder_name(title)
    print("Folder name", folder_name)

    folder_path = IMG_OUTPUT_PATH / folder_name

    if not folder_path.exists():
        folder_path.mkdir(parents=True)
    else:
        print("Skipping", folder_path)
        return

    (folder_path / "prompt.txt").write_text(title)

    for i, image_url in enumerate(image_urls):
        # TBD format, maybe full name is useful when moving out of folder
        file_path = folder_path / f"{i + 1}.png"
        response = requests.get(image_url, timeout=TIMEOUT)
        file_path.write_bytes(response.content)
