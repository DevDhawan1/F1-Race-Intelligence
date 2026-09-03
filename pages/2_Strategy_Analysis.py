import html

import pandas as pd
import streamlit as st

from src.analytics.strategy_analysis import (
    stint_analysis,
    tyre_degradation,
    pit_stop_analysis,
    race_pace_evolution,
    compound_comparison,
)

from src.ui.session_selector import session_selector

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Strategy Analysis",
    page_icon=":material/tire_repair:",
    layout="wide",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GENERAL
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       SECTION HEADER
       ===================================================== */

    .strategy-section-header {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                110deg,
                #101927 0%,
                #111a29 55%,
                #17131e 100%
            );

        border: 1px solid #293344;
        border-radius: 18px;

        padding: 28px 38px;

        margin-top: 35px;
        margin-bottom: 28px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.18);
    }


    .strategy-section-header::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 5px;

        background: #ff4054;
    }


    .strategy-section-number {
        position: absolute;

        right: 28px;
        top: 12px;

        font-size: 70px;
        font-weight: 900;

        color: rgba(255,255,255,0.025);

        line-height: 1;
    }


    .strategy-section-kicker {
        font-size: 12px;
        font-weight: 800;

        letter-spacing: 3px;

        color: #82a9d8;

        margin-bottom: 8px;

        text-transform: uppercase;
    }


    .strategy-section-title {
        font-size: 30px;
        font-weight: 850;

        color: #ffffff;

        line-height: 1.15;

        margin-bottom: 8px;
    }


    .strategy-section-description {
        font-size: 14px;

        color: #7793b8;

        line-height: 1.5;
    }


    /* =====================================================
       SUMMARY CARDS
       ===================================================== */

    .strategy-card {
        position: relative;

        background:
            linear-gradient(
                145deg,
                #121b29,
                #101721
            );

        border: 1px solid #263243;

        border-radius: 16px;

        padding: 25px 26px;

        min-height: 145px;

        overflow: hidden;
    }


    .strategy-card::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 4px;

        background: #4fd65c;
    }


    .strategy-card-label {
        font-size: 11px;
        font-weight: 800;

        letter-spacing: 2px;

        text-transform: uppercase;

        color: #7fa1c9;

        margin-bottom: 20px;
    }


    .strategy-card-value {
        font-size: 34px;
        font-weight: 850;

        color: #ffffff;

        line-height: 1;
    }


    .strategy-card-unit {
        font-size: 12px;

        color: #7894b8;

        margin-left: 6px;
    }


    /* =====================================================
       TYRE COMPOUND COLORS
       ===================================================== */

    .compound-medium {
        background: linear-gradient(
            135deg,
            #ffd52e,
            #e8b900
        );

        color: #151515;
    }


    .compound-hard {
        background: linear-gradient(
            135deg,
            #e1e6ec,
            #adb8c6
        );

        color: #121820;
    }


    .compound-soft {
        background: linear-gradient(
            135deg,
            #ff5368,
            #e52540
        );

        color: #ffffff;
    }


    .compound-intermediate {
        background: linear-gradient(
            135deg,
            #45d66b,
            #159c43
        );

        color: #ffffff;
    }


    .compound-wet {
        background: linear-gradient(
            135deg,
            #36a9ff,
            #176ac0
        );

        color: #ffffff;
    }


    /* =====================================================
       STINT TIMELINE
       ===================================================== */

    .stint-timeline {
        display: flex;

        width: 100%;

        height: 105px;

        border-radius: 15px;

        overflow: hidden;

        border: 1px solid #273244;

        background: #111823;

        margin-bottom: 28px;
    }


    .timeline-stint {
        display: flex;

        flex-direction: column;

        justify-content: center;

        align-items: center;

        text-align: center;

        min-width: 55px;

        border-right: 2px solid #10151d;

        font-weight: 800;

        position: relative;
    }


    .timeline-compound {
        font-size: 13px;

        letter-spacing: 2px;

        text-transform: uppercase;
    }


    .timeline-laps {
        font-size: 11px;

        margin-top: 7px;

        opacity: 0.75;
    }


    /* =====================================================
       STINT CARDS
       ===================================================== */

    .stint-card {
        background: #121b27;

        border: 1px solid #283445;

        border-radius: 15px;

        overflow: hidden;

        min-height: 170px;
    }


    .stint-card-top {
        padding: 11px 18px;

        font-size: 12px;

        font-weight: 900;

        letter-spacing: 2px;

        text-transform: uppercase;
    }


    .stint-card-body {
        padding: 20px;
    }


    .stint-card-laps {
        font-size: 27px;

        font-weight: 850;

        color: #ffffff;
    }


    .stint-card-laps span {
        font-size: 11px;

        font-weight: 600;

        color: #7894b8;

        margin-left: 5px;
    }


    .stint-card-range {
        margin-top: 10px;

        color: #6f8db3;

        font-size: 12px;
    }


    /* =====================================================
       PIT STOP CARDS
       ===================================================== */

    .pit-card {
        background: #121b27;

        border: 1px solid #293548;

        border-radius: 15px;

        padding: 22px;

        min-height: 150px;
    }


    .pit-number {
        font-size: 11px;

        letter-spacing: 2px;

        font-weight: 800;

        color: #ff5264;

        margin-bottom: 12px;
    }


    .pit-lap {
        font-size: 28px;

        font-weight: 850;

        color: #ffffff;
    }


    .pit-transition {
        margin-top: 10px;

        font-size: 13px;

        color: #88a4c8;
    }


    /* =====================================================
       INSIGHT BOX
       ===================================================== */

    .strategy-insight {
        background:
            linear-gradient(
                135deg,
                #121d2b,
                #111822
            );

        border: 1px solid #293649;

        border-left: 4px solid #ff4054;

        border-radius: 15px;

        padding: 25px 28px;

        color: #b2c3da;

        line-height: 1.7;
    }


    .strategy-insight strong {
        color: #ffffff;
    }


    /* =====================================================
       TABLE
       ===================================================== */

    .strategy-table-title {
        font-size: 18px;

        font-weight: 800;

        color: #ffffff;

        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# HELPER: SECTION HEADER
# ==========================================================


def section_header(
    number,
    kicker,
    title,
    description,
):
    st.html(f"""
        <div class="strategy-section-header">

            <div class="strategy-section-number">
                {number:02d}
            </div>

            <div class="strategy-section-kicker">
                {html.escape(kicker)}
            </div>

            <div class="strategy-section-title">
                {html.escape(title)}
            </div>

            <div class="strategy-section-description">
                {html.escape(description)}
            </div>

        </div>
        """)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.html("""
    <div class="strategy-section-header"
         style="margin-top:0;">

        <div class="strategy-section-kicker">
            F1 RACE INTELLIGENCE
        </div>

        <div class="strategy-section-title">
            Strategy Analysis
        </div>

        <div class="strategy-section-description">
            Understand tyre usage, stint progression,
            degradation and strategic decisions.
        </div>

    </div>
    """)


# ==========================================================
# SESSION SELECTION
# ==========================================================

with st.expander(
    ":material/settings: Session Selection",
    expanded=False,
):
    session = session_selector()


if session is None:

    st.info("Select a Season, Circuit and Session " "to begin strategy analysis.")

    st.stop()


# ==========================================================
# LOAD ANALYTICS
# ==========================================================

try:
    stints = stint_analysis(session)
except Exception:
    stints = pd.DataFrame()

try:
    degradation = tyre_degradation(session)
except Exception:
    degradation = pd.DataFrame()

try:
    pit_stops = pit_stop_analysis(session)
except Exception:
    pit_stops = pd.DataFrame()

try:
    pace = race_pace_evolution(session)
except Exception:
    pace = pd.DataFrame()

try:
    compounds = compound_comparison(session)
except Exception:
    compounds = pd.DataFrame()


# ==========================================================
# 01 - STRATEGY OVERVIEW
# ==========================================================

section_header(
    1,
    "RACE STRATEGY",
    "Strategy Overview",
    "A high-level view of tyre usage and strategic decisions.",
)


# Number of stints across the session
number_of_stints = (
    stints["Stint"].nunique() if not stints.empty and "Stint" in stints.columns else 0
)

number_of_pit_stops = len(pit_stops) if not pit_stops.empty else 0

number_of_compounds = (
    compounds["Compound"].nunique()
    if not compounds.empty and "Compound" in compounds.columns
    else 0
)

total_laps = (
    int(degradation["Lap Number"].max())
    if not degradation.empty and "Lap Number" in degradation.columns
    else 0
)


c1, c2, c3, c4 = st.columns(4)


with c1:
    st.html(f"""
        <div class="strategy-card">
            <div class="strategy-card-label">
                Total Stints
            </div>

            <div class="strategy-card-value">
                {number_of_stints}
            </div>
        </div>
        """)


with c2:
    st.html(f"""
        <div class="strategy-card">
            <div class="strategy-card-label">
                Pit Stops
            </div>

            <div class="strategy-card-value">
                {number_of_pit_stops}
            </div>
        </div>
        """)


with c3:
    st.html(f"""
        <div class="strategy-card">
            <div class="strategy-card-label">
                Compounds Used
            </div>

            <div class="strategy-card-value">
                {number_of_compounds}
            </div>
        </div>
        """)


with c4:
    st.html(f"""
        <div class="strategy-card">
            <div class="strategy-card-label">
                Race Laps
            </div>

            <div class="strategy-card-value">
                {total_laps}
            </div>
        </div>
        """)


# ==========================================================
# 02 - STINT STRATEGY
# ==========================================================

section_header(
    2,
    "TYRE STRATEGY",
    "Stint Strategy",
    "Tyre compound progression throughout the session.",
)


# ----------------------------------------------------------
# Select driver
# ----------------------------------------------------------

if not stints.empty:

    drivers = sorted(stints["Driver"].dropna().unique().tolist())

    selected_driver = st.selectbox(
        "Driver",
        drivers,
        key="strategy_driver",
    )

    driver_stints = stints[stints["Driver"] == selected_driver].copy()

else:

    selected_driver = None
    driver_stints = pd.DataFrame()


# ----------------------------------------------------------
# Timeline + Stint Cards (fragment for independent rerun)
# ----------------------------------------------------------

@st.fragment
def render_stint_strategy(driver_stints):
    if driver_stints.empty:
        return

    # Timeline
    timeline_parts = []
    total_driver_laps = driver_stints["Stint Length"].sum()

    compound_classes = {
        "MEDIUM": "compound-medium",
        "HARD": "compound-hard",
        "SOFT": "compound-soft",
        "INTERMEDIATE": "compound-intermediate",
        "WET": "compound-wet",
    }

    for _, stint in driver_stints.iterrows():
        compound = str(stint["Compound"]).upper()
        stint_length = int(stint["Stint Length"])
        width = stint_length / total_driver_laps * 100 if total_driver_laps else 100
        css_class = compound_classes.get(compound, "compound-hard")

        timeline_parts.append(f"""
            <div class="timeline-stint {css_class}" style="width:{width}%">
                <div class="timeline-compound">{html.escape(compound)}</div>
                <div class="timeline-laps">L{int(stint["Start Lap"])} → L{int(stint["End Lap"])}</div>
            </div>
        """)

    st.html(f'<div class="stint-timeline">{"".join(timeline_parts)}</div>')

    # Stint cards
    stint_columns = st.columns(min(len(driver_stints), 3))
    for index, (_, stint) in enumerate(driver_stints.iterrows()):
        compound = str(stint["Compound"]).upper()
        css_class = compound_classes.get(compound, "compound-hard")

        with stint_columns[index % len(stint_columns)]:
            st.html(f"""
                <div class="stint-card">
                    <div class="stint-card-top {css_class}">{html.escape(compound)}</div>
                    <div class="stint-card-body">
                        <div class="stint-card-laps">{int(stint["Stint Length"])} <span>LAPS</span></div>
                        <div class="stint-card-range">Laps {int(stint["Start Lap"])} – {int(stint["End Lap"])}</div>
                    </div>
                </div>
            """)


render_stint_strategy(driver_stints)


# ==========================================================
# 03 - TYRE PERFORMANCE
# ==========================================================

section_header(
    3,
    "COMPOUND PERFORMANCE",
    "Tyre Performance",
    "Compare race pace and tyre longevity across compounds.",
)


if compounds.empty:

    st.info("Compound performance data is not available.")

else:

    display_compounds = compounds.copy()

    if "Average Lap Time (s)" in display_compounds:
        display_compounds["Average Lap Time"] = display_compounds[
            "Average Lap Time (s)"
        ].apply(lambda x: f"{x:.3f} s")

    if "Fastest Lap (s)" in display_compounds:
        display_compounds["Fastest Lap"] = display_compounds["Fastest Lap (s)"].apply(
            lambda x: f"{x:.3f} s"
        )

    display_columns = [
        "Compound",
        "Average Lap Time",
        "Fastest Lap",
        "Average Tyre Life",
        "Maximum Tyre Life",
        "Number of Laps",
        "Drivers Using Compound",
    ]

    display_columns = [
        column for column in display_columns if column in display_compounds.columns
    ]

    st.dataframe(
        display_compounds[display_columns],
        width="stretch",
        hide_index=True,
    )


# ==========================================================
# 04 - TYRE DEGRADATION
# ==========================================================

section_header(
    4,
    "TYRE PERFORMANCE",
    "Tyre Degradation",
    "Understand how lap pace changes as tyre life increases.",
)


if degradation.empty:

    st.info("Tyre degradation data is not available.")

else:

    degradation_driver = st.selectbox(
        "Driver",
        sorted(degradation["Driver"].dropna().unique().tolist()),
        key="degradation_driver",
    )

    driver_degradation = degradation[degradation["Driver"] == degradation_driver].copy()

    chart_data = driver_degradation[
        [
            "Tyre Life",
            "Lap Time (s)",
        ]
    ].dropna()

    if not chart_data.empty:

        chart_data = (
            chart_data.groupby("Tyre Life")["Lap Time (s)"].mean().reset_index()
        )

        chart_data = chart_data.set_index("Tyre Life")

        st.line_chart(
            chart_data,
            x_label="Tyre Life",
            y_label="Lap Time (seconds)",
        )


# ==========================================================
# 05 - PIT STOP ANALYSIS
# ==========================================================

section_header(
    5,
    "STRATEGIC DECISIONS",
    "Pit Stop Analysis",
    "Understand when and how the driver changed compounds.",
)


@st.fragment
def render_pit_stops(pit_stops, selected_driver):
    if pit_stops.empty:
        st.info("No pit-stop transitions were identified for this session.")
        return

    driver_pits = pit_stops[pit_stops["Driver"] == selected_driver].copy()

    if driver_pits.empty:
        st.info("No pit stops were recorded for the selected driver.")
        return

    pit_columns = st.columns(min(len(driver_pits), 3))

    for index, (_, pit) in enumerate(driver_pits.iterrows()):
        with pit_columns[index % len(pit_columns)]:
            old_compound = str(pit["Old Compound"]).upper()
            new_compound = str(pit["New Compound"]).upper()

            st.html(f"""
                <div class="pit-card">
                    <div class="pit-number">PIT STOP {int(pit["Pit Stop"])}</div>
                    <div class="pit-lap">LAP {int(pit["Pit Lap"])}</div>
                    <div class="pit-transition">{html.escape(old_compound)} → {html.escape(new_compound)}</div>
                </div>
            """)


if not pit_stops.empty:
    render_pit_stops(pit_stops, selected_driver)
else:
    st.info("No pit-stop transitions were identified for this session.")


# ==========================================================
# 06 - RACE PACE
# ==========================================================

section_header(
    6,
    "RACE PACE",
    "Pace Evolution",
    "Track how lap performance changed throughout the race.",
)


if pace.empty:

    st.info("Race pace data is not available.")

else:

    pace_driver = st.selectbox(
        "Driver",
        sorted(pace["Driver"].dropna().unique().tolist()),
        key="pace_driver",
    )

    driver_pace = pace[pace["Driver"] == pace_driver].copy()

    chart_data = driver_pace[
        [
            "Lap Number",
            "Lap Time (s)",
        ]
    ].dropna()

    if not chart_data.empty:

        chart_data = chart_data.set_index("Lap Number")

        st.line_chart(
            chart_data,
            x_label="Lap",
            y_label="Lap Time (seconds)",
        )


# ==========================================================
# 07 - STRATEGY INSIGHT
# ==========================================================

section_header(
    7,
    "RACE READ",
    "Strategy Insight",
    "A concise interpretation of the selected driver's race strategy.",
)


if not driver_stints.empty:

    compounds_used = [
        str(compound).upper() for compound in driver_stints["Compound"].tolist()
    ]

    strategy_text = " → ".join(compounds_used)

    longest_stint = driver_stints.loc[driver_stints["Stint Length"].idxmax()]

    longest_compound = str(longest_stint["Compound"]).upper()

    longest_length = int(longest_stint["Stint Length"])

    st.html(f"""
        <div class="strategy-insight">

            <strong>Strategy:</strong>
            {html.escape(strategy_text)}
            <br><br>

            <strong>Key finding:</strong>
            The longest stint was completed on the
            <strong>{html.escape(longest_compound)}</strong>
            compound, lasting
            <strong>{longest_length} laps</strong>.

        </div>
        """)



