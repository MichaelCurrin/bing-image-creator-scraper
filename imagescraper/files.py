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

    urls = [url.split("?")[0] for url in urls if url]

    unique_urls = set(urls)
    urls = sorted(unique_urls)

    return urls
