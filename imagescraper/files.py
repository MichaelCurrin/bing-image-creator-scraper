"""
Files module.

Read files of URLs.
"""

from pathlib import Path
from .config import BING_CREATE_URL


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


def urls_from_text_files(dir_path: Path) -> list[str]:
    """
    Read URLs from text files in the given directory.

    Query parameters and duplicates will be removed. Note, sometimes unnecessary
    query parameters appear like this
        '...891?FORM=GLP2CR'.
    """
    print(f"Reading files in: {dir_path}")
    text_files = dir_path.glob("*.txt")

    urls = []

    for f in text_files:
        contents = f.read_text()
        urls.extend(contents.split("\n"))

    assert urls, f"No files found or files are empty directory:\n {dir_path}"

    urls = [url.split("?")[0] for url in urls if url and _is_creation_url(url)]

    unique_urls = set(urls)
    urls = sorted(unique_urls)

    return urls
