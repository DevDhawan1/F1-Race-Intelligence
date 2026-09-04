import os
import requests
import streamlit as st

# Patch default timeout for all requests to prevent indefinite socket hanging on Streamlit Cloud
_original_session_request = requests.Session.request

def _request_with_default_timeout(self, method, url, **kwargs):
    if "timeout" not in kwargs or kwargs["timeout"] is None:
        kwargs["timeout"] = (10, 60)  # 10 seconds connect timeout, 60 seconds read timeout
    return _original_session_request(self, method, url, **kwargs)

requests.Session.request = _request_with_default_timeout

# FastF1 cache directory (must be set before importing fastf1)
# Use project data/cache where pre-cached files are stored
cache_dir = os.path.join(os.getcwd(), "data", "cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ.setdefault("FASTF1_CACHE", cache_dir)

# Page Configuration
st.set_page_config(
    page_title="F1 Race Intelligence",
    page_icon=":material/directions_car:",
    layout="wide",
)

# Define Pages
dashboard = st.Page(
    "pages/0_Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True,
)

driver = st.Page(
    "pages/1_Driver_Analysis.py",
    title="Driver Analysis",
    icon=":material/person:",
)

strategy = st.Page(
    "pages/2_Strategy_Analysis.py",
    title="Strategy Analysis",
    icon=":material/tire_repair:",
)

team = st.Page(
    "pages/3_Team_Analysis.py",
    title="Team Analysis",
    icon=":material/flag:",
)

overview = st.Page(
    "pages/4_Race_Overview.py",
    title="Race Overview",
    icon=":material/analytics:",
)

# Navigation
pg = st.navigation(
    [
        dashboard,
        driver,
        strategy,
        team,
        overview,
    ]
)

pg.run()
