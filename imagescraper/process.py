"""
Process module.
"""
import bs4


# We need to add this explicitly like in the case of only a single creation on a page.
BING_IMAGE_DOMAIN = "https://tse1.mm.bing.net/"

# NB. Some classes and id values are randomized, but this seems constant.
CSS_IMG_CLASS = "mimg"
CSS_IMG_CLASS_SINGLE = "gir_mmimg"


def _get_prompt(soup: bs4.BeautifulSoup) -> str:
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

    Ignore query parameters in the URL.

    Expect images like this:
        <img class="mimg"
            style=""
            height="270"
            width="270"
            src="https://tse1.mm.bing.net/th/id/OIG.KrUfYLcUu0ihSU7Ucdgd?w=270&...pid=ImgGn"
            alt="a beautiful purple ... depth of field. Afbeelding 1 van 4" />
    """
    img_tags = soup.find_all("img", class_=class_name)

    image_urls = []
    for img_tag in img_tags:
        image_url = img_tag["src"].split("?")[0]

        if image_url.startswith("/"):
            image_url = f"{BING_IMAGE_DOMAIN}{image_url}"
        image_urls.append(image_url)

    return image_urls


def process_creation_page(url: str, soup: bs4.BeautifulSoup) -> tuple[str, list[str]]:
    """
    Expect HTML for a page of 1-4 creations and return the prompt/title and image URLs.
    """
    title = _get_prompt(soup)
    print("Title", title, "URL", url)

    image_urls = get_image_urls(soup, CSS_IMG_CLASS)
    if not image_urls:
        print("Trying another CSS selector")
        image_urls = get_image_urls(soup, CSS_IMG_CLASS_SINGLE)

    assert image_urls, f"Expected at least one image URL for CSS selectos at {url}"

    print("Image URLs", image_urls)

    return title, image_urls
