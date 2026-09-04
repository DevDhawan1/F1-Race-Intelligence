import os
import fastf1
import streamlit as st
from pathlib import Path

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
