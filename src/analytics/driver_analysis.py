import pandas as pd
import streamlit as st


def _session_cache_key(session):
    """Generate a cache key from session metadata."""
    if session is None:
        return "none"
    event = session.event
    return f"{event['EventDate'].year}_{event['EventName']}_{session.name}"


# Helper Functions
def _get_valid_laps(session):
    """
    Return a copy of all laps with a valid lap time.
    """
    laps = session.laps.copy()

    laps = laps[
        laps["LapTime"].notna()
    ].copy()

    return laps


def _convert_lap_time(laps):
    """
    Add lap time in seconds.
    """
    laps = laps.copy()

    laps["Lap Time (s)"] = laps["LapTime"].dt.total_seconds()

    return laps


def _convert_sector_times(laps):
    """
    Add sector times in seconds.
    """
    laps = laps.copy()

    laps["Sector 1 (s)"] = laps["Sector1Time"].dt.total_seconds()
    laps["Sector 2 (s)"] = laps["Sector2Time"].dt.total_seconds()
    laps["Sector 3 (s)"] = laps["Sector3Time"].dt.total_seconds()

    return laps


# Driver Summary
@st.cache_data(show_spinner=False, ttl=3600)
def driver_summary(_session):
    """
    Generate a summary of each driver's race performance.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)
    laps = _convert_lap_time(laps)

    results = _session.results.copy()

    summary = (
        laps.groupby("Driver")
        .agg(
            Team=("Team", "first"),
            **{
                "Average Lap Time (s)": ("Lap Time (s)", "mean"),
                "Fastest Lap Time (s)": ("Lap Time (s)", "min"),
                "Median Lap Time (s)": ("Lap Time (s)", "median"),
                "Lap Time Std Dev (s)": ("Lap Time (s)", "std"),
                "Total Valid Laps": ("LapNumber", "count"),
                "Pit Stops": ("Stint", lambda x: max(x.nunique() - 1, 0)),
            },
        )
        .reset_index()
    )

    positions = (
        results[
            [
                "Abbreviation",
                "GridPosition",
                "Position",
            ]
        ]
        .rename(
            columns={
                "Abbreviation": "Driver",
                "GridPosition": "Start Position",
                "Position": "Finish Position",
            }
        )
    )

    summary = summary.merge(
        positions,
        on="Driver",
        how="left",
    )

    summary = summary.sort_values(
        by="Finish Position"
    ).reset_index(drop=True)

    numeric_cols = [
        "Average Lap Time (s)",
        "Fastest Lap Time (s)",
        "Median Lap Time (s)",
        "Lap Time Std Dev (s)",
    ]

    summary[numeric_cols] = summary[numeric_cols].round(3)

    return summary


# Sector Analysis
@st.cache_data(show_spinner=False, ttl=3600)
def sector_analysis(_session):
    """
    Calculate average sector times for each driver.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    laps = laps.dropna(
        subset=[
            "Sector1Time",
            "Sector2Time",
            "Sector3Time",
        ]
    )

    laps = _convert_sector_times(laps)

    sector_df = (
        laps.groupby("Driver")
        .agg(
            Team=("Team", "first"),
            **{
                "Average Sector 1 (s)": ("Sector 1 (s)", "mean"),
                "Average Sector 2 (s)": ("Sector 2 (s)", "mean"),
                "Average Sector 3 (s)": ("Sector 3 (s)", "mean"),
            },
        )
        .reset_index()
    )

    numeric_cols = [
        "Average Sector 1 (s)",
        "Average Sector 2 (s)",
        "Average Sector 3 (s)",
    ]

    sector_df[numeric_cols] = sector_df[numeric_cols].round(3)

    return sector_df

# Speed Analysis
@st.cache_data(show_spinner=False, ttl=3600)
def speed_analysis(_session):
    """
    Calculate average and maximum speed statistics for each driver.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    speed_df = (
        laps.groupby("Driver")
        .agg(
            Team=("Team", "first"),
            **{
                "Average Speed I1 (km/h)": ("SpeedI1", "mean"),
                "Average Speed I2 (km/h)": ("SpeedI2", "mean"),
                "Average Finish Line Speed (km/h)": ("SpeedFL", "mean"),
                "Average Speed Trap (km/h)": ("SpeedST", "mean"),
                "Maximum Speed Trap (km/h)": ("SpeedST", "max"),
            },
        )
        .reset_index()
    )

    numeric_cols = [
        "Average Speed I1 (km/h)",
        "Average Speed I2 (km/h)",
        "Average Finish Line Speed (km/h)",
        "Average Speed Trap (km/h)",
        "Maximum Speed Trap (km/h)",
    ]

    speed_df[numeric_cols] = speed_df[numeric_cols].round(2)

    return speed_df

# Driver Report
def driver_report(session, driver):
    """
    Generate a complete report for a single driver.

    Parameters
    ----------
    session : fastf1.core.Session

    driver : str
        Driver abbreviation (e.g. 'NOR', 'VER', 'HAM')

    Returns
    -------
    pandas.Series
    """

    summary = driver_summary(session)
    sectors = sector_analysis(session)
    speeds = speed_analysis(session)

    report = (
        summary
        .merge(sectors, on=["Driver", "Team"])
        .merge(speeds, on=["Driver", "Team"])
    )

    report = report[
        report["Driver"] == driver.upper()
    ]

    if report.empty:
        raise ValueError(
            f"No data found for driver '{driver}'."
        )

    return report.squeeze()


# Position Changes
@st.cache_data(show_spinner=False, ttl=3600)
def position_changes(_session):
    """
    Calculate how many positions each driver gained or lost
    during the race.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    summary = driver_summary(_session).copy()

    summary["Positions Gained"] = (
        summary["Start Position"] -
        summary["Finish Position"]
    )

    position_df = summary[
        [
            "Driver",
            "Team",
            "Start Position",
            "Finish Position",
            "Positions Gained",
        ]
    ].copy()

    position_df = position_df.sort_values(
        by="Positions Gained",
        ascending=False
    ).reset_index(drop=True)

    return position_df


# Tyre Usage Analysis
@st.cache_data(show_spinner=False, ttl=3600)
def tyre_usage(_session):
    """
    Analyze tyre usage for every driver.

    Parameters
    ----------
    _session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    laps = _get_valid_laps(_session)

    tyre_df = (
        laps.groupby("Driver")
        .agg(
            Team=("Team", "first"),

            Compounds=("Compound",
                       lambda x: ", ".join(sorted(x.dropna().unique()))),

            Number_of_Stints=("Stint", "nunique"),

            Average_Tyre_Life=("TyreLife", "mean"),

            Maximum_Tyre_Life=("TyreLife", "max"),

            Fresh_Tyre_Start=(
                "FreshTyre",
                lambda x: bool(x.any())
            ),
        )
        .reset_index()
    )

    tyre_df.rename(
        columns={
            "Compounds": "Compounds Used",
            "Number_of_Stints": "Number of Stints",
            "Average_Tyre_Life": "Average Tyre Life",
            "Maximum_Tyre_Life": "Maximum Tyre Life",
            "Fresh_Tyre_Start": "Started on Fresh Tyres",
        },
        inplace=True,
    )

    tyre_df[
        [
            "Average Tyre Life",
            "Maximum Tyre Life",
        ]
    ] = tyre_df[
        [
            "Average Tyre Life",
            "Maximum Tyre Life",
        ]
    ].round(2)

    return tyre_df

# ==========================================================
# Individual Driver Lap Analysis
# ==========================================================


def driver_lap_analysis(session, driver):
    """
    Return lap-by-lap performance data for one driver.
    """

    laps = _get_valid_laps(session)

    driver_laps = laps[laps["Driver"] == driver.upper()].copy()

    if driver_laps.empty:
        return pd.DataFrame()

    driver_laps = _convert_lap_time(driver_laps)

    driver_laps = driver_laps.sort_values(by="LapNumber")

    columns = [
        "LapNumber",
        "LapTime",
        "Lap Time (s)",
        "Compound",
        "TyreLife",
        "Stint",
    ]

    # Only keep columns that actually exist
    columns = [column for column in columns if column in driver_laps.columns]

    return driver_laps[columns]


def format_lap_time(seconds):
    """
    Convert lap time in seconds to M:SS.mmm format.
    """

    if seconds is None:
        return "-"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    return f"{minutes}:{remaining_seconds:06.3f}"



