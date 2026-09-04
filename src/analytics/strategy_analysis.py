import pandas as pd
import streamlit as st
from src.utils.lap_filters import remove_outlier_laps


def _session_cache_key(session):
    """Generate a cache key from session metadata."""
    if session is None:
        return "none"
    event = session.event
    return f"{event['EventDate'].year}_{event['EventName']}_{session.name}"


# Helper Functions
def _get_valid_laps(session):
    """
    Return all laps with a valid lap time.
    """
    try:
        laps = session.laps.copy()
    except Exception:
        return pd.DataFrame()

    laps = laps[laps["LapTime"].notna()].copy()

    laps["Lap Time (s)"] = laps["LapTime"].dt.total_seconds()

    return laps


# Stint Analysis
@st.cache_data(show_spinner=False, ttl=3600)
def stint_analysis(_session):
    """
    Generate a summary of every race stint.
    """

    laps = _get_valid_laps(_session)

    # Remove unrealistic lap times caused by red flags,
    # race stoppages, etc.
    laps = remove_outlier_laps(laps)

    stint_df = (
        laps.groupby(
            [
                "Driver",
                "Team",
                "Stint",
            ]
        )
        .agg(
            Compound=("Compound", "first"),
            Start_Lap=("LapNumber", "min"),
            End_Lap=("LapNumber", "max"),
            Number_of_Laps=("LapNumber", "count"),
            Average_Lap_Time=("Lap Time (s)", "mean"),
            Fastest_Lap=("Lap Time (s)", "min"),
        )
        .reset_index()
    )

    stint_df.rename(
        columns={
            "Start_Lap": "Start Lap",
            "End_Lap": "End Lap",
            "Number_of_Laps": "Stint Length",
            "Average_Lap_Time": "Average Lap Time (s)",
            "Fastest_Lap": "Fastest Lap (s)",
        },
        inplace=True,
    )

    numeric_cols = [
        "Average Lap Time (s)",
        "Fastest Lap (s)",
    ]

    stint_df[numeric_cols] = stint_df[numeric_cols].round(3)

    return stint_df

# Tyre Degradation
@st.cache_data(show_spinner=False, ttl=3600)
def tyre_degradation(_session):
    """
    Return lap-by-lap tyre data for degradation analysis.
    """

    laps = _get_valid_laps(_session)

    # Remove unrealistic laps (red flags etc.)
    laps = remove_outlier_laps(laps)
    
    tyre_df = laps[
        [
            "Driver",
            "Team",
            "Stint",
            "Compound",
            "TyreLife",
            "LapNumber",
            "Lap Time (s)",
        ]
    ].copy()

    tyre_df.rename(
        columns={
            "TyreLife": "Tyre Life",
            "LapNumber": "Lap Number",
        },
        inplace=True,
    )

    tyre_df["Lap Time (s)"] = tyre_df["Lap Time (s)"].round(3)

    tyre_df = tyre_df.sort_values(["Driver", "Stint", "Lap Number"]).reset_index(
        drop=True
    )

    return tyre_df


# Pit Stop Analysis
@st.cache_data(show_spinner=False, ttl=3600)
def pit_stop_analysis(_session):
    """
    Generate a summary of strategic pit stops during the race.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    pit_stops = []

    for driver in laps["Driver"].unique():

        driver_laps = (
            laps[laps["Driver"] == driver]
            .sort_values("LapNumber")
            .reset_index(drop=True)
        )

        stints = sorted(driver_laps["Stint"].unique())

        # Skip drivers who never changed tyres
        if len(stints) <= 1:
            continue

        pit_number = 1

        for i in range(1, len(stints)):

            previous_stint = stints[i - 1]
            current_stint = stints[i]

            previous_data = driver_laps[driver_laps["Stint"] == previous_stint]

            current_data = driver_laps[driver_laps["Stint"] == current_stint]

            pit_lap = int(current_data["LapNumber"].min())

            pit_stops.append(
                {
                    "Driver": driver,
                    "Team": previous_data["Team"].iloc[0],
                    "Pit Stop": pit_number,
                    "Pit Lap": pit_lap,
                    "Old Compound": previous_data["Compound"].iloc[0],
                    "New Compound": current_data["Compound"].iloc[0],
                    "Previous Stint Length": len(previous_data),
                }
            )

            pit_number += 1

    pit_df = pd.DataFrame(pit_stops)

    if pit_df.empty:
        return pit_df

    pit_df = pit_df.sort_values(["Driver", "Pit Stop"]).reset_index(drop=True)

    return pit_df


# Race Pace Evolution
@st.cache_data(show_spinner=False, ttl=3600)
def race_pace_evolution(_session):
    """
    Return lap-by-lap race pace for all drivers.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    pace_df = laps[
        [
            "Driver",
            "Team",
            "LapNumber",
            "LapTime",
            "Compound",
            "TyreLife",
            "Stint",
            "Position",
        ]
    ].copy()

    pace_df["Lap Time (s)"] = pace_df["LapTime"].dt.total_seconds().round(3)

    pace_df.drop(columns="LapTime", inplace=True)

    pace_df.rename(
        columns={
            "LapNumber": "Lap Number",
            "TyreLife": "Tyre Life",
        },
        inplace=True,
    )

    pace_df = pace_df.sort_values(["Driver", "Lap Number"]).reset_index(drop=True)

    return pace_df


# Compound Comparison
@st.cache_data(show_spinner=False, ttl=3600)
def compound_comparison(_session):
    """
    Compare the performance of each tyre compound used during the race.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    # Convert lap times to seconds
    laps["Lap Time (s)"] = laps["LapTime"].dt.total_seconds()

    # Remove laps that are not representative of race pace
    laps = laps[laps["Lap Time (s)"] < 300].copy()

    compound_df = (
        laps.groupby("Compound")
        .agg(
            **{
                "Average Lap Time (s)": ("Lap Time (s)", "mean"),
                "Fastest Lap (s)": ("Lap Time (s)", "min"),
                "Average Tyre Life": ("TyreLife", "mean"),
                "Maximum Tyre Life": ("TyreLife", "max"),
                "Number of Laps": ("LapNumber", "count"),
                "Drivers Using Compound": ("Driver", "nunique"),
            }
        )
        .reset_index()
    )

    numeric_cols = [
        "Average Lap Time (s)",
        "Fastest Lap (s)",
        "Average Tyre Life",
    ]

    compound_df[numeric_cols] = compound_df[numeric_cols].round(3)

    compound_df = compound_df.sort_values(by="Average Lap Time (s)").reset_index(
        drop=True
    )

    return compound_df



