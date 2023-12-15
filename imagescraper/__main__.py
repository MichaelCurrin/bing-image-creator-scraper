"""
Bing AI scraper app.

Extract prompts and images from text file of URLs.

Read URLs for a text file, get the prompt and image URLs for that page
and save them.
"""
import sys
from pathlib import Path

import bs4

from . import download, process
from .config import FIREFOX_URLS_PATH, EDGE_URLS_PATH, HEADERS


def _read_file(path: Path) -> list[str]:
    """
    Return all non-empty lines in a text file.
    """
    results = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            results.append(line)

    return results


def _all_urls(firefox_path: Path, edge_path: Path) -> list[str]:
    """
    Read URLs from Firefox and Edge text files if they exist and return combined
    URLs list.
    """
    assert (
        firefox_path.exists() or not edge_path.exists()
    ), "Unable to find either the Firefox or Edge files of URLs"

    urls = []
    if firefox_path.exists():
        firefox_urls = _read_file(firefox_path)
        assert firefox_urls, "Firefox URLs text file cannot be empty"
        urls.extend(firefox_urls)

    if edge_path.exists():
        edge_urls = _read_file(edge_path)
        assert edge_urls, "Edge URLs text file cannot be empty"
        urls.extend(edge_urls)

    return urls


def download_for_creation_page(url: str, html: str):
    """
    Request images for creation page HTML and store them, with creation metadata.
    """
    soup = bs4.BeautifulSoup(html, "html.parser")
    prompt, image_urls = process.process_creation_page(url, soup)

    download.download_images(prompt, url, image_urls)


def main(args: list[str]) -> None:
    """
    Main command-line entry-point.

    TODO: Add flag so existing folders can be skipped if they are not empty.
    TODO: Add a flag to fetch exactly one item always and write it.
    """
    if args:
        url = args.pop(0)
        urls = [url]
    else:
        urls = _all_urls(FIREFOX_URLS_PATH, EDGE_URLS_PATH)

    print("GET HTML FOR CREATION PAGE URLS")
    html_content = download.get_html_for_urls(urls, HEADERS)

    print("GET PROMPT AND IMAGE URLS AND DOWNLOAD")
    for url, html in html_content.items():
        download_for_creation_page(url, html)


if __name__ == "__main__":
    main(sys.argv[1:])
