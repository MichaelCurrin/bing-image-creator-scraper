"""
Files module.

Read files of URLs.
"""

from pathlib import Path

from .config import BING_CREATE_URL


def _is_creation_url(url: str) -> bool:
    """
    Check if the URL matches the creation URL pattern.
    In particular to ignore `https://www.bing.com/images/create/termsofservice`
    and similar.
    """
    end = url.removeprefix(BING_CREATE_URL)

    if len(end.split("/")) == 2:
        return True

    return False


def _read_text_files(path: Path) -> set:
    print(f"Reading files in: {path}")
    text_files = path.glob("*.txt")

    urls = []

    for text_file in text_files:
        lines = text_file.read_text().splitlines()
        urls.extend(lines)

    assert urls, f"No files found or files are empty directory:\n {path}"

    urls = [url.split("?")[0] for url in urls if url and _is_creation_url(url)]

    return set(urls)


def _get_seen_urls(path: Path) -> set:
    """
    Get all URLs which already been processed.

    A URL is considered already process if there is a creations folder for
    that ID and it has a metadata text file in it.
    """
    print(f"Reading seen URLs in : {path}")
    text_files = path.glob("*/metadata.txt")
    seen_urls = set()

    for text_file in text_files:
        text = text_file.read_text().splitlines()
        url = text[0]
        seen_urls.add(url)

    return seen_urls


def urls_from_text_files(url_files_dir: Path, creations_dir: Path) -> list[str]:
    """
    Read URLs from text files in the given directory.

    Query parameters and duplicates will be removed. Note, sometimes unnecessary
    query parameters appear like this
        '...891?FORM=GLP2CR'.
    """
    unique_urls = _read_text_files(url_files_dir)
    seen_urls = _get_seen_urls(creations_dir)

    urls_to_process = unique_urls - seen_urls
    print(
        f"URLs to read: {len(unique_urls)}. Seen URLs: {len(seen_urls)}."
        f" To process: {len(urls_to_process)}."
    )

    return sorted(urls_to_process)
