import re
import requests
import streamlit as st
from requests import RequestException

F1_DRIVERS_URL = "https://www.formula1.com/en/drivers"

KNOWN_DRIVER_IMAGE_URLS = {
    "fracol01": "https://media.formula1.com/image/upload/c_fill,w_720/q_auto/v1740000001/common/f1/2026/alpine/fracol01/2026alpinefracol01right.webp",
    "nichul01": "https://media.formula1.com/image/upload/c_fill,w_720/q_auto/v1740000001/common/f1/2026/audi/nichul01/2026audinichul01right.webp",
    "serper01": "https://media.formula1.com/image/upload/c_fill,w_720/q_auto/v1740000001/common/f1/2026/cadillac/serper01/2026cadillacserper01right.webp",
}


def parse_driver_images(html):
    """Extract driver image URLs from Formula1.com HTML."""
    urls = re.findall(
        r"https://media\.formula1\.com/image/upload/[^\"']*common/f1/2026/[^\"']*right\.webp",
        html,
    )
    drivers = {}
    for url in urls:
        slug = re.search(r"/([a-z]{6}\d{2})/", url)
        if slug:
            drivers[slug.group(1)] = url.replace("w_440", "w_600").replace("c_lfill", "c_fit")
    return drivers


@st.cache_data(show_spinner=False, max_entries=4)
def load_driver_images():
    """
    Returns

    {
        "lannor01": "...url...",
        "maxver01": "...url..."
    }
    """

    try:
        response = requests.get(F1_DRIVERS_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        response.raise_for_status()
        return parse_driver_images(response.text)
    except (RequestException, ValueError):
        return {}


def get_driver_image(slug):

    if not slug:
        return None

    if slug in KNOWN_DRIVER_IMAGE_URLS:
        return KNOWN_DRIVER_IMAGE_URLS[slug]

    images = load_driver_images()

    return images.get(slug)



