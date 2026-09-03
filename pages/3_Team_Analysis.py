import html

import pandas as pd
import streamlit as st

from src.analytics.driver_analysis import (
    driver_lap_analysis,
    format_lap_time,
)
from src.services.driver_service import get_driver_profile
from src.ui.session_selector import session_selector

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Team Analysis",
    page_icon=":material/flag:",
    layout="wide",
)


# ==========================================================
# GLOBAL STYLING
# ==========================================================

st.markdown(
    """
    <style>

    /* ======================================================
       PAGE
       ====================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       SECTION BANNER
       ====================================================== */

    .team-section-banner {
        position: relative;
        overflow: hidden;

        margin: 28px 0 26px 0;
        padding: 28px 34px;

        background:
            linear-gradient(
                105deg,
                #111c2b 0%,
                #111a28 60%,
                #17121f 100%
            );

        border: 1px solid #293548;
        border-radius: 18px;

        border-left: 6px solid #ff4058;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.18);
    }


    .team-section-number {
        position: absolute;

        right: 34px;
        top: 12px;

        font-size: 72px;
        line-height: 1;

        font-weight: 900;

        color: rgba(255,255,255,0.035);

        pointer-events: none;
    }


    .team-section-kicker {
        position: relative;
        z-index: 2;

        margin-bottom: 7px;

        color: #82a9d7;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 2.4px;
        text-transform: uppercase;
    }


    .team-section-title {
        position: relative;
        z-index: 2;

        color: #ffffff;

        font-size: 30px;
        font-weight: 850;

        line-height: 1.15;

        margin-bottom: 9px;
    }


    .team-section-description {
        position: relative;
        z-index: 2;

        color: #7898c0;

        font-size: 14px;

        line-height: 1.5;
    }


    /* ======================================================
       TEAM SELECTOR
       ====================================================== */

    .selector-label {
        color: #86a8d2;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 1.8px;
        text-transform: uppercase;

        margin-bottom: 8px;
    }


    /* ======================================================
       DRIVER COMPARISON
       ====================================================== */

    .driver-comparison {
        display: grid;

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 24px;

        margin-top: 8px;
        margin-bottom: 30px;
    }


    /* ======================================================
       DRIVER CARD
       ====================================================== */

    .driver-panel {
        position: relative;
        overflow: hidden;

        min-height: 475px;

        padding: 30px;

        background:
            linear-gradient(
                145deg,
                #151f2e 0%,
                #101823 100%
            );

        border: 1px solid #2b394d;

        border-radius: 20px;

        box-shadow:
            0 14px 35px rgba(0,0,0,0.18);
    }


    /* Red accent */
    .driver-panel::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 4px;

        background: #ff4058;

        border-radius:
            20px 0 0 20px;
    }


    /* Right-side image glow */
    .driver-panel::after {
        content: "";

        position: absolute;

        right: -80px;
        top: 20px;

        width: 330px;
        height: 330px;

        background:
            radial-gradient(
                circle,
                rgba(40,90,150,0.18) 0%,
                rgba(40,90,150,0.06) 40%,
                transparent 72%
            );

        pointer-events: none;
    }


    /* ======================================================
       DRIVER CONTENT
       ====================================================== */

    .driver-panel-content {
        position: relative;
        z-index: 5;

        width: 62%;
    }


    .driver-panel-name {
        color: #ffffff;

        font-size: 29px;
        font-weight: 900;

        line-height: 1;

        margin-bottom: 9px;
    }


    .driver-panel-team {
        color: #82a9d7;

        font-size: 11px;
        font-weight: 700;

        letter-spacing: 2px;

        text-transform: uppercase;

        margin-bottom: 28px;
    }


    /* ======================================================
       DRIVER IMAGE
       ====================================================== */

    .driver-panel-image {
        position: absolute;

        right: 0;
        bottom: 0;

        width: 43%;
        height: 100%;

        display: flex;

        align-items: flex-end;
        justify-content: center;

        z-index: 3;

        pointer-events: none;
    }


    .driver-panel-image img {
        display: block;

        width: 100%;
        max-width: 285px;

        height: auto;

        max-height: 430px;

        object-fit: contain;

        object-position: bottom center;

        filter:
            drop-shadow(
                0 18px 28px
                rgba(0,0,0,0.50)
            );
    }


    /* ======================================================
       DRIVER STAT ROW
       ====================================================== */

    .driver-stat {
        display: flex;

        align-items: center;
        justify-content: space-between;

        gap: 15px;

        padding: 11px 0;

        border-bottom:
            1px solid
            rgba(255,255,255,0.055);
    }


    .driver-stat-label {
        color: #7395bf;

        font-size: 12px;

        white-space: nowrap;
    }


    .driver-stat-value {
        color: #ffffff;

        font-size: 13px;
        font-weight: 800;

        text-align: right;

        white-space: nowrap;
    }


    /* ======================================================
       EMPTY / INFO CARD
       ====================================================== */

    .team-empty {
        padding: 30px;

        background: #121b29;

        border: 1px solid #293548;

        border-radius: 16px;

        color: #7898c0;

        text-align: center;
    }


    /* ======================================================
       TEAM SUMMARY CARDS
       ====================================================== */

    .summary-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 18px;

        margin-bottom: 25px;
    }


    .summary-card {
        position: relative;

        padding: 25px;

        background: #121b29;

        border: 1px solid #293548;

        border-radius: 16px;

        border-left: 4px solid #284d77;
    }


    .summary-label {
        color: #7898c0;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 1.7px;

        text-transform: uppercase;

        margin-bottom: 10px;
    }


    .summary-value {
        color: #ffffff;

        font-size: 27px;
        font-weight: 850;
    }


    /* ======================================================
       RESPONSIVE
       ====================================================== */

    @media (max-width: 900px) {

        .driver-comparison {
            grid-template-columns: 1fr;
        }

        .summary-grid {
            grid-template-columns: 1fr;
        }

        .driver-panel-content {
            width: 60%;
        }

        .driver-panel-image {
            width: 45%;
        }
    }


    @media (max-width: 600px) {

        .team-section-banner {
            padding: 24px;
        }

        .team-section-title {
            font-size: 24px;
        }

        .driver-panel {
            min-height: 430px;
            padding: 24px;
        }

        .driver-panel-content {
            width: 64%;
        }

        .driver-panel-image {
            width: 42%;
        }

        .driver-panel-image img {
            max-width: 220px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# HELPER - SECTION BANNER
# ==========================================================


def section_banner(
    number,
    kicker,
    title,
    description,
):
    st.html(f"""
        <div class="team-section-banner">

            <div class="team-section-number">
                {html.escape(str(number))}
            </div>

            <div class="team-section-kicker">
                {html.escape(str(kicker))}
            </div>

            <div class="team-section-title">
                {html.escape(str(title))}
            </div>

            <div class="team-section-description">
                {html.escape(str(description))}
            </div>

        </div>
        """)


# ==========================================================
# HELPER - SAFE VALUE
# ==========================================================


def safe_value(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    return value


# ==========================================================
# HELPER - FORMAT POSITION
# ==========================================================


def format_position(value):

    value = safe_value(value)

    if value is None:
        return "-"

    try:
        return f"P{int(float(value))}"
    except Exception:
        return str(value)


# ==========================================================
# HELPER - FORMAT POINTS
# ==========================================================


def format_points(value):

    value = safe_value(value)

    if value is None:
        return "-"

    try:
        return f"{float(value):g}"
    except Exception:
        return str(value)


# ==========================================================
# HELPER - FORMAT NUMBER
# ==========================================================


def format_number(value):

    value = safe_value(value)

    if value is None:
        return "-"

    try:
        return f"{float(value):g}"
    except Exception:
        return str(value)


# ==========================================================
# HELPER - DRIVER DATA
# ==========================================================


def get_driver_comparison_data(
    session,
    driver,
):
    """
    Build all comparison statistics for one driver.
    """

    results = session.results.copy()

    driver_results = results[
        results["Abbreviation"].astype(str).str.upper() == driver.upper()
    ]

    if driver_results.empty:
        return None

    result = driver_results.iloc[0]

    # ------------------------------------------------------
    # Basic race result
    # ------------------------------------------------------

    finish_position = safe_value(result.get("Position"))

    grid_position = safe_value(result.get("GridPosition"))

    points = safe_value(result.get("Points"))

    laps_completed = safe_value(result.get("Laps"))

    # ------------------------------------------------------
    # Lap analysis
    # ------------------------------------------------------

    try:
        laps = driver_lap_analysis(
            session,
            driver,
        )
    except Exception:
        laps = pd.DataFrame()

    average_lap = None
    fastest_lap = None

    if laps is not None and not laps.empty:

        if "Lap Time (s)" in laps.columns:

            valid_times = laps["Lap Time (s)"].dropna()

            if not valid_times.empty:

                average_lap = valid_times.mean()

                fastest_lap = valid_times.min()

    # ------------------------------------------------------
    # Position gain
    # ------------------------------------------------------

    positions_gained = None

    if grid_position is not None and finish_position is not None:
        try:
            positions_gained = float(grid_position) - float(finish_position)
        except Exception:
            positions_gained = None

    # ------------------------------------------------------
    # Team
    # ------------------------------------------------------

    team = result.get(
        "TeamName",
        "Unknown",
    )

    team = safe_value(team)

    if team is None:
        team = "Unknown"

    # ------------------------------------------------------
    # Driver profile / image
    # ------------------------------------------------------

    profile = None

    try:

        season = session.event["EventDate"].year

        profile = get_driver_profile(
            driver,
            season,
        )

    except Exception:
        profile = None

    image = None

    if profile:
        image = profile.get("image")

    return {
        "driver": driver.upper(),
        "team": str(team),
        "finish_position": finish_position,
        "grid_position": grid_position,
        "points": points,
        "laps_completed": laps_completed,
        "average_lap": average_lap,
        "fastest_lap": fastest_lap,
        "positions_gained": positions_gained,
        "image": image,
    }


# ==========================================================
# PAGE HEADER
# ==========================================================

st.html("""
    <div class="team-section-banner"
         style="
            border-left-color:#ff4058;
            margin-top:0;
         ">

        <div class="team-section-number">
            01
        </div>

        <div class="team-section-kicker">
            F1 RACE INTELLIGENCE
        </div>

        <div class="team-section-title">
            TEAM <span style="color:#ff4058;">
                ANALYSIS
            </span>
        </div>

        <div class="team-section-description">
            Compare teammate performance across
            race result, pace, positioning and points.
        </div>

    </div>
    """)


# ==========================================================
# SESSION SELECTION
# ==========================================================

with st.expander(
    "Session Selection",
    expanded=False,
):

    session = session_selector()


if session is None:

    st.info("Select a Season, Circuit and Session " "to begin team analysis.")

    st.stop()


# ==========================================================
# SESSION RESULTS
# ==========================================================

results = session.results.copy()

if results is None or results.empty:

    st.warning("Team comparison data is not available " "for this session.")

    st.stop()


# ==========================================================
# TEAM SELECTION
# ==========================================================

section_banner(
    "01",
    "TEAM SELECTION",
    "Choose a Team",
    "Select a constructor to compare its two drivers.",
)


team_column = None

if "TeamName" in results.columns:
    team_column = "TeamName"
elif "Team" in results.columns:
    team_column = "Team"


if team_column is None:

    st.error("Team information is not available " "in this session.")

    st.stop()


teams = (
    results[team_column].dropna().astype(str).drop_duplicates().sort_values().tolist()
)


if not teams:

    st.info("No teams are available for this session.")

    st.stop()


selected_team = st.selectbox(
    "Team",
    teams,
    label_visibility="collapsed",
)


# ==========================================================
# FIND TEAM DRIVERS
# ==========================================================

team_results = results[results[team_column].astype(str) == selected_team].copy()


if "Abbreviation" not in team_results.columns:

    st.error("Driver information is not available " "for this team.")

    st.stop()


team_drivers = (
    team_results["Abbreviation"]
    .dropna()
    .astype(str)
    .str.upper()
    .drop_duplicates()
    .tolist()
)


if len(team_drivers) < 2:

    st.warning(
        f"{selected_team} does not have " "two comparable drivers in this session."
    )

    st.stop()


# ==========================================================
# LIMIT TO TWO DRIVERS
# ==========================================================

driver_a = team_drivers[0]
driver_b = team_drivers[1]


# ==========================================================
# BUILD DRIVER DATA
# ==========================================================

data_a = get_driver_comparison_data(
    session,
    driver_a,
)

data_b = get_driver_comparison_data(
    session,
    driver_b,
)


if data_a is None or data_b is None:

    st.error("Unable to build teammate comparison " "for this session.")

    st.stop()


# ==========================================================
# TEAMMATE PERFORMANCE
# ==========================================================

section_banner(
    "02",
    "DRIVER COMPARISON",
    "Teammate Performance",
    "Compare the two drivers across race result, pace and points.",
)


# ==========================================================
# DRIVER CARD
# ==========================================================


def driver_card(data):

    image_html = ""

    if data["image"]:

        image_html = f"""
            <div class="driver-panel-image">

                <img
                    src="{html.escape(
                        str(data["image"])
                    )}"
                    alt="{html.escape(
                        data["driver"]
                    )}"
                    loading="lazy"
                >

            </div>
        """

    gained = data["positions_gained"]

    if gained is None:

        gained_text = "-"

    else:

        try:
            gained_text = f"{int(gained):+d}"
        except Exception:
            gained_text = str(gained)

    average_text = (
        format_lap_time(data["average_lap"]) if data["average_lap"] is not None else "-"
    )

    fastest_text = (
        format_lap_time(data["fastest_lap"]) if data["fastest_lap"] is not None else "-"
    )

    laps_text = format_number(data["laps_completed"])

    return f"""
        <div class="driver-panel">

            {image_html}

            <div class="driver-panel-content">

                <div class="driver-panel-name">
                    {html.escape(
                        data["driver"]
                    )}
                </div>

                <div class="driver-panel-team">
                    {html.escape(
                        data["team"]
                    )}
                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Finish Position
                    </span>

                    <span class="driver-stat-value">
                        {format_position(
                            data["finish_position"]
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Grid Position
                    </span>

                    <span class="driver-stat-value">
                        {format_position(
                            data["grid_position"]
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Points
                    </span>

                    <span class="driver-stat-value">
                        {format_points(
                            data["points"]
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Average Lap
                    </span>

                    <span class="driver-stat-value">
                        {html.escape(
                            average_text
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Fastest Lap
                    </span>

                    <span class="driver-stat-value">
                        {html.escape(
                            fastest_text
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Positions Gained
                    </span>

                    <span class="driver-stat-value">
                        {html.escape(
                            gained_text
                        )}
                    </span>

                </div>


                <div class="driver-stat">

                    <span class="driver-stat-label">
                        Laps Completed
                    </span>

                    <span class="driver-stat-value">
                        {html.escape(
                            laps_text
                        )}
                    </span>

                </div>

            </div>

        </div>
    """


# ==========================================================
# RENDER BOTH DRIVER CARDS
# ==========================================================

st.html(f"""
    <div class="driver-comparison">

        {driver_card(data_a)}

        {driver_card(data_b)}

    </div>
    """)


# ==========================================================
# TEAM SUMMARY
# ==========================================================

section_banner(
    "03",
    "TEAM SNAPSHOT",
    "Combined Performance",
    "A quick view of how the two teammates performed together.",
)


# ----------------------------------------------------------
# Combined points
# ----------------------------------------------------------

points_a = data_a["points"]
points_b = data_b["points"]

combined_points = None

if points_a is not None and points_b is not None:

    try:
        combined_points = float(points_a) + float(points_b)
    except Exception:
        combined_points = None


# ----------------------------------------------------------
# Best finish
# ----------------------------------------------------------

finish_a = data_a["finish_position"]
finish_b = data_b["finish_position"]

best_finish = None

valid_finishes = []

for value in [
    finish_a,
    finish_b,
]:

    value = safe_value(value)

    if value is not None:

        try:
            valid_finishes.append(float(value))
        except Exception:
            pass


if valid_finishes:
    best_finish = min(valid_finishes)


# ----------------------------------------------------------
# Pace difference
# ----------------------------------------------------------

pace_difference = None

if data_a["average_lap"] is not None and data_b["average_lap"] is not None:

    pace_difference = abs(data_a["average_lap"] - data_b["average_lap"])


# ==========================================================
# SUMMARY CARDS
# ==========================================================

combined_points_text = (
    format_points(combined_points) if combined_points is not None else "-"
)

best_finish_text = format_position(best_finish) if best_finish is not None else "-"

pace_difference_text = (
    f"{pace_difference:.3f} s" if pace_difference is not None else "-"
)


st.html(f"""
    <div class="summary-grid">

        <div class="summary-card">

            <div class="summary-label">
                Combined Points
            </div>

            <div class="summary-value">
                {combined_points_text}
            </div>

        </div>


        <div class="summary-card">

            <div class="summary-label">
                Best Team Finish
            </div>

            <div class="summary-value">
                {best_finish_text}
            </div>

        </div>


        <div class="summary-card">

            <div class="summary-label">
                Teammate Pace Gap
            </div>

            <div class="summary-value">
                {pace_difference_text}
            </div>

        </div>

    </div>
    """)



