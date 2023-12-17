"""
Bing AI scraper app.

Extract prompts and images from text file of URLs.

Read URLs for a text file, get the prompt and image URLs for that page
and save them.
"""
import sys

import bs4

from . import download, files, process_html
from .config import HISTORY_PROCESSED_DIR, HEADERS


def download_for_creation_page(url: str, html: str):
    """
    Request images for creation page HTML and store them, with creation metadata.
    """
    soup = bs4.BeautifulSoup(html, "html.parser")
    prompt, image_urls = process_html.process_creation_page(url, soup)

    download.download_images(prompt, url, image_urls)


def main(args: list[str]) -> None:
    """
    Main command-line entry-point.
    """
    if args:
        url = args.pop(0)
        urls = [url]
    else:
        urls = files.urls_from_text_files(HISTORY_PROCESSED_DIR)

    print(f"Found URLs: {len(urls)}")

    print("GET HTML FOR CREATION PAGE URLS")
    html_content = download.get_html_for_urls(urls, HEADERS)
    print()

    print("GET PROMPT AND IMAGE URLS AND DOWNLOAD")
    for url, html in html_content.items():
        download_for_creation_page(url, html)


if __name__ == "__main__":
    main(sys.argv[1:])
