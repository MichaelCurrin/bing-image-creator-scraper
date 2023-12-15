"""
Files module.

Read files of URLs.
"""

from pathlib import Path


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


def all_urls(firefox_path: Path, edge_path: Path) -> list[str]:
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
