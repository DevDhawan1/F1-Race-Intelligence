import pandas as pd
import streamlit as st
from src.utils.lap_filters import remove_outlier_laps


def _session_cache_key(session):
    """Generate a cache key from session metadata."""
    if session is None:
        return "none"
    event = session.event
    return f"{event['EventDate'].year}_{event['EventName']}_{session.name}"


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================


def _get_valid_laps(session):
    """
    Return laps with a valid lap time.
    """

    if session is None or session.laps is None:
        return pd.DataFrame()

    laps = session.laps.copy()

    if laps.empty:
        return pd.DataFrame()

    laps = laps[laps["LapTime"].notna()].copy()

    laps["Lap Time (s)"] = laps["LapTime"].dt.total_seconds()

    return laps


def _get_clean_race_laps(session):
    """
    Return valid laps with obvious outlier laps removed.
    """

    laps = _get_valid_laps(session)

    if laps.empty:
        return laps

    try:
        laps = remove_outlier_laps(laps)
    except Exception:
        pass

    return laps


def _clean_numeric(value):
    """
    Convert a value to float where possible.
    """

    try:
        if pd.isna(value):
            return None

        return float(value)

    except (TypeError, ValueError):
        return None


# ==========================================================
# TEAM SUMMARY
# ==========================================================


@st.cache_data(show_spinner=False, ttl=3600)
def team_summary(_session):
    """
    Generate a high-level summary for every team.

    Returns
    -------
    pandas.DataFrame

    Columns include:
        Team
        Drivers
        Number of Drivers
        Combined Points
        Best Finish
        Average Finish
        Combined Laps
    """

    if _session is None or _session.results is None or _session.results.empty:
        return pd.DataFrame()

    results = _session.results.copy()

    required_columns = [
        "Abbreviation",
        "TeamName",
        "Position",
        "Points",
        "Laps",
    ]

    available_columns = [
        column for column in required_columns if column in results.columns
    ]

    results = results[available_columns].copy()

    # ------------------------------------------------------
    # Normalise team column
    # ------------------------------------------------------

    if "TeamName" not in results.columns:
        return pd.DataFrame()

    results = results.rename(
        columns={
            "TeamName": "Team",
        }
    )

    # ------------------------------------------------------
    # Make numeric result columns safe
    # ------------------------------------------------------

    for column in [
        "Position",
        "Points",
        "Laps",
    ]:
        if column in results.columns:

            results[column] = pd.to_numeric(
                results[column],
                errors="coerce",
            )

    # ------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------

    summary = (
        results.groupby("Team")
        .agg(
            Drivers=(
                "Abbreviation",
                lambda x: ", ".join(x.dropna().astype(str)),
            ),
            **{
                "Number of Drivers": (
                    "Abbreviation",
                    "nunique",
                ),
                "Combined Points": (
                    "Points",
                    "sum",
                ),
                "Best Finish": (
                    "Position",
                    "min",
                ),
                "Average Finish": (
                    "Position",
                    "mean",
                ),
                "Combined Laps": (
                    "Laps",
                    "sum",
                ),
            }
        )
        .reset_index()
    )

    summary["Average Finish"] = summary["Average Finish"].round(2)

    summary = summary.sort_values(
        by=[
            "Combined Points",
            "Best Finish",
        ],
        ascending=[
            False,
            True,
        ],
    ).reset_index(drop=True)

    return summary


# ==========================================================
# TEAMMATE COMPARISON
# ==========================================================


@st.cache_data(show_spinner=False, ttl=3600)
def teammate_comparison(_session, team):
    """
    Compare drivers from the selected team.

    Returns one row per driver containing race result,
    pace and position-change information.
    """

    laps = _get_clean_race_laps(_session)

    if laps.empty:
        return pd.DataFrame()

    team_laps = laps[laps["Team"] == team].copy()

    if team_laps.empty:
        return pd.DataFrame()

    # ------------------------------------------------------
    # Pace statistics
    # ------------------------------------------------------

    pace = (
        team_laps.groupby("Driver")
        .agg(
            **{
                "Average Lap Time (s)": (
                    "Lap Time (s)",
                    "mean",
                ),
                "Median Lap Time (s)": (
                    "Lap Time (s)",
                    "median",
                ),
                "Fastest Lap Time (s)": (
                    "Lap Time (s)",
                    "min",
                ),
                "Lap Time Std Dev (s)": (
                    "Lap Time (s)",
                    "std",
                ),
                "Valid Laps": (
                    "LapNumber",
                    "count",
                ),
            }
        )
        .reset_index()
    )

    # ------------------------------------------------------
    # Session results
    # ------------------------------------------------------

    results = _session.results.copy()

    result_columns = [
        "Abbreviation",
        "GridPosition",
        "Position",
        "Points",
        "Laps",
        "Status",
    ]

    result_columns = [column for column in result_columns if column in results.columns]

    results = results[result_columns].copy()

    results = results.rename(
        columns={
            "Abbreviation": "Driver",
            "GridPosition": "Grid Position",
            "Position": "Finish Position",
            "Points": "Points",
            "Laps": "Laps Completed",
            "Status": "Status",
        }
    )

    comparison = pace.merge(
        results,
        on="Driver",
        how="left",
    )

    # ------------------------------------------------------
    # Position change
    # ------------------------------------------------------

    if (
        "Grid Position" in comparison.columns
        and "Finish Position" in comparison.columns
    ):

        comparison["Positions Gained"] = pd.to_numeric(
            comparison["Grid Position"],
            errors="coerce",
        ) - pd.to_numeric(
            comparison["Finish Position"],
            errors="coerce",
        )

    # ------------------------------------------------------
    # Round pace values
    # ------------------------------------------------------

    pace_columns = [
        "Average Lap Time (s)",
        "Median Lap Time (s)",
        "Fastest Lap Time (s)",
        "Lap Time Std Dev (s)",
    ]

    for column in pace_columns:

        if column in comparison.columns:

            comparison[column] = comparison[column].round(3)

    if "Finish Position" in comparison.columns:

        comparison = comparison.sort_values(by="Finish Position").reset_index(drop=True)

    return comparison


# ==========================================================
# TEAM PACE COMPARISON
# ==========================================================


@st.cache_data(show_spinner=False, ttl=3600)
def team_pace_comparison(_session, team):
    """
    Return lap-by-lap pace for drivers from one team.

    Intended for teammate pace charts.
    """

    laps = _get_clean_race_laps(_session)

    if laps.empty:
        return pd.DataFrame()

    team_laps = laps[laps["Team"] == team].copy()

    if team_laps.empty:
        return pd.DataFrame()

    columns = [
        "Driver",
        "Team",
        "LapNumber",
        "Lap Time (s)",
        "Compound",
        "TyreLife",
        "Stint",
    ]

    columns = [column for column in columns if column in team_laps.columns]

    pace_df = team_laps[columns].copy()

    pace_df = pace_df.rename(
        columns={
            "LapNumber": "Lap Number",
            "TyreLife": "Tyre Life",
        }
    )

    pace_df["Lap Time (s)"] = pace_df["Lap Time (s)"].round(3)

    pace_df = pace_df.sort_values(
        by=[
            "Lap Number",
            "Driver",
        ]
    ).reset_index(drop=True)

    return pace_df


# ==========================================================
# TEAM TYRE STRATEGY
# ==========================================================


@st.cache_data(show_spinner=False, ttl=3600)
def team_tyre_strategy(_session, team):
    """
    Return stint strategy for both drivers from a team.
    """

    laps = _get_valid_laps(_session)

    if laps.empty:
        return pd.DataFrame()

    team_laps = laps[laps["Team"] == team].copy()

    if team_laps.empty:
        return pd.DataFrame()

    strategy = (
        team_laps.groupby(
            [
                "Driver",
                "Team",
                "Stint",
            ]
        )
        .agg(
            Compound=(
                "Compound",
                "first",
            ),
            **{
                "Start Lap": (
                    "LapNumber",
                    "min",
                ),
                "End Lap": (
                    "LapNumber",
                    "max",
                ),
                "Stint Length": (
                    "LapNumber",
                    "count",
                ),
                "Average Tyre Life": (
                    "TyreLife",
                    "mean",
                ),
            }
        )
        .reset_index()
    )

    strategy["Average Tyre Life"] = strategy["Average Tyre Life"].round(2)

    strategy = strategy.sort_values(
        by=[
            "Driver",
            "Stint",
        ]
    ).reset_index(drop=True)

    return strategy


# ==========================================================
# TEAM PERFORMANCE
# ==========================================================


@st.cache_data(show_spinner=False, ttl=3600)
def team_performance(_session, team):
    """
    Generate overall performance statistics for one team.

    Returns
    -------
    dict
    """

    comparison = teammate_comparison(
        _session,
        team,
    )

    if comparison.empty:
        return None

    # ------------------------------------------------------
    # Drivers
    # ------------------------------------------------------

    drivers = comparison["Driver"].dropna().astype(str).tolist()

    # ------------------------------------------------------
    # Combined points
    # ------------------------------------------------------

    combined_points = None

    if "Points" in comparison.columns:

        points = pd.to_numeric(
            comparison["Points"],
            errors="coerce",
        )

        combined_points = points.sum()

    # ------------------------------------------------------
    # Best finish
    # ------------------------------------------------------

    best_finish = None

    if "Finish Position" in comparison.columns:

        positions = pd.to_numeric(
            comparison["Finish Position"],
            errors="coerce",
        )

        if positions.notna().any():
            best_finish = positions.min()

    # ------------------------------------------------------
    # Combined completed laps
    # ------------------------------------------------------

    combined_laps = None

    if "Laps Completed" in comparison.columns:

        completed = pd.to_numeric(
            comparison["Laps Completed"],
            errors="coerce",
        )

        combined_laps = completed.sum()

    # ------------------------------------------------------
    # Best team lap
    # ------------------------------------------------------

    best_lap = None

    if "Fastest Lap Time (s)" in comparison.columns:

        fastest = pd.to_numeric(
            comparison["Fastest Lap Time (s)"],
            errors="coerce",
        )

        if fastest.notna().any():
            best_lap = fastest.min()

    # ------------------------------------------------------
    # Average team pace
    # ------------------------------------------------------

    average_team_pace = None

    if "Average Lap Time (s)" in comparison.columns:

        averages = pd.to_numeric(
            comparison["Average Lap Time (s)"],
            errors="coerce",
        )

        if averages.notna().any():
            average_team_pace = averages.mean()

    # ------------------------------------------------------
    # Teammate pace delta
    # ------------------------------------------------------

    pace_delta = None
    faster_driver = None
    slower_driver = None

    if len(comparison) >= 2 and "Average Lap Time (s)" in comparison.columns:

        pace_rows = comparison[
            [
                "Driver",
                "Average Lap Time (s)",
            ]
        ].dropna()

        if len(pace_rows) >= 2:

            pace_rows = pace_rows.sort_values(by="Average Lap Time (s)")

            faster = pace_rows.iloc[0]
            slower = pace_rows.iloc[-1]

            faster_driver = faster["Driver"]
            slower_driver = slower["Driver"]

            pace_delta = float(slower["Average Lap Time (s)"]) - float(
                faster["Average Lap Time (s)"]
            )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {
        "team": team,
        "drivers": drivers,
        "combined_points": (
            round(
                float(combined_points),
                2,
            )
            if combined_points is not None
            else None
        ),
        "best_finish": (
            int(best_finish)
            if best_finish is not None and not pd.isna(best_finish)
            else None
        ),
        "combined_laps": (
            int(combined_laps)
            if combined_laps is not None and not pd.isna(combined_laps)
            else None
        ),
        "best_lap_seconds": (
            round(
                float(best_lap),
                3,
            )
            if best_lap is not None
            else None
        ),
        "average_team_pace_seconds": (
            round(
                float(average_team_pace),
                3,
            )
            if average_team_pace is not None
            else None
        ),
        "pace_delta_seconds": (
            round(
                float(pace_delta),
                3,
            )
            if pace_delta is not None
            else None
        ),
        "faster_driver": faster_driver,
        "slower_driver": slower_driver,
    }



