import html

import pandas as pd
import streamlit as st

from src.ui.session_selector import session_selector
from src.services.driver_service import get_driver_profile
from src.analytics.driver_analysis import format_lap_time
from src.ui.circuit_map import create_circuit_map
from src.utils.formatters import format_lap_time as fmt_lap_time, format_duration

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="F1 Race Intelligence",
    page_icon=":material/directions_car:",
    layout="wide",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.html("""
    <style>

    /* ======================================================
       PROJECT BANNER
       ====================================================== */

    .project-banner {
        width: 100%;
        box-sizing: border-box;

        padding: 32px 70px;
        min-height: 150px;

        margin-bottom: 45px;

        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.15);

        background:
            radial-gradient(
                circle at 85% 50%,
                rgba(255,55,70,0.20),
                transparent 40%
            ),
            linear-gradient(
                110deg,
                #07101e 0%,
                #111827 55%,
                #42131d 100%
            );

        display: flex;
        align-items: center;

        box-shadow:
            0 15px 40px rgba(0,0,0,0.20);
    }


    .project-logo {
        display: flex;
        align-items: center;
        gap: 30px;
    }


    .project-icon {
        font-size: 42px;
        line-height: 1;
        display: inline-flex;
        align-items: center;
        color: #ffffff;
    }

    .project-icon svg {
        width: 48px;
        height: 48px;
        display: block;
        fill: currentColor;
    }


    .project-title {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -1.5px;
        color: white;
    }


    .project-title span {
        color: #ff4b55;
    }


    .project-subtitle {
        margin-top: 14px;

        font-size: 15px;
        font-weight: 600;

        letter-spacing: 8px;

        color: rgba(255,255,255,0.55);
    }


    /* ======================================================
       SESSION SELECTION
       ====================================================== */

    .section-subtitle {
        color: rgba(255,255,255,0.55);
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 20px;
    }


    /* ======================================================
       CURRENTLY LOADED SESSION
       ====================================================== */

    .loaded-session {
        margin-top: 15px;

        padding: 28px;

        border-radius: 20px;

        border: 1px solid rgba(255,255,255,0.12);

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.035),
                rgba(255,255,255,0.015)
            );
    }


    .loaded-label {
        color: rgba(255,255,255,0.50);

        font-size: 14px;
        font-weight: 600;

        text-transform: uppercase;
        letter-spacing: 2px;

        margin-bottom: 10px;
    }


    .loaded-title {
        color: white;

        font-size: 34px;
        font-weight: 750;

        margin-bottom: 6px;
    }


    .loaded-location {
        color: rgba(255,255,255,0.60);

        font-size: 16px;

        margin-bottom: 28px;
    }


    .session-info-grid {
        display: grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap: 14px;
    }


    .session-info {
        padding: 18px;

        border-radius: 14px;

        background: rgba(255,255,255,0.035);

        border: 1px solid rgba(255,255,255,0.08);
    }


    .session-info-label {
        font-size: 13px;

        color: rgba(255,255,255,0.50);

        margin-bottom: 7px;
    }


    .session-info-value {
        font-size: 25px;

        color: white;

        font-weight: 650;
    }


    /* ======================================================
       TRACK CARD
       ====================================================== */


    .track-card {
    min-height: 200px;

    border-radius: 20px;

    border: 1px solid rgba(255, 255, 255, 0.12);

    background:
        radial-gradient(
            circle at 80% 15%,
            rgba(255, 75, 85, 0.16),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            #101827,
            #17191f
        );

    padding: 15px;

    box-sizing: border-box;

    display: flex;

    flex-direction: column;

    align-items: center;

    text-align: center;
}


.track-header {
    width: 100%;
}


.track-title {
    font-size: 30px;

    font-weight: 800;

    color: #ffffff;

    margin-top: 4px;
}


.track-subtitle {
    font-size: 16px;

    color: #9ca3af;

    margin-top: 8px;
}


.track-map {
    width: 100%;

    flex: 1;

    display: flex;

    align-items: center;

    justify-content: center;

    margin-top: 15px;
}


.track-map img {
    width: 90%;

    max-width: 430px;

    max-height: 280px;

    object-fit: contain;
}


.track-map-empty {
    flex: 1;

    display: flex;

    align-items: center;

    justify-content: center;

    color: #6b7280;

    font-size: 15px;
}


    .track-icon {
        font-size: 55px;
        margin-bottom: 12px;
    }


    .track-title {
        font-size: 30px;

        font-weight: 750;

        color: white;
    }


    .track-subtitle {
        margin-top: 7px;

        font-size: 15px;

        color: rgba(255,255,255,0.55);
    }


    /* ==========================================================
   PODIUM
   ========================================================== */

.podium-container {
    width: 100%;

    display: grid;

    grid-template-columns: 1fr 1.15fr 1fr;

    align-items: end;

    gap: 28px;

    margin-top: 45px;

    padding: 0 20px 0 20px;

    box-sizing: border-box;
}


/* ----------------------------------------------------------
   Individual podium item
   ---------------------------------------------------------- */

.podium-item {

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: flex-end;

    text-align: center;

    min-width: 0;
}


/* ----------------------------------------------------------
   Position
   ---------------------------------------------------------- */

.podium-position {

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 10px;

    margin-bottom: 14px;
}


.podium-medal {

    font-size: 30px;

    line-height: 1;
}


.podium-position-text {

    font-size: 30px;

    font-weight: 800;

    color: #ffffff;
}


/* ----------------------------------------------------------
   Driver card
   ---------------------------------------------------------- */

.podium-driver {

    width: 100%;

    min-height: 410px;

    border: 1px solid rgba(255, 255, 255, 0.12);

    border-radius: 18px 18px 0 0;

    background:
        linear-gradient(
            180deg,
            rgba(30, 33, 42, 0.98),
            rgba(18, 20, 27, 0.98)
        );

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: flex-end;

    overflow: hidden;

    box-sizing: border-box;

    padding: 20px 18px 24px;

    position: relative;
}


/* ----------------------------------------------------------
   P1 gets a slightly larger card
   ---------------------------------------------------------- */

.podium-p1 .podium-driver {

    min-height: 455px;

    border-color: rgba(255, 196, 70, 0.35);

    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(255, 196, 70, 0.08),
            transparent 45%
        ),
        linear-gradient(
            180deg,
            rgba(34, 35, 41, 0.98),
            rgba(18, 20, 27, 0.98)
        );
}


/* ----------------------------------------------------------
   Driver image
   ---------------------------------------------------------- */

.podium-driver-image {

    width: 100%;

    height: 320px;

    object-fit: contain;

    object-position: bottom center;

    display: block;

    margin-bottom: 8px;
}


.podium-p1 .podium-driver-image {

    height: 360px;
}


/* ----------------------------------------------------------
   Driver information
   ---------------------------------------------------------- */

.podium-driver-name {

    font-size: 24px;

    font-weight: 800;

    color: #ffffff;

    line-height: 1.15;

    margin-top: 6px;
}


.podium-driver-team {

    font-size: 15px;

    color: #9ca3af;

    margin-top: 6px;
}


.podium-driver-points {

    font-size: 20px;

    font-weight: 700;

    color: #ffffff;

    margin-top: 12px;
}


.podium-driver-points span {

    font-size: 12px;

    font-weight: 600;

    color: #9ca3af;

    margin-left: 3px;

    letter-spacing: 1px;
}


/* ----------------------------------------------------------
   Podium blocks
   ---------------------------------------------------------- */

.podium-block {

    width: 100%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 48px;

    font-weight: 900;

    color: rgba(255, 255, 255, 0.9);

    border-radius: 0 0 10px 10px;

    box-sizing: border-box;
}


/* P1 = tallest */

.podium-p1 .podium-block {

    height: 120px;

    background:
        linear-gradient(
            180deg,
            rgba(255, 196, 70, 0.30),
            rgba(255, 196, 70, 0.12)
        );

    border: 1px solid rgba(255, 196, 70, 0.25);

    border-top: none;
}


/* P2 */

.podium-p2 .podium-block {

    height: 85px;

    background:
        linear-gradient(
            180deg,
            rgba(192, 192, 192, 0.25),
            rgba(192, 192, 192, 0.10)
        );

    border: 1px solid rgba(192, 192, 192, 0.20);

    border-top: none;
}


/* P3 */

.podium-p3 .podium-block {

    height: 60px;

    background:
        linear-gradient(
            180deg,
            rgba(205, 127, 50, 0.25),
            rgba(205, 127, 50, 0.10)
        );

    border: 1px solid rgba(205, 127, 50, 0.20);

    border-top: none;
}


/* ----------------------------------------------------------
   Responsive
   ---------------------------------------------------------- */

@media (max-width: 900px) {

    .podium-container {

        grid-template-columns:
            1fr 1fr 1fr;

        gap: 12px;

        padding: 0;
    }

    .podium-driver {

        min-height: 330px;
    }

    .podium-p1 .podium-driver {

        min-height: 370px;
    }

    .podium-driver-image {

        height: 250px;
    }

    .podium-p1 .podium-driver-image {

        height: 275px;
    }

    .podium-driver-name {

        font-size: 18px;
    }

    .podium-position-text {

        font-size: 24px;
    }

    .podium-medal {

        font-size: 24px;
    }
}


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {

        .project-banner {
            padding: 25px 30px;
        }

        .project-title {
            font-size: 32px;
        }

        .project-subtitle {
            font-size: 11px;
            letter-spacing: 4px;
        }

        .podium-container {
            gap: 10px;
        }

        .podium-wrapper {
            width: 32%;
        }

        .driver-image {
            width: 160px;
            height: 220px;
        }

        .driver-name {
            font-size: 18px;
        }

        .driver-team {
            font-size: 14px;
        }

        .session-info-grid {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """)


# ==========================================================
# PROJECT HEADER
# ==========================================================

st.html("""
    <div class="project-banner">

        <div class="project-logo">

            <div class="project-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                    <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.22.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 7h11l1.04 3H5.46L6.5 7zM5 15.5A1.5 1.5 0 1 1 5 12.5a1.5 1.5 0 0 1 0 3zm14 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM5 17h14v1H5v-1z"/>
                </svg>
            </div>

            <div>

                <div class="project-title">
                    F1 <span>RACE INTELLIGENCE</span>
                </div>

                <div class="project-subtitle">
                    PERFORMANCE ANALYTICS
                </div>

            </div>

        </div>

    </div>
    """)


# ==========================================================
# SESSION SELECTION
# ==========================================================

st.header("Session Selection")

st.caption("Choose a Formula 1 session to begin the analysis.")

session = session_selector()

st.divider()


if session is None:

    st.info(
        "Select a Season, Circuit and Session above, " "then click **Load Session**."
    )

    st.stop()


# ==========================================================
# SESSION INFORMATION
# ==========================================================

season = session.event["EventDate"].year
event_name = session.event["EventName"]
location = session.event["Location"]
country = session.event["Country"]
session_name = session.name


# Safely convert values to HTML-safe strings

event_name_html = html.escape(str(event_name))
location_html = html.escape(str(location))
country_html = html.escape(str(country))
session_name_html = html.escape(str(session_name))


# ==========================================================
# SESSION RESULTS
# ==========================================================

results = session.results

if results is None or results.empty:

    st.warning("Session results are not available.")

    st.stop()

results = results.copy()


# ==========================================================
# CURRENTLY LOADED SESSION
# ==========================================================

st.header("Currently Loaded Session")


left_col, right_col = st.columns(
    [1.7, 1],
    gap="large",
)


with left_col:

    st.html(f"""
        <div class="loaded-session">

            <div class="loaded-label">
                Currently Loaded Session
            </div>

            <div class="loaded-title">
                {event_name_html} - {session_name_html}
            </div>

            <div class="loaded-location">
                {season} · {location_html}, {country_html}
            </div>

            <div class="session-info-grid">

                <div class="session-info">

                    <div class="session-info-label">
                        Season
                    </div>

                    <div class="session-info-value">
                        {season}
                    </div>

                </div>


                <div class="session-info">

                    <div class="session-info-label">
                        Circuit
                    </div>

                    <div class="session-info-value">
                        {location_html}
                    </div>

                </div>


                <div class="session-info">

                    <div class="session-info-label">
                        Session
                    </div>

                    <div class="session-info-value">
                        {session_name_html}
                    </div>

                </div>

            </div>

        </div>
        """)


with right_col:

    track_image = create_circuit_map(session)

    if track_image:

        st.html(f"""
            <div class="track-card">

                <div class="track-header">

                    <div class="track-title">
                        {location_html}
                    </div>

                    <div class="track-subtitle">
                        {country_html} · {session_name_html}
                    </div>

                </div>

                <div class="track-map">

                    <img
                        src="data:image/png;base64,{track_image}"
                        alt="Circuit layout"
                    >

                </div>

            </div>
            """)

    else:

        st.html(f"""
            <div class="track-card">

                <div class="track-header">

                    <div class="track-title">
                        {location_html}
                    </div>

                    <div class="track-subtitle">
                        {country_html} · {session_name_html}
                    </div>

                </div>

                <div class="track-map-empty">
                    Circuit layout unavailable
                </div>

            </div>
            """)


# ==========================================================
# TOP 3
# ==========================================================

top_three = results.copy()

top_three = top_three[top_three["Position"].notna()].copy()

top_three = top_three.sort_values("Position").head(3)


# ==========================================================
# SESSION TYPE
# ==========================================================

session_lower = session_name.lower()


if "qualifying" in session_lower:

    result_title = ":material/flag: Qualifying Top 3"

elif "practice" in session_lower:

    result_title = ":material/speed: Fastest Drivers"

elif "sprint" in session_lower:

    result_title = ":material/emoji_events: Sprint Result"

else:

    result_title = ":material/emoji_events: Race Result"


# ==========================================================
# PODIUM (fragment for independent rerun)
# ==========================================================

@st.fragment
def render_podium(top_three, season, result_title):
    st.divider()
    st.subheader(result_title)

    if len(top_three) < 3:
        st.info("Not enough classified drivers to display a podium.")
        return

    podium_drivers = []

    for _, driver in top_three.iterrows():
        abbreviation = driver["Abbreviation"]
        try:
            profile = get_driver_profile(abbreviation, season)
        except Exception:
            profile = None

        podium_drivers.append(
            {
                "position": int(driver["Position"]),
                "abbreviation": abbreviation,
                "name": driver.get("FullName", abbreviation),
                "team": driver.get("TeamName", profile.get("team", "Unknown") if profile else "Unknown"),
                "points": driver.get("Points"),
                "image": profile.get("image") if profile else None,
            }
        )

    p1 = next(d for d in podium_drivers if d["position"] == 1)
    p2 = next(d for d in podium_drivers if d["position"] == 2)
    p3 = next(d for d in podium_drivers if d["position"] == 3)

    def podium_card(driver, position):
        card_classes = {1: "podium-p1", 2: "podium-p2", 3: "podium-p3"}
        card_class = card_classes.get(position, "")

        points = driver["points"]
        points_text = f"{float(points):g} <span>PTS</span>" if pd.notna(points) else "-"

        image_html = ""
        if driver["image"]:
            image_html = f'<img src="{html.escape(str(driver["image"]))}" class="podium-driver-image" loading="lazy">'

        name = html.escape(str(driver["name"]))
        team = html.escape(str(driver["team"]))

        return f"""
        <div class="podium-item {card_class}">
            <div class="podium-position">
                <span class="podium-position-text">P{position}</span>
            </div>
            <div class="podium-driver">
                {image_html}
                <div class="podium-driver-name">{name}</div>
                <div class="podium-driver-team">{team}</div>
                <div class="podium-driver-points">{points_text}</div>
            </div>
            <div class="podium-block"><span>{position}</span></div>
        </div>
        """

    st.html(f"""
        <div class="podium-container">
            {podium_card(p2, 2)}
            {podium_card(p1, 1)}
            {podium_card(p3, 3)}
        </div>
        """)


render_podium(top_three, season, result_title)


# ==========================================================
# WEATHER (fragment for independent rerun)
# ==========================================================

@st.fragment
def render_weather(session):
    st.divider()
    st.subheader(":material/wb_sunny: Session Weather")

    weather = session.weather_data

    if weather is None or weather.empty:
        st.info("Weather data is not available for this session.")
        return

    air_temp = weather["AirTemp"].mean()
    track_temp = weather["TrackTemp"].mean()
    humidity = weather["Humidity"].mean()
    wind_speed = weather["WindSpeed"].mean()
    rainfall = weather["Rainfall"].sum() if "Rainfall" in weather.columns else 0

    if rainfall > 0:
        weather_icon = ":material/umbrella:"
        weather_condition = "Rain"
    else:
        weather_icon = ":material/wb_sunny:"
        weather_condition = "Dry"

    w1, w2, w3, w4, w5 = st.columns(5)

    with w1:
        st.metric(f"{weather_icon} Conditions", weather_condition)

    with w2:
        st.metric("Air Temperature", f"{air_temp:.1f} °C")

    with w3:
        st.metric("Track Temperature", f"{track_temp:.1f} °C")

    with w4:
        st.metric("Humidity", f"{humidity:.0f} %")

    with w5:
        st.metric("Wind", f"{wind_speed:.1f} km/h")


render_weather(session)


# ==========================================================
# SESSION HIGHLIGHTS (fragment for independent rerun)
# ==========================================================

@st.fragment
def render_highlights(session, results):
    st.divider()
    st.subheader(":material/analytics: Session Highlights")

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        st.metric("Drivers", len(results))

    total_laps = results["Laps"].max() if "Laps" in results.columns else None
    with h2:
        st.metric("Total Laps", int(total_laps) if pd.notna(total_laps) else "-")

    # Fastest lap
    fastest_lap_seconds = None
    try:
        laps = session.laps
        if laps is not None and not laps.empty:
            valid_laps = laps[laps["LapTime"].notna()]
            if not valid_laps.empty:
                fastest_lap_seconds = valid_laps["LapTime"].min().total_seconds()
    except Exception:
        pass

    with h3:
        st.metric("Fastest Lap", fmt_lap_time(fastest_lap_seconds) if fastest_lap_seconds else "-")

    # Session duration
    session_duration_seconds = None
    try:
        if laps is not None and not laps.empty:
            session_times = laps["Time"].dropna()
            if not session_times.empty:
                session_duration_seconds = session_times.max().total_seconds()
    except Exception:
        pass

    with h4:
        st.metric("Session Duration", format_duration(session_duration_seconds) if session_duration_seconds else "-")


render_highlights(session, results)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.info(
    "Use the pages in the sidebar to explore "
    "Driver, Strategy, Team and Race analysis."
)



