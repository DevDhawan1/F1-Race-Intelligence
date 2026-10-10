import streamlit as st


def get_available_drivers(results):
    """Return sorted unique driver abbreviations from session results."""
    if results is None or results.empty or "Abbreviation" not in results.columns:
        return []
    return sorted(results["Abbreviation"].dropna().astype(str).unique().tolist())


def driver_selector(session, key="driver_selector", shared_key=None):
    """
    Display a driver dropdown and return the selected driver.
    """

    results = getattr(session, "results", None)
    drivers = get_available_drivers(results)

    if not drivers:
        st.info("No driver results are available for this session.")
        return None

    if shared_key:
        shared_driver = st.session_state.get(shared_key)
        if key not in st.session_state or st.session_state[key] not in drivers:
            st.session_state[key] = (
                shared_driver if shared_driver in drivers else drivers[0]
            )

        def sync_driver_selection():
            st.session_state[shared_key] = st.session_state[key]

        selected_driver = st.selectbox(
            "Driver",
            drivers,
            key=key,
            on_change=sync_driver_selection,
        )
        st.session_state[shared_key] = selected_driver
        return selected_driver

    return st.selectbox(
        "Driver",
        drivers,
        key=key,
    )



