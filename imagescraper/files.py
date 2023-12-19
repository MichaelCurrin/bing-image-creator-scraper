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


def _get_seen_urls(path: Path) -> set:
    """
    Get all URLs which appear in text files for existing creation folders.
    """
    txt_files = path.glob("*/*.txt")
    seen_urls = set()

    for f in txt_files:
        text = f.read_text().splitlines()
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
    print(f"Reading files in: {url_files_dir}")
    text_files = url_files_dir.glob("*.txt")

    urls = []

    for f in text_files:
        lines = f.read_text().splitlines()
        urls.extend(lines)

    assert urls, f"No files found or files are empty directory:\n {url_files_dir}"

    urls = [url.split("?")[0] for url in urls if url and _is_creation_url(url)]

    unique_urls = set(urls)
    seen_urls = _get_seen_urls(creations_dir)
    unique_urls = unique_urls - seen_urls

    urls = sorted(unique_urls)

    return urls
