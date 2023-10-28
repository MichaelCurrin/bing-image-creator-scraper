import bs4
import requests
import re
from pathlib import Path

URLS = Path("var") / "outputs" / "firefox_urls.txt"
IMG_OUTPUT_PATH = Path("var") / "outputs" / "creations"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
}

# NB. Some classes and id values are randomized, but this seems constant.
IMG_CLASS = "mimg"


def get_html(url_file, headers):
    html_content = {}

    with open(url_file, "r") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue

            print(url)
            response = requests.get(url, headers=headers)
            assert response.ok, f"{response.status_code} - {response.reason} - {url}"

            html = response.text
            html_content[url] = html

    return html_content


def get_prompt(soup):
    """
    Extracts the prompt of a page.
    """
    textarea_element = soup.select_one("form > textarea")

    assert textarea_element is not None, "Could not find textarea"

    return textarea_element.text


def get_image_urls(soup, class_name):
    """
    Gets all of the image URLs on an HTML page, using the given class name to select the img tags.
    Ignore query parameters.
    """
    img_tags = soup.find_all("img", class_=class_name)

    image_urls = []
    for img_tag in img_tags:
        image_url = img_tag["src"]
        image_url = image_url.split("?")[0]
        image_urls.append(image_url)

    assert image_urls

    return image_urls


import random


def slugify(value):
    value = value.replace(" ", "-")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.lower()

    return value


def make_folder_name(title):
    """
    Makes a folder name given a title.
    """
    title = slugify(title)
    title = title[:20]

    random_number = random.randint(100000, 999999)

    return f"{title}-{random_number}"


def download_images(title, image_urls):
    """
    Download image URLs for a creation page to a folder, with a text file containing the prompt.
    """
    folder_name = make_folder_name(title)
    print(folder_name)

    folder_path = IMG_OUTPUT_PATH / folder_name
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    (folder_path / "prompt.txt").write_text(title)

    for i, image_url in enumerate(image_urls):
        file_path = folder_path / f"{i + 1}.png"  # TBD format
        response = requests.get(image_url)
        file_path.write_bytes(response.content)


def process_creation_page(url, soup):
    title = get_prompt(soup)
    print(title)

    image_urls = get_image_urls(soup, IMG_CLASS)
    print(image_urls)

    return title, image_urls


def main():
    print("GET HTML")
    html_content = get_html(URLS, HEADERS)

    print("GET TITLE AND IMG URLS")
    for url, html in html_content.items():
        soup = bs4.BeautifulSoup(html, "html.parser")
        title, image_urls = process_creation_page(url, soup)
        download_images(title, image_urls)


if __name__ == "__main__":
    main()
