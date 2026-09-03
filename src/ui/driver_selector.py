import streamlit as st


def driver_selector(session):
    """
    Display a driver dropdown and return the selected driver.
    """

    drivers = sorted(session.results["Abbreviation"].tolist())

    return st.selectbox(
        "Driver",
        drivers,
    )



