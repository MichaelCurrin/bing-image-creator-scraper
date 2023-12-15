"""
Bing AI scraper app.

Extract prompts and images from text file of URLs.

Read URLs for a text file, get the prompt and image URLs for that page
and save them.
"""
import random
import re
from pathlib import Path

import bs4
import requests

VAR_DIR = Path("var")
FIREFOX_URLS_PATH = VAR_DIR / "outputs" / "firefox_urls.txt"
IMG_OUTPUT_PATH = VAR_DIR / "outputs" / "creations"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101"
    " Firefox/117.0",
}

# NB. Some classes and id values are randomized, but this seems constant.
CSS_IMG_CLASS = "mimg"


def get_html(url: str, headers: dict[str, str]) -> str:
    """
    Request HTML for a URL and return as text.
    """
    response = requests.get(url, headers=headers)
    assert response.ok, f"{response.status_code} - {response.reason} - {url}"

    html = response.text

    return html


def get_html_for_urls(url_file: Path, headers: dict[str, str]) -> dict[str, str]:
    """
    Open a text file and return the HTML content for each URL.
    """
    html_content = {}

    with open(url_file, "r") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue

            print("URL", url)
            html = get_html(url, headers)
            html_content[url] = html
            break
    return html_content


def get_prompt(soup: bs4.BeautifulSoup) -> str:
    """
    Extract the prompt of a page and return it.
    """
    textarea_element = soup.select_one("form > textarea")

    assert textarea_element is not None, "Could not find textarea element"

    return textarea_element.text


def get_image_urls(soup: bs4.BeautifulSoup, class_name: str) -> list[str]:
    """
    Gets all of the image URLs on an HTML page, using the given class name
    to select the img tags.

    Ignore query parameters.
    """
    img_tags = soup.find_all("img", class_=class_name)

    image_urls = []
    for img_tag in img_tags:
        image_url = img_tag["src"].split("?")[0]
        image_urls.append(image_url)

    assert image_urls, "Expected at leat one image URL"

    return image_urls


def slugify(value: str) -> str:
    """
    Convert a value to lowercase alphanumeric and hyphens in place of spaces.
    """
    value = value.replace(" ", "-")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.lower()

    return value


def make_folder_name(title: str) -> str:
    """
    Makes a folder name given a title.
    """
    title = slugify(title)
    title = title[:20]

    random_number = random.randint(100000, 999999)

    return f"{title}-{random_number}"


def download_images(title: str, image_urls: list[str]) -> None:
    """
    Download image URLs for a creation page to a folder, with a text file containing the prompt.
    """
    folder_name = make_folder_name(title)
    print("Folder name", folder_name)

    folder_path = IMG_OUTPUT_PATH / folder_name
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    (folder_path / "prompt.txt").write_text(title)

    for i, image_url in enumerate(image_urls):
        file_path = folder_path / f"{i + 1}.png"  # TBD format
        response = requests.get(image_url)
        file_path.write_bytes(response.content)


def process_creation_page(url: str, soup: bs4.BeautifulSoup) -> tuple[str, list[str]]:
    """
    Expect HTML for a page of 1-4 creations and return the prompt/title and image URLs.
    """
    title = get_prompt(soup)
    print("Title", title, "URL", url)

    image_urls = get_image_urls(soup, CSS_IMG_CLASS)
    print("Image URLs", image_urls)

    return title, image_urls


def main() -> None:
    print("GET HTML FOR CREATION PAGE URLS")
    html_content = get_html_for_urls(FIREFOX_URLS_PATH, HEADERS)

    print("GET PROMPT AND IMAGE URLS AND DOWNLOAD")
    for url, html in html_content.items():
        soup = bs4.BeautifulSoup(html, "html.parser")
        title, image_urls = process_creation_page(url, soup)

        download_images(title, image_urls)


if __name__ == "__main__":
    main()
