import datetime
from typing import Optional

import fastf1
import streamlit as st

from src.data.loader import load_session


# ==========================================================
# Cached Schedule
# ==========================================================


@st.cache_data(show_spinner=False)
def get_schedule(year: int):
    """
    Download and cache the F1 schedule for a season.
    """
    return fastf1.get_event_schedule(year)


# ==========================================================
# Event Mapping
# ==========================================================


def get_event_mapping(schedule):
    """
    Returns
    "Spa-Francorchamps (Belgium)"
            ->
    Complete FastF1 event row
    """
    mapping = {}
    for _, row in schedule.iterrows():
        display_name = f"{row['Location']} ({row['Country']})"
        mapping[display_name] = row
    return mapping


# ==========================================================
# Session Selector
# ==========================================================


def session_selector() -> Optional[object]:
    """Render session selection UI and return loaded session."""

    # Session State initialization
    if "session_config" not in st.session_state:
        st.session_state.session_config = {
            "year": None,
            "circuit": None,
            "session": None,
            "loaded_session": None,
        }

    config = st.session_state.session_config
    current_year = datetime.datetime.now().year

    # Season selector
    seasons = list(range(current_year, 2017, -1))
    season_options = ["Select Season"] + seasons

    selected_year = st.selectbox(
        "Season",
        season_options,
        index=season_options.index(config["year"]) if config["year"] in seasons else 0,
        key="season_selector",
    )

    if selected_year == "Select Season":
        config.update({"year": None, "circuit": None, "session": None, "loaded_session": None})
        return None

    config["year"] = selected_year

    # Circuit selector
    schedule = get_schedule(config["year"])
    event_mapping = get_event_mapping(schedule)

    circuit_options = ["Select Circuit"] + list(event_mapping.keys())
    selected_circuit = st.selectbox(
        "Circuit",
        circuit_options,
        index=circuit_options.index(config["circuit"]) if config["circuit"] in event_mapping else 0,
        key="circuit_selector",
    )

    if selected_circuit == "Select Circuit":
        config.update({"circuit": None, "session": None, "loaded_session": None})
        return None

    config["circuit"] = selected_circuit

    # Session selector - use segmented control for better UX
    event = event_mapping[config["circuit"]]
    code_map = {
        "Practice 1": "FP1",
        "Practice 2": "FP2",
        "Practice 3": "FP3",
        "Qualifying": "Q",
        "Race": "R",
        "Sprint": "S",
        "Sprint Qualifying": "SQ",
        "Sprint Shootout": "SQ",
    }

    available_sessions = []
    for i in range(1, 6):
        session_name = event.get(f"Session{i}")
        if session_name and session_name in code_map:
            available_sessions.append(session_name)

    if not available_sessions:
        st.warning("No sessions available for this event")
        return None

    # Use segmented control for session type selection
    selected_session = st.segmented_control(
        "Session Type",
        options=available_sessions,
        default=config["session"] if config["session"] in available_sessions else available_sessions[0],
        key="session_type_selector",
    )

    if selected_session:
        config["session"] = selected_session
    else:
        config["session"] = None
        return None

    # Load Session Button
    can_load = all([config["year"], config["circuit"], config["session"]])

    if st.button(
        "Load Session",
        disabled=not can_load,
        type="primary",
        width="stretch",
    ):
        session_code = code_map[config["session"]]
        with st.spinner("Loading session data..."):
            config["loaded_session"] = load_session(
                config["year"],
                event["EventName"],
                session_code,
            )
        st.rerun()

    # Currently Loaded Session display
    if config["loaded_session"] is not None:
        st.divider()
        loaded = config["loaded_session"]
        event = loaded.event

        st.caption("Currently Loaded Session")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Season", event["EventDate"].year)
        with c2:
            st.metric("Circuit", f"{event['Location']} ({event['Country']})")
        with c3:
            st.metric("Session", loaded.name)

    return config["loaded_session"]



