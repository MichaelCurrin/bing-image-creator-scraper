"""
Bing AI scraper app.

Extract prompts and images from text file of URLs.

Read URLs for a text file, get the prompt and image URLs for that page
and save them.

Note on logic for retries:
    - If a directory exists with a `metadata.txt` file with a URL on the first time,
      then that URL will be skipped.
      Skipping that URL allows the initialy scrape of creation pages to
      be quicker.
    - If a directory exists, no error will happen on directory creation
      but the logic will run anyway (in case the directory is empty
      so there is no `metadata.txt` file in it).
    - To retry a specific case, delete file `metadata.txt` file or the whole
      directory for that creation.
"""
import sys
import logging

import bs4

from . import download, files, process_html
from .config import HEADERS, HISTORY_PROCESSED_DIR, IMG_OUTPUT_DIR, LOG_PATH

# Configure logging to save errors to a file
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
        urls = files.urls_from_text_files(HISTORY_PROCESSED_DIR, IMG_OUTPUT_DIR)

    logging.info("Found URLs: %d", len(urls))

    print("GET HTML FOR CREATION PAGE URLS")
    html_content = download.get_html_for_urls(urls, HEADERS)
    print()

    print("GET PROMPT AND IMAGE URLS AND DOWNLOAD")
    for url, html in html_content.items():
        try:
            download_for_creation_page(url, html)
        except Exception:
            logging.exception("Failed to download for %s", url)


if __name__ == "__main__":
    main(sys.argv[1:])
