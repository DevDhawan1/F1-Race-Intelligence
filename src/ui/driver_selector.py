import streamlit as st


def get_available_drivers(results):
    """Return sorted unique driver abbreviations from session results."""
    if results is None or results.empty or "Abbreviation" not in results.columns:
        return []
    return sorted(results["Abbreviation"].dropna().astype(str).unique().tolist())


def driver_selector(session):
    """
    Display a driver dropdown and return the selected driver.
    """

    results = getattr(session, "results", None)
    drivers = get_available_drivers(results)

    if not drivers:
        st.info("No driver results are available for this session.")
        return None

    return st.selectbox(
        "Driver",
        drivers,
    )



