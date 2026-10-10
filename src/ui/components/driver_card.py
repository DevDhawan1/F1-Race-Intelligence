import html

import streamlit as st


TEAM_COLORS = {
    "Alpine": "#274a9b",
    "Aston Martin": "#006f62",
    "Audi": "#59616b",
    "Cadillac": "#7d6b45",
    "Ferrari": "#b00020",
    "Haas F1 Team": "#59636e",
    "McLaren": "#d97822",
    "Mercedes": "#167b76",
    "Racing Bulls": "#303d72",
    "Red Bull Racing": "#182548",
    "Williams": "#1764a5",
}

NATIONALITY_DISPLAY = {
    "Argentine": ("ar", "Argentina"),
    "Australian": ("au", "Australia"),
    "Austrian": ("at", "Austria"),
    "Belgian": ("be", "Belgium"),
    "Brazilian": ("br", "Brazil"),
    "British": ("gb", "United Kingdom"),
    "Canadian": ("ca", "Canada"),
    "Dutch": ("nl", "Netherlands"),
    "Finnish": ("fi", "Finland"),
    "French": ("fr", "France"),
    "German": ("de", "Germany"),
    "Italian": ("it", "Italy"),
    "Japanese": ("jp", "Japan"),
    "Mexican": ("mx", "Mexico"),
    "Monegasque": ("mc", "Monaco"),
    "New Zealander": ("nz", "New Zealand"),
    "Spanish": ("es", "Spain"),
    "Thai": ("th", "Thailand"),
}


def _team_color(team):
    return TEAM_COLORS.get(team, "#3c424b")


def driver_card(profile, show_stats=True):
    team = profile.get("team") or "Team unavailable"
    team_color = _team_color(team)
    first_name = profile.get("first_name") or "Driver"
    last_name = profile.get("last_name") or profile.get("name") or "Profile"
    image = profile.get("image")
    nationality = profile.get("nationality") or "Nationality unavailable"
    country_code, country = NATIONALITY_DISPLAY.get(nationality, (None, nationality))
    flag_markup = (
        f'<img class="driver-flag" src="https://flagcdn.com/24x18/{country_code}.png" '
        f'alt="{html.escape(str(country))} flag">'
        if country_code
        else ""
    )
    driver_number = profile.get("number") or "-"

    if image:
        image_markup = (
            f'<img class="driver-banner-image" src="{html.escape(image, quote=True)}" '
            'alt="Driver portrait">'
        )
    else:
        image_markup = '<div class="driver-banner-placeholder">Image unavailable</div>'

    st.html(f"""
        <style>
            .driver-banner {{
                position: relative;
                min-height: 340px;
                overflow: hidden;
                border: 1px solid color-mix(in srgb, var(--team-color), white 12%);
                border-radius: 2px;
                background: linear-gradient(110deg, color-mix(in srgb, var(--team-color), black 42%) 0%, var(--team-color) 58%, color-mix(in srgb, var(--team-color), white 8%) 100%);
                color: #ffffff;
                isolation: isolate;
            }}
            .driver-banner-background {{
                position: absolute;
                inset: 0;
                opacity: 0.16;
                background: repeating-linear-gradient(135deg, transparent 0 58px, #ffffff 59px 62px, transparent 63px 116px);
                mask-image: linear-gradient(90deg, black 0%, black 64%, transparent 94%);
                z-index: -1;
            }}
            .driver-banner::before, .driver-banner::after {{
                content: "";
                position: absolute;
                left: 32%;
                width: 22px;
                height: 64px;
                background: #ffffff;
                z-index: 3;
                clip-path: polygon(0 0, 100% 0, 100% 72%, 58% 100%, 0 72%);
            }}
            .driver-banner::before {{ top: 0; height: 86px; }}
            .driver-banner::after {{ bottom: 0; transform: rotate(180deg); }}
            .driver-banner-copy {{
                position: relative;
                z-index: 2;
                padding: 105px 0 72px 16%;
                width: 48%;
            }}
            .driver-banner-kicker {{
                display: none;
                color: rgba(255,255,255,0.7);
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 3px;
                margin-bottom: 26px;
            }}
            .driver-banner-first-name {{
                font-size: 38px;
                font-family: "Northwell Clean Alt", "Brush Script MT", "Segoe Script", cursive;
                font-style: normal;
                line-height: 1;
                margin: 0;
                text-align: center;
            }}
            .driver-banner-last-name {{
                font-size: clamp(38px, 5.4vw, 72px);
                font-family: "Motiga Regular", Arial, sans-serif;
                font-weight: 900;
                letter-spacing: -2px;
                line-height: 0.95;
                margin: 3px 0 24px;
                text-align: center;
            }}
            .driver-banner-meta {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 0;
                color: rgba(255,255,255,0.9);
                font-size: 16px;
                font-weight: 700;
                text-align: center;
                width: 100%;
                margin-top: 8px;
            }}
            .driver-banner-meta span {{
                padding: 0 14px;
                border-right: 1px solid rgba(255,255,255,0.45);
            }}
            .driver-banner-meta span:first-child {{ padding-left: 0; }}
            .driver-banner-meta span:last-child {{ border-right: 0; }}
            .driver-flag {{
                width: 18px;
                height: 13px;
                object-fit: cover;
                vertical-align: -1px;
                margin-right: 5px;
            }}
            .driver-banner-portrait {{
                position: absolute;
                right: -2%;
                top: 0;
                height: 100%;
                width: 50%;
                box-sizing: border-box;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                z-index: 1;
            }}
            .driver-banner-number {{
                position: absolute;
                right: 2%;
                bottom: -28px;
                color: rgba(0,0,0,0.28);
                font-size: clamp(220px, 30vw, 420px);
                font-family: "Arial Narrow", "Roboto Condensed", Impact, sans-serif;
                font-stretch: condensed;
                font-weight: 900;
                line-height: 0.8;
                letter-spacing: -20px;
                transform: scaleX(0.82);
                transform-origin: center bottom;
                z-index: 0;
            }}
            .driver-banner-image {{
                display: block;
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: center top;
                transform: scale(1.6);
                transform-origin: center top;
                filter: drop-shadow(-18px 12px 18px rgba(0,0,0,0.35));
            }}
            .driver-banner-placeholder {{
                color: rgba(255,255,255,0.6);
                font-size: 14px;
                padding-bottom: 48px;
            }}
            @media (max-width: 700px) {{
                .driver-banner {{ min-height: 290px; }}
                .driver-banner-copy {{ padding: 88px 0 42px 9%; width: 62%; }}
                .driver-banner-first-name {{ font-size: 22px; }}
                .driver-banner-last-name {{ font-size: 38px; }}
                .driver-banner-meta {{ font-size: 11px; }}
                .driver-banner-meta span {{ padding: 0 7px; }}
                .driver-banner-portrait {{ right: -8%; width: 54%; }}
                .driver-banner-number {{ right: 0; }}
            }}
        </style>
        <div class="driver-banner" style="--team-color: {team_color};">
            <div class="driver-banner-background"></div>
            <div class="driver-banner-copy">
                <div class="driver-banner-kicker">DRIVER PROFILE</div>
                <div class="driver-banner-first-name">{html.escape(str(first_name))}</div>
                <div class="driver-banner-last-name">{html.escape(str(last_name)).upper()}</div>
                <div class="driver-banner-meta">
                    <span>{flag_markup}{html.escape(str(country))}</span>
                    <span>{html.escape(str(team))}</span>
                    <span>#{html.escape(str(profile.get("number") or "-"))}</span>
                </div>
            </div>
            <div class="driver-banner-portrait">
                {image_markup}
            </div>
            <div class="driver-banner-number">{html.escape(str(driver_number))}</div>
        </div>
        """)

    if not show_stats:
        return

    with st.container(border=True):
        st.subheader("2026 Season Statistics")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Championship Position",
                profile["position"] if profile["position"] is not None else "-",
            )

        with c2:
            st.metric(
                "Points",
                profile["points"] if profile["points"] is not None else "-",
            )

        c3, c4 = st.columns(2)

        with c3:
            st.metric(
                "Wins",
                profile["wins"] if profile["wins"] is not None else "-",
            )

        with c4:
            st.metric(
                "Team",
                profile["team"] if profile["team"] is not None else "-",
            )
