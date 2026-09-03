import html
import pandas as pd
import streamlit as st

from src.analytics.driver_analysis import (
    driver_lap_analysis,
    format_lap_time,
    speed_analysis,
    sector_analysis,
    position_changes,
    tyre_usage,
)

from src.services.driver_service import (
    get_driver_profile,
    get_session_driver_stats,
)

from src.ui.components.driver_card import driver_card
from src.ui.driver_selector import driver_selector
from src.ui.session_selector import session_selector

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Driver Analysis",
    page_icon=":material/person:",
    layout="wide",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GENERAL PAGE
       ====================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       MAIN HEADER
       ====================================================== */

    .driver-page-header {
        position: relative;

        padding: 38px 42px;

        margin-bottom: 36px;

        border-radius: 22px;

        background:
            radial-gradient(
                circle at 85% 30%,
                rgba(255, 70, 85, 0.18),
                transparent 35%
            ),
            linear-gradient(
                110deg,
                #09111f,
                #111827,
                #241018
            );

        border: 1px solid rgba(255,255,255,0.10);

        overflow: hidden;
    }


    .driver-page-header::after {
        content: "";

        position: absolute;

        right: -90px;
        top: -120px;

        width: 350px;
        height: 350px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(255,70,85,0.12),
                transparent 68%
            );

        pointer-events: none;
    }


    .driver-header-kicker {
        color: #8ea5c3;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 3px;

        margin-bottom: 9px;
    }


    .driver-header-title {
        color: #ffffff;

        font-size: 38px;

        font-weight: 850;

        line-height: 1.1;

        margin-bottom: 12px;
    }


    .driver-header-title span {
        color: #ff4655;
    }


    .driver-header-description {
        color: #8c9bb0;

        font-size: 14px;

        line-height: 1.6;

        max-width: 720px;
    }


/* ==========================================================
   SECTION HEADER BANNERS
   ========================================================== */

.section-banner {
    position: relative;

    margin-top: 42px;
    margin-bottom: 24px;

    padding: 28px 32px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #121b2a 0%,
            #101722 65%,
            #121923 100%
        );

    border: 1px solid rgba(255,255,255,0.09);

    overflow: hidden;
}


/* F1 RED SECTION ACCENT */

.section-banner::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 5px;

    background: #ff4655;
}


/* subtle background glow */

.section-banner::after {
    content: "";

    position: absolute;

    right: -80px;
    top: -100px;

    width: 280px;
    height: 280px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,70,85,0.08),
            transparent 70%
        );

    pointer-events: none;
}


/* kicker */

.section-banner-kicker {
    position: relative;

    z-index: 1;

    color: #8da7c8;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 8px;
}


/* main title */

.section-banner-title {
    position: relative;

    z-index: 1;

    color: #ffffff;

    font-size: 27px;

    font-weight: 850;

    line-height: 1.15;

    margin: 0;
}


/* description */

.section-banner-description {
    position: relative;

    z-index: 1;

    color: #8193ad;

    font-size: 13px;

    line-height: 1.5;

    margin-top: 9px;

    max-width: 700px;
}


/* section number */

.section-banner-number {
    position: absolute;

    right: 28px;
    top: 50%;

    transform: translateY(-50%);

    color: rgba(255,255,255,0.035);

    font-size: 72px;

    font-weight: 900;

    line-height: 1;

    pointer-events: none;
}

    /* ======================================================
       METRIC CARDS
       ====================================================== */

    [data-testid="stMetric"] {
        position: relative;

        background:
            linear-gradient(
                145deg,
                #151d2a,
                #10161f
            ) !important;

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 16px;

        padding: 22px 24px;

        min-height: 125px;

        overflow: hidden;
    }


    [data-testid="stMetric"]::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 4px;

        background: #2d8cff;
    }


    [data-testid="stMetricLabel"] {
        color: #8fa5c2 !important;

        font-size: 10px !important;

        font-weight: 800 !important;

        letter-spacing: 1.5px !important;

        text-transform: uppercase;
    }


    [data-testid="stMetricValue"] {
        color: #ffffff !important;

        font-size: 30px !important;

        font-weight: 850 !important;
    }


    /* ======================================================
       ANALYSIS HEADER
       ====================================================== */

    .analysis-header {
        margin-top: 25px;

        margin-bottom: 14px;

        padding: 20px 24px;

        border-radius: 15px;

        background:
            linear-gradient(
                110deg,
                #111927,
                #121923
            );

        border: 1px solid rgba(255,255,255,0.07);
    }


    .analysis-title {
        color: #ffffff;

        font-size: 17px;

        font-weight: 800;
    }


    .analysis-subtitle {
        color: #71839d;

        font-size: 12px;

        margin-top: 5px;
    }


    /* ======================================================
       TYRE STRATEGY
       ====================================================== */

    .strategy-timeline {
        display: flex;

        width: 100%;

        height: 92px;

        border-radius: 14px;

        overflow: hidden;

        border: 1px solid rgba(255,255,255,0.08);

        margin: 25px 0 22px 0;
    }


    .strategy-stint {
        display: flex;

        flex-direction: column;

        align-items: center;

        justify-content: center;

        min-width: 70px;

        border-right: 2px solid #0d1118;

        color: #10141b;

        font-weight: 900;

        text-align: center;
    }


    .strategy-stint:last-child {
        border-right: none;
    }


    .strategy-compound {
        font-size: 13px;

        letter-spacing: 1px;
    }


    .strategy-laps {
        font-size: 11px;

        margin-top: 7px;

        opacity: 0.8;
    }


    .compound-soft {
        background: linear-gradient(
            180deg,
            #ff5265,
            #e51e38
        );
    }


    .compound-medium {
        background: linear-gradient(
            180deg,
            #ffda3d,
            #efbf00
        );
    }


    .compound-hard {
        background: linear-gradient(
            180deg,
            #d9e0e8,
            #aab5c2
        );
    }


    .compound-intermediate {
        background: linear-gradient(
            180deg,
            #57d66a,
            #25a943
        );
    }


    .compound-wet {
        background: linear-gradient(
            180deg,
            #42a5ff,
            #1471c9
        );

        color: white;
    }


    .stint-card {
        background:
            linear-gradient(
                145deg,
                #141c28,
                #10161f
            );

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 15px;

        overflow: hidden;

        margin-bottom: 18px;
    }


    .stint-card-header {
        padding: 10px 18px;

        font-size: 11px;

        font-weight: 900;

        letter-spacing: 1.5px;
    }


    .stint-card-body {
        padding: 20px;
    }


    .stint-value {
        color: #ffffff;

        font-size: 27px;

        font-weight: 800;
    }


    .stint-label {
        color: #71839d;

        font-size: 10px;

        text-transform: uppercase;

        letter-spacing: 1px;

        margin-left: 5px;
    }


    .stint-range {
        color: #71839d;

        font-size: 12px;

        margin-top: 8px;
    }

/* ======================================================
   SPEED ANALYSIS
   ====================================================== */

.speed-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 16px;

    margin-top: 24px;
    margin-bottom: 35px;
}


/* ------------------------------------------------------
   SPEED CARD
   ------------------------------------------------------ */

.speed-card {
    position: relative;

    min-height: 145px;

    padding: 24px 22px 24px 27px;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            #172335,
            #111a28
        );

    border: 1px solid rgba(83,130,184,0.24);

    overflow: hidden;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}


/* F1 red accent */

.speed-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background: #2d8cff;
}


/* subtle glow */

.speed-card::after {
    content: "";

    position: absolute;

    width: 110px;
    height: 110px;

    right: -55px;
    bottom: -55px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(59,130,246,0.10),
            transparent 70%
        );

    pointer-events: none;
}


.speed-card:hover {

    transform: translateY(-3px);

    border-color: rgba(45,140,255,0.48);

    box-shadow: 0 10px 28px rgba(0,0,0,0.22);
}

/* ==========================================================
   SECTOR ANALYSIS
   ========================================================== */

.sector-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 16px;

    margin-top: 24px;

    margin-bottom: 35px;
}


.sector-card {
    position: relative;

    min-height: 155px;

    padding: 25px 26px 25px 31px;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            #172335,
            #111a28
        );

    border: 1px solid rgba(83,130,184,0.24);

    overflow: hidden;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}


.sector-card::before {
    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 4px;

    background: #2d8cff;
}


.sector-card:hover {

    transform: translateY(-3px);

    border-color: rgba(45,140,255,0.48);

    box-shadow: 0 10px 28px rgba(0,0,0,0.22);
}


.sector-card-label {

    color: #8fa5c2;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-bottom: 20px;
}


.sector-card-value {

    color: #ffffff;

    font-size: 31px;

    font-weight: 850;

    line-height: 1;
}


.sector-card-value span {

    color: #71839d;

    font-size: 12px;

    font-weight: 700;

    margin-left: 5px;
}


.sector-card-caption {

    color: #62738c;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 1.3px;

    margin-top: 17px;
}


@media (max-width: 700px) {

    .sector-grid {

        grid-template-columns:
            repeat(1, minmax(0, 1fr));

    }

}

/* ------------------------------------------------------
   LABEL
   ------------------------------------------------------ */

.speed-card-label {

    color: #8fa5c2;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.5px;

    line-height: 1.4;

    text-transform: uppercase;

    margin-bottom: 20px;
}


/* ------------------------------------------------------
   VALUE
   ------------------------------------------------------ */

.speed-card-value {

    color: #ffffff;

    font-size: 27px;

    font-weight: 850;

    line-height: 1.1;

    white-space: nowrap;
}


.speed-card-value span {

    margin-left: 5px;

    color: #71839d;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 0.5px;
}


/* ======================================================
   RESPONSIVE SPEED GRID
   ====================================================== */

@media (max-width: 1200px) {

    .speed-grid {

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

    }

}


@media (max-width: 700px) {

    .speed-grid {

        grid-template-columns:
            repeat(1, minmax(0, 1fr));

    }

}
    /* ======================================================
       FOOTER
       ====================================================== */

    .driver-footer {
        margin-top: 60px;

        padding-top: 20px;

        border-top: 1px solid rgba(255,255,255,0.08);

        color: #65758d;

        font-size: 10px;

        text-align: center;

        letter-spacing: 1.5px;
    }


    /* ======================================================
       EXPANDER
       ====================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 14px;

        background: #10161f;
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
        <div class="section-banner">

            <div class="section-banner-number">
                {number}
            </div>

            <div class="section-banner-kicker">
                {kicker}
            </div>

            <div class="section-banner-title">
                {title}
            </div>

            <div class="section-banner-description">
                {description}
            </div>

        </div>
        """)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.html("""
    <div class="driver-page-header">

        <div class="driver-header-kicker">
            F1 RACE INTELLIGENCE
        </div>

        <div class="driver-header-title">
            DRIVER <span>ANALYSIS</span>
        </div>

        <div class="driver-header-description">
            Detailed session-level performance, pace,
            positioning and race strategy analysis.
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

    st.info("Select a Season, Circuit and Session " "to begin driver analysis.")

    st.stop()


# ==========================================================
# DRIVER SELECTION
# ==========================================================

driver = driver_selector(session)


if driver is None:

    st.info("Select a driver to continue.")

    st.stop()


# ==========================================================
# DRIVER PROFILE
# ==========================================================

season = session.event["EventDate"].year

profile = get_driver_profile(
    driver,
    season,
)


section_banner(
    "01",
    "DRIVER PROFILE",
    "Driver Overview",
    "Driver identity, team and championship information.",
)


driver_card(profile)


# ==========================================================
# SESSION STATISTICS
# ==========================================================

section_banner(
    "02",
    "SESSION PERFORMANCE",
    "Session Statistics",
    "Key results from the selected session.",
)


session_stats = get_session_driver_stats(
    session,
    driver,
)


if session_stats is None:

    st.info("No session results are available " "for this driver.")

else:

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        position = session_stats.get("position")

        st.metric(
            "Session Position",
            position if position is not None else "-",
        )

    with c2:

        grid_position = session_stats.get("grid_position")

        st.metric(
            "Grid Position",
            grid_position if grid_position is not None else "-",
        )

    with c3:

        points = session_stats.get("points")

        st.metric(
            "Session Points",
            points if points is not None else "-",
        )

    with c4:

        completed_laps = session_stats.get("laps")

        st.metric(
            "Laps Completed",
            completed_laps if completed_laps is not None else "-",
        )


# ==========================================================
# LAP PACE ANALYSIS
# ==========================================================

section_banner(
    "03",
    "RACE PACE",
    "Lap Pace Analysis",
    "Analyse consistency and outright pace across every completed lap.",
)


laps = driver_lap_analysis(
    session,
    driver,
)


if laps.empty:

    st.info("Lap timing data is not available " "for this driver in this session.")

else:

    # ------------------------------------------------------
    # LAP METRICS
    # ------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Laps Analysed",
            len(laps),
        )

    with c2:

        fastest = laps["Lap Time (s)"].min()

        st.metric(
            "Fastest Lap",
            format_lap_time(fastest),
        )

    with c3:

        average = laps["Lap Time (s)"].mean()

        st.metric(
            "Average Lap",
            format_lap_time(average),
        )

    # ------------------------------------------------------
    # LAP PACE CHART
    # ------------------------------------------------------

    st.html("""
        <div class="analysis-header">

            <div class="analysis-title">
                Lap-by-Lap Pace
            </div>

            <div class="analysis-subtitle">
                Lap time variation throughout the session
            </div>

        </div>
        """)

    chart_data = laps[
        [
            "LapNumber",
            "Lap Time (s)",
        ]
    ].copy()

    chart_data = chart_data.set_index("LapNumber")

    st.line_chart(
        chart_data,
        x_label="Lap",
        y_label="Lap Time (seconds)",
    )

    # ------------------------------------------------------
    # LAP DATA
    # ------------------------------------------------------

    st.html("""
        <div class="analysis-header">

            <div class="analysis-title">
                Lap Data
            </div>

            <div class="analysis-subtitle">
                Detailed lap timing and tyre information
            </div>

        </div>
        """)

    display_laps = laps.copy()

    display_laps["Lap Time"] = display_laps["Lap Time (s)"].apply(format_lap_time)

    display_columns = [
        "LapNumber",
        "Lap Time",
        "Compound",
        "TyreLife",
        "Stint",
    ]

    display_columns = [
        column for column in display_columns if column in display_laps.columns
    ]

    st.dataframe(
        display_laps[display_columns],
        width="stretch",
        hide_index=True,
    )


# ==========================================================
# SPEED ANALYSIS
# ==========================================================

section_banner(
    "04",
    "STRAIGHT-LINE PERFORMANCE",
    "Speed Analysis",
    "Compare speed performance across the circuit's key speed measurement points.",
)

speed_df = speed_analysis(session)

if speed_df.empty:

    st.info("Speed data is not available for this session.")

else:

    driver_speed = speed_df[speed_df["Driver"] == driver.upper()]

    if driver_speed.empty:

        st.info("Speed data is not available for this driver.")

    else:

        speed = driver_speed.iloc[0]

        # ==================================================
        # SPEED CARDS
        # ==================================================

        speed_metrics = [
            (
                "AVERAGE SPEED I1",
                speed.get("Average Speed I1 (km/h)"),
            ),
            (
                "AVERAGE SPEED I2",
                speed.get("Average Speed I2 (km/h)"),
            ),
            (
                "FINISH LINE SPEED",
                speed.get("Average Finish Line Speed (km/h)"),
            ),
            (
                "AVERAGE SPEED TRAP",
                speed.get("Average Speed Trap (km/h)"),
            ),
            (
                "MAXIMUM SPEED TRAP",
                speed.get("Maximum Speed Trap (km/h)"),
            ),
        ]

        speed_cards_html = ""

        for label, value in speed_metrics:

            if value is None or pd.isna(value):

                value_html = "-"

            else:

                value_html = f"""
                    {float(value):.2f}
                    <span>km/h</span>
                """

            speed_cards_html += f"""
                <div class="speed-card">

                    <div class="speed-card-label">
                        {html.escape(label)}
                    </div>

                    <div class="speed-card-value">
                        {value_html}
                    </div>

                </div>
            """

        st.html(f"""
            <div class="speed-grid">

                {speed_cards_html}

            </div>
            """)

# ==========================================================
# SECTOR ANALYSIS
# ==========================================================

section_banner(
    "05",
    "TRACK SECTORS",
    "Sector Performance",
    "Compare the driver's average pace through each circuit sector.",
)

sector_df = sector_analysis(session)

if sector_df.empty:

    st.info("Sector timing data is not available " "for this session.")

else:

    driver_sector = sector_df[sector_df["Driver"] == driver.upper()]

    if driver_sector.empty:

        st.info("Sector timing data is not available " "for this driver.")

    else:

        sector = driver_sector.iloc[0]

        sector_metrics = [
            (
                "SECTOR 1",
                sector.get("Average Sector 1 (s)"),
            ),
            (
                "SECTOR 2",
                sector.get("Average Sector 2 (s)"),
            ),
            (
                "SECTOR 3",
                sector.get("Average Sector 3 (s)"),
            ),
        ]

        sector_cards_html = ""

        for label, value in sector_metrics:

            if value is None or pd.isna(value):

                value_text = "-"

            else:

                value_text = f"""
                    {float(value):.3f}
                    <span>sec</span>
                """

            sector_cards_html += f"""
                <div class="sector-card">

                    <div class="sector-card-label">
                        {label}
                    </div>

                    <div class="sector-card-value">
                        {value_text}
                    </div>

                    <div class="sector-card-caption">
                        AVERAGE SECTOR TIME
                    </div>

                </div>
            """

        st.html(f"""
            <div class="sector-grid">

                {sector_cards_html}

            </div>
            """)

# ==========================================================
# POSITION ANALYSIS
# ==========================================================

section_banner(
    "05",
    "RACE PROGRESSION",
    "Position Analysis",
    "Understand how the driver's starting position translated into the final result.",
)


position_df = position_changes(session)


if position_df.empty:

    st.info("Position data is not available " "for this session.")

else:

    driver_position = position_df[position_df["Driver"] == driver.upper()]

    if driver_position.empty:

        st.info("Position data is not available " "for this driver.")

    else:

        position_data = driver_position.iloc[0]

        starting = position_data.get("Start Position")

        finishing = position_data.get("Finish Position")

        gained = position_data.get("Positions Gained")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Starting Position",
                (f"{starting:g}" if pd.notna(starting) else "-"),
            )

        with c2:

            st.metric(
                "Finishing Position",
                (f"{finishing:g}" if pd.notna(finishing) else "-"),
            )

        with c3:

            st.metric(
                "Positions Gained",
                (f"{gained:+g}" if pd.notna(gained) else "-"),
            )

        # --------------------------------------------------
        # POSITION SUMMARY
        # --------------------------------------------------

        if pd.notna(gained):

            if gained > 0:

                position_message = (
                    f"The driver gained {int(gained)} "
                    f"position{'s' if gained != 1 else ''} "
                    f"during the session."
                )

            elif gained < 0:

                lost = abs(int(gained))

                position_message = (
                    f"The driver lost {lost} "
                    f"position{'s' if lost != 1 else ''} "
                    f"during the session."
                )

            else:

                position_message = (
                    "The driver finished in the same "
                    "position as their starting position."
                )

            st.html(f"""
    <div class="analysis-header">

        <div class="analysis-title">
            Race Progression
        </div>

        <div class="analysis-subtitle">
            {html.escape(position_message)}
        </div>

    </div>
    """)


# ==========================================================
# TYRE STRATEGY
# ==========================================================

section_banner(
    "06",
    "RACE STRATEGY",
    "Tyre Strategy",
    "Detailed breakdown of tyre compounds, stint lengths and tyre usage.",
)


tyre_df = tyre_usage(session)


if tyre_df.empty:

    st.info("Tyre strategy data is not available " "for this session.")

else:

    driver_tyre = tyre_df[tyre_df["Driver"] == driver.upper()]

    if driver_tyre.empty:

        st.info("Tyre strategy data is not available " "for this driver.")

    else:

        tyre_data = driver_tyre.iloc[0]

        # --------------------------------------------------
        # TYRE SUMMARY
        # --------------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Number of Stints",
                tyre_data.get(
                    "Number of Stints",
                    "-",
                ),
            )

        with c2:

            average_life = tyre_data.get("Average Tyre Life")

            st.metric(
                "Average Tyre Life",
                (f"{average_life:.1f} laps" if pd.notna(average_life) else "-"),
            )

        with c3:

            max_life = tyre_data.get("Maximum Tyre Life")

            st.metric(
                "Maximum Tyre Life",
                (f"{max_life:.0f} laps" if pd.notna(max_life) else "-"),
            )

        # --------------------------------------------------
        # FRESH TYRE
        # --------------------------------------------------

        fresh_tyres = tyre_data.get("Started on Fresh Tyres")

        if pd.notna(fresh_tyres):

            fresh_text = "YES" if bool(fresh_tyres) else "NO"

            fresh_colour = "#57e35f" if bool(fresh_tyres) else "#ff4655"

            st.html(f"""
                <div style="
                    margin-top:20px;
                    padding:20px 24px;
                    border-radius:15px;
                    background:#121a25;
                    border:1px solid rgba(255,255,255,0.08);
                    border-left:4px solid {fresh_colour};
                ">

                    <div style="
                        color:#8fa5c2;
                        font-size:10px;
                        font-weight:800;
                        letter-spacing:1.5px;
                    ">
                        STARTED ON FRESH TYRES
                    </div>

                    <div style="
                        color:{fresh_colour};
                        font-size:28px;
                        font-weight:850;
                        margin-top:7px;
                    ">
                        {fresh_text}
                    </div>

                </div>
                """)

        # ==================================================
        # STINT STRATEGY
        # ==================================================

        st.html("""
            <div class="analysis-header">

                <div class="analysis-title">
                    Stint Strategy
                </div>

                <div class="analysis-subtitle">
                    Tyre compound progression throughout the session
                </div>

            </div>
            """)

        # --------------------------------------------------
        # BUILD STINT DATA FROM LAP DATA
        # --------------------------------------------------

        if not laps.empty and "Compound" in laps.columns:

            stint_source = laps.copy()

            if "Stint" in stint_source.columns:

                stint_source = stint_source.dropna(subset=["Compound"]).sort_values(
                    ["Stint", "LapNumber"]
                )

                stint_rows = []

                for stint_number, group in stint_source.groupby("Stint"):

                    if group.empty:
                        continue

                    compound = str(group["Compound"].dropna().iloc[0]).upper()

                    start_lap = int(group["LapNumber"].min())

                    end_lap = int(group["LapNumber"].max())

                    lap_count = len(group)

                    stint_rows.append(
                        {
                            "stint": int(stint_number),
                            "compound": compound,
                            "start": start_lap,
                            "end": end_lap,
                            "laps": lap_count,
                        }
                    )

                # ------------------------------------------
                # TIMELINE
                # ------------------------------------------

                if stint_rows:

                    total_laps = sum(item["laps"] for item in stint_rows)

                    timeline_html = '<div class="strategy-timeline">'

                    for item in stint_rows:

                        width = item["laps"] / total_laps * 100

                        compound_lower = item["compound"].lower()

                        if "MEDIUM" in item["compound"]:

                            compound_class = "compound-medium"

                        elif "HARD" in item["compound"]:

                            compound_class = "compound-hard"

                        elif "SOFT" in item["compound"]:

                            compound_class = "compound-soft"

                        elif "INTERMEDIATE" in item["compound"]:

                            compound_class = "compound-intermediate"

                        elif "WET" in item["compound"]:

                            compound_class = "compound-wet"

                        else:

                            compound_class = "compound-hard"

                        timeline_html += f"""
                        <div
                            class="strategy-stint {compound_class}"
                            style="width:{width:.2f}%"
                        >

                            <div class="strategy-compound">
                                {html.escape(
                                    item["compound"]
                                )}
                            </div>

                            <div class="strategy-laps">
                                {item["start"]}
                                →
                                {item["end"]}
                            </div>

                        </div>
                        """

                    timeline_html += "</div>"

                    st.html(timeline_html)

                    # --------------------------------------
                    # STINT CARDS
                    # --------------------------------------

                    card_columns = st.columns(len(stint_rows))

                    for column, item in zip(
                        card_columns,
                        stint_rows,
                    ):

                        compound = item["compound"]

                        if "MEDIUM" in compound:

                            header_bg = "linear-gradient(" "90deg,#ffda3d,#efbf00)"

                        elif "HARD" in compound:

                            header_bg = "linear-gradient(" "90deg,#d9e0e8,#aab5c2)"

                        elif "SOFT" in compound:

                            header_bg = "linear-gradient(" "90deg,#ff5265,#e51e38)"

                        elif "INTERMEDIATE" in compound:

                            header_bg = "linear-gradient(" "90deg,#57d66a,#25a943)"

                        else:

                            header_bg = "linear-gradient(" "90deg,#42a5ff,#1471c9)"

                        with column:

                            st.html(f"""
                                <div class="stint-card">

                                    <div
                                        class="stint-card-header"
                                        style="
                                            background:
                                            {header_bg};
                                            color:#10141b;
                                        "
                                    >
                                        {html.escape(
                                            compound
                                        )}
                                    </div>

                                    <div class="stint-card-body">

                                        <div>
                                            <span class="stint-value">
                                                {item["laps"]}
                                            </span>

                                            <span class="stint-label">
                                                laps
                                            </span>
                                        </div>

                                        <div class="stint-range">
                                            Laps {item["start"]}
                                            →
                                            {item["end"]}
                                        </div>

                                    </div>

                                </div>
                                """)

                else:

                    st.info("Detailed stint data is not available " "for this driver.")

        else:

            st.info("Detailed tyre stint data is not available " "for this session.")


# ==========================================================
# FOOTER
# ==========================================================

st.html("""
    <div class="driver-footer">
        F1 RACE INTELLIGENCE · DRIVER PERFORMANCE ANALYTICS
    </div>
    """)



