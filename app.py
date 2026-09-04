import os
import streamlit as st

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
