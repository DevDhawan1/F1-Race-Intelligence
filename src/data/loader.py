import os
import requests
import fastf1
import fastf1._api
import streamlit as st
from pathlib import Path

# Patch default timeout for all HTTP requests to prevent socket hanging on Streamlit Cloud
_original_session_request = requests.Session.request

def _request_with_default_timeout(self, method, url, **kwargs):
    if "timeout" not in kwargs or kwargs["timeout"] is None:
        kwargs["timeout"] = (10, 60)  # 10s connect, 60s read timeout
    return _original_session_request(self, method, url, **kwargs)

requests.Session.request = _request_with_default_timeout

# Configure full browser headers for FastF1 API calls to bypass Cloudflare/F1 CDN blocking on Streamlit Cloud
fastf1._api.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.formula1.com/",
    "Origin": "https://www.formula1.com",
})

# Get the root of the project (F1-Race-Intelligence)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Cache directory: use FASTF1_CACHE env var if set, else default to project data/cache
cache_env = os.environ.get("FASTF1_CACHE")
if cache_env:
    CACHE_DIR = Path(cache_env)
else:
    CACHE_DIR = PROJECT_ROOT / "data" / "cache"

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Enable caching
fastf1.Cache.enable_cache(str(CACHE_DIR))


@st.cache_resource(show_spinner=False)
def load_session(year: int, grand_prix: str, session_type: str):
    """
    Load an F1 session and return the FastF1 Session object.
    Cached in memory across reruns with Streamlit cache_resource.
    """

    session = fastf1.get_session(
        year,
        grand_prix,
        session_type
    )

    session.load()

    return session
