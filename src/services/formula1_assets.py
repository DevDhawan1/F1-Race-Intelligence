import re
import requests
import streamlit as st

F1_DRIVERS_URL = "https://www.formula1.com/en/drivers"


@st.cache_data(show_spinner=False)
def load_driver_images():
    """
    Returns

    {
        "lannor01": "...url...",
        "maxver01": "...url..."
    }
    """

    response = requests.get(
        F1_DRIVERS_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )

    response.raise_for_status()

    html = response.text

    urls = re.findall(
        r"https://media\.formula1\.com/image/upload/[^\"']*common/f1/2026/[^\"']*right\.webp",
        html,
    )

    drivers = {}

    for url in urls:

        slug = re.search(
            r"/([a-z]{6}\d{2})/",
            url,
        )

        if slug:

            # Request a higher resolution portrait
            high_res = url.replace("w_440", "w_600").replace("c_lfill", "c_fit")

            drivers[slug.group(1)] = high_res

    return drivers


def get_driver_image(slug):

    images = load_driver_images()

    return images.get(slug)



