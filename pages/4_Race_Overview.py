import html
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.driver_analysis import (
    driver_summary,
    position_changes,
    format_lap_time,
)
from src.analytics.team_analysis import team_summary
from src.analytics.strategy_analysis import (
    stint_analysis,
    pit_stop_analysis,
    race_pace_evolution,
    compound_comparison,
)
from src.ui.session_selector import session_selector
from src.utils.formatters import format_lap_time as fmt_lap_time, format_duration

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Race Overview",
    page_icon=":material/analytics:",
    layout="wide",
)

# ==========================================================
# CUSTOM CSS
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
    max-width: 1600px;
}


/* ======================================================
   RACE HEADER BANNER
   ====================================================== */

.race-header {
    position: relative;
    overflow: hidden;

    padding: 40px 50px;

    margin-bottom: 36px;

    border-radius: 24px;

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

    box-shadow:
        0 20px 50px rgba(0,0,0,0.25);
}

.race-header::after {
    content: "";

    position: absolute;

    right: -100px;
    top: -140px;

    width: 400px;
    height: 400px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle at 30% 30%,
            rgba(255, 70, 85, 0.12),
            transparent 60%
        );

    pointer-events: none;
}

.race-header-content {
    position: relative;
    z-index: 2;

    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;

    gap: 30px;
}

.race-title-block {
    flex: 1;
    min-width: 280px;
}

.race-category {
    display: inline-block;

    margin-bottom: 10px;

    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;

    color: #ff4655;

    background: rgba(255, 70, 85, 0.12);
    border: 1px solid rgba(255, 70, 85, 0.25);
    border-radius: 6px;

    padding: 6px 14px;
}

.race-name {
    font-size: 42px;
    font-weight: 850;
    line-height: 1.1;
    letter-spacing: -1.5px;

    color: #ffffff;
    margin: 0 0 6px 0;
}

.race-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    margin-top: 12px;
}

.race-meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.race-meta-icon {
    font-size: 18px;
    opacity: 0.7;
}

.race-meta-label {
    font-size: 13px;
    color: rgba(255,255,255,0.55);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.race-meta-value {
    font-size: 15px;
    color: #ffffff;
    font-weight: 600;
}

.race-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.08);
}

.race-stat {
    text-align: center;
}

.race-stat-value {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
}

.race-stat-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.50);
    margin-top: 4px;
}


/* ======================================================
   SECTION BANNER
   ====================================================== */

.section-banner {
    position: relative;
    overflow: hidden;

    margin: 32px 0 24px 0;
    padding: 24px 32px;

    background:
        linear-gradient(
            105deg,
            #111c2b 0%,
            #111a28 60%,
            #17121f 100%
        );

    border: 1px solid #293548;
    border-radius: 16px;

    border-left: 5px solid #ff4058;

    box-shadow:
        0 8px 28px rgba(0,0,0,0.18);
}

.section-number {
    position: absolute;
    right: 32px;
    top: 8px;

    font-size: 64px;
    line-height: 1;
    font-weight: 900;
    color: rgba(255,255,255,0.03);
    pointer-events: none;
}

.section-title-row {
    display: flex;
    align-items: baseline;
    gap: 14px;
    flex-wrap: wrap;
}

.section-kicker {
    margin-bottom: 4px;
    color: #82a9d7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2.2px;
    text-transform: uppercase;
}

.section-title {
    margin: 0;
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.section-subtitle {
    margin-top: 4px;
    color: rgba(255,255,255,0.55);
    font-size: 14px;
    font-weight: 500;
}


/* ======================================================
   DATAFRAME STYLING
   ====================================================== */

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

.stDataFrame [data-testid="stTable"] {
    background: transparent;
}

.stDataFrame thead th {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(255,255,255,0.85) !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    padding: 14px 16px !important;
}

.stDataFrame tbody td {
    color: rgba(255,255,255,0.9) !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    background: transparent !important;
}

.stDataFrame tbody tr:last-child td {
    border-bottom: none !important;
}

.stDataFrame tbody tr:hover td {
    background: rgba(255,255,255,0.02) !important;
}

/* Position column highlight */
.stDataFrame td:first-child {
    font-weight: 700 !important;
    font-size: 16px !important;
}

/* Team color indicators */
.team-color-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}


/* ======================================================
   METRIC CARDS
   ====================================================== */

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 16px;
}

.metric-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px 24px;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: rgba(255,70,85,0.3);
    background: rgba(255,70,85,0.03);
}

.metric-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.50);
    margin-bottom: 6px;
}

.metric-value {
    font-size: 22px;
    font-weight: 750;
    color: #ffffff;
    line-height: 1.2;
}

.metric-delta {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
}

.metric-delta.positive { color: #22c55e; }
.metric-delta.negative { color: #ef4444; }
.metric-delta.neutral { color: #9ca3af; }


/* ======================================================
   CHART CONTAINERS
   ====================================================== */

.chart-container {
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 20px;
    margin-top: 12px;
}

.chart-title {
    font-size: 14px;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}


/* ======================================================
   RESPONSIVE
   ====================================================== */

@media (max-width: 1024px) {
    .race-header {
        padding: 30px 28px;
    }
    .race-name {
        font-size: 32px;
    }
    .race-stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .race-stat-value {
        font-size: 22px;
    }
}

@media (max-width: 768px) {
    .race-header-content {
        flex-direction: column;
        align-items: flex-start;
    }
    .race-stats-grid {
        grid-template-columns: 1fr 1fr;
    }
    .section-banner {
        padding: 20px 24px;
    }
    .section-title {
        font-size: 20px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# TEAM COLOR MAP
# ==========================================================

TEAM_COLORS = {
    "Red Bull Racing": "#1E41FF",
    "Ferrari": "#DC143C",
    "Mercedes": "#00D2BE",
    "McLaren": "#FF8700",
    "Aston Martin": "#006F62",
    "Alpine": "#0090FF",
    "Williams": "#005AFF",
    "RB": "#6692FF",
    "Kick Sauber": "#52E252",
    "Haas F1 Team": "#B6BABD",
    "AlphaTauri": "#2B4562",
    "Alfa Romeo": "#900000",
}

def get_team_color(team_name: str) -> str:
    """Get team color, fallback to gray."""
    return TEAM_COLORS.get(team_name, "#6B7280")


# ==========================================================
# SESSION SELECTION
# ==========================================================

with st.expander(
    ":material/settings: Session Selection",
    expanded=False,
):
    session = session_selector()

if session is None:
    st.info("Select a Season, Circuit and Session to begin race analysis.")
    st.stop()

# ==========================================================
# RACE HEADER
# ==========================================================

season = session.event["EventDate"].year
event_name = session.event["EventName"]
location = session.event["Location"]
country = session.event["Country"]
session_name = session.name

event_name_html = html.escape(str(event_name))
location_html = html.escape(str(location))
country_html = html.escape(str(country))
session_name_html = html.escape(str(session_name))

results = session.results
if results is None or results.empty:
    st.warning("Session results are not available.")
    st.stop()

results = results.copy()
classified = results[results["Position"].notna()].copy()
classified = classified.sort_values("Position")

total_laps = int(classified["Laps"].max()) if "Laps" in classified.columns and classified["Laps"].notna().any() else 0
num_drivers = len(classified)
winner = classified.iloc[0] if len(classified) > 0 else None
winner_name = winner.get("FullName", winner.get("Abbreviation", "N/A")) if winner is not None else "N/A"
winner_team = winner.get("TeamName", "N/A") if winner is not None else "N/A"

# Race duration
race_duration = None
try:
    laps = session.laps
    if laps is not None and not laps.empty:
        session_times = laps["Time"].dropna()
        if not session_times.empty:
            race_duration = session_times.max().total_seconds()
except Exception:
    pass

# Weather
weather_condition = "Unknown"
try:
    weather = session.weather_data
    if weather is not None and not weather.empty:
        rainfall = weather["Rainfall"].sum() if "Rainfall" in weather.columns else 0
        air_temp = weather["AirTemp"].mean()
        track_temp = weather["TrackTemp"].mean()
        if rainfall > 0:
            weather_condition = f"Rain · Air {air_temp:.0f}°C · Track {track_temp:.0f}°C"
        else:
            weather_condition = f"Dry · Air {air_temp:.0f}°C · Track {track_temp:.0f}°C"
except Exception:
    pass

winner_team_color = get_team_color(winner_team)

st.html(f"""
    <div class="race-header">
        <div class="race-header-content">
            <div class="race-title-block">
                <div class="race-category">Grand Prix · {season}</div>
                <h1 class="race-name">{event_name_html}</h1>
                <div class="race-meta">
                    <div class="race-meta-item">
                        <span class="race-meta-icon">📍</span>
                        <span class="race-meta-label">Circuit</span>
                        <span class="race-meta-value">{location_html}, {country_html}</span>
                    </div>
                    <div class="race-meta-item">
                        <span class="race-meta-icon">🏁</span>
                        <span class="race-meta-label">Session</span>
                        <span class="race-meta-value">{session_name_html}</span>
                    </div>
                    <div class="race-meta-item">
                        <span class="race-meta-icon">🌤️</span>
                        <span class="race-meta-label">Conditions</span>
                        <span class="race-meta-value">{html.escape(weather_condition)}</span>
                    </div>
                </div>
                <div class="race-stats-grid">
                    <div class="race-stat">
                        <div class="race-stat-value">{total_laps}</div>
                        <div class="race-stat-label">Total Laps</div>
                    </div>
                    <div class="race-stat">
                        <div class="race-stat-value">{num_drivers}</div>
                        <div class="race-stat-label">Classified Drivers</div>
                    </div>
                    <div class="race-stat">
                        <div class="race-stat-value">{fmt_lap_time(race_duration) if race_duration else "-"}</div>
                        <div class="race-stat-label">Race Duration</div>
                    </div>
                    <div class="race-stat">
                        <div class="race-stat-value" style="color: {winner_team_color};">{html.escape(str(winner_name))}</div>
                        <div class="race-stat-label">Race Winner</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
""")

# ==========================================================
# HELPER: Get fastest laps overall
# ==========================================================

@st.cache_data(show_spinner=False, ttl=3600)
def fastest_laps_overall(_session, top_n=10):
    """Get overall fastest laps across all drivers."""
    if _session is None or _session.laps is None:
        return pd.DataFrame()

    laps = _session.laps.copy()
    laps = laps[laps["LapTime"].notna()].copy()

    if laps.empty:
        return pd.DataFrame()

    laps["Lap Time (s)"] = laps["LapTime"].dt.total_seconds()

    # Remove outlier laps (> 2 minutes for most circuits)
    laps = laps[laps["Lap Time (s)"] < 180].copy()

    # Get fastest lap per driver
    fastest_per_driver = laps.loc[laps.groupby("Driver")["Lap Time (s)"].idxmin()].copy()

    # Sort and take top N
    fastest_per_driver = fastest_per_driver.sort_values("Lap Time (s)").head(top_n).reset_index(drop=True)

    # Add lap number and compound
    cols = ["Driver", "Team", "LapNumber", "Lap Time (s)", "Compound", "TyreLife", "Stint"]
    cols = [c for c in cols if c in fastest_per_driver.columns]
    fastest_per_driver = fastest_per_driver[cols].copy()

    fastest_per_driver.rename(
        columns={
            "LapNumber": "Lap #",
            "TyreLife": "Tyre Life",
        },
        inplace=True,
    )

    fastest_per_driver["Lap Time (s)"] = fastest_per_driver["Lap Time (s)"].round(3)

    # Format lap time
    fastest_per_driver["Lap Time"] = fastest_per_driver["Lap Time (s)"].apply(fmt_lap_time)

    return fastest_per_driver


# ==========================================================
# SECTION 1: TOP 10 FINISHERS
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">01</div>
        <div class="section-title-row">
            <span class="section-kicker">Race Result</span>
            <h2 class="section-title">Top 10 Finishers</h2>
        </div>
        <div class="section-subtitle">Final classification with gaps, points and status</div>
    </div>
""")

# Build top 10 table
top10 = classified.head(10).copy()

display_cols = []
if "Position" in top10.columns:
    display_cols.append("Position")
if "Abbreviation" in top10.columns:
    display_cols.append("Abbreviation")
if "FullName" in top10.columns:
    display_cols.append("FullName")
if "TeamName" in top10.columns:
    display_cols.append("TeamName")
if "GridPosition" in top10.columns:
    display_cols.append("GridPosition")
if "Points" in top10.columns:
    display_cols.append("Points")
if "Status" in top10.columns:
    display_cols.append("Status")

top10_display = top10[display_cols].copy() if display_cols else top10.copy()

# Rename for display
rename_map = {
    "Abbreviation": "Driver",
    "FullName": "Name",
    "TeamName": "Team",
    "GridPosition": "Grid",
    "Points": "Pts",
}
top10_display = top10_display.rename(columns=rename_map)

# Format
if "Position" in top10_display.columns:
    top10_display["Position"] = top10_display["Position"].astype(int)
if "Grid" in top10_display.columns:
    top10_display["Grid"] = pd.to_numeric(top10_display["Grid"], errors="coerce").astype("Int64")
if "Pts" in top10_display.columns:
    top10_display["Pts"] = pd.to_numeric(top10_display["Pts"], errors="coerce").astype("Int64")

# Add team color indicator
def make_team_colored(row):
    team = row.get("Team", "")
    color = get_team_color(team)
    return f'<span class="team-color-dot" style="background:{color}"></span>{html.escape(str(team))}'

if "Team" in top10_display.columns:
    top10_display["Team"] = top10_display.apply(make_team_colored, axis=1)

# Add position change indicator
if "Position" in top10_display.columns and "Grid" in top10_display.columns:
    def pos_change(row):
        pos = row["Position"]
        grid = row["Grid"]
        if pd.notna(grid):
            diff = int(grid) - pos
            if diff > 0:
                return f'<span style="color:#22c55e;font-weight:600;">+{diff}</span>'
            elif diff < 0:
                return f'<span style="color:#ef4444;font-weight:600;">{diff}</span>'
            else:
                return '<span style="color:#9ca3af;">±0</span>'
        return "—"
    top10_display["Pos Δ"] = top10_display.apply(pos_change, axis=1)

# Reorder columns
final_cols = [c for c in ["Position", "Driver", "Name", "Team", "Grid", "Pos Δ", "Pts", "Status"] if c in top10_display.columns]
top10_display = top10_display[final_cols]

st.write(top10_display.to_html(escape=False, index=False), unsafe_allow_html=True)

st.caption("Pos Δ = Grid Position − Finish Position (positive = gained positions)")

# ==========================================================
# SECTION 2: POSITION CHANGES
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">02</div>
        <div class="section-title-row">
            <span class="section-kicker">Race Dynamics</span>
            <h2 class="section-title">Position Changes</h2>
        </div>
        <div class="section-subtitle">Biggest climbers and fallers from grid to finish</div>
    </div>
""")

pos_changes = position_changes(session)

if not pos_changes.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🟢 Biggest Gainers**")
        gainers = pos_changes[pos_changes["Positions Gained"] > 0].head(5)
        if not gainers.empty:
            gainers_display = gainers[["Driver", "Team", "Start Position", "Finish Position", "Positions Gained"]].copy()
            gainers_display = gainers_display.rename(columns={
                "Start Position": "Grid",
                "Finish Position": "Finish",
                "Positions Gained": "Gained",
            })
            gainers_display["Driver"] = gainers_display.apply(
                lambda r: f'<span class="team-color-dot" style="background:{get_team_color(r["Team"])}"></span>{html.escape(str(r["Driver"]))}',
                axis=1
            )
            st.write(gainers_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No position gains")

    with col2:
        st.markdown("**🔴 Biggest Losers**")
        losers = pos_changes[pos_changes["Positions Gained"] < 0].tail(5).sort_values("Positions Gained")
        if not losers.empty:
            losers_display = losers[["Driver", "Team", "Start Position", "Finish Position", "Positions Gained"]].copy()
            losers_display = losers_display.rename(columns={
                "Start Position": "Grid",
                "Finish Position": "Finish",
                "Positions Gained": "Lost",
            })
            losers_display["Lost"] = losers_display["Lost"].abs()
            losers_display["Driver"] = losers_display.apply(
                lambda r: f'<span class="team-color-dot" style="background:{get_team_color(r["Team"])}"></span>{html.escape(str(r["Driver"]))}',
                axis=1
            )
            st.write(losers_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No position losses")

# ==========================================================
# SECTION 3: TEAM STANDINGS
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">03</div>
        <div class="section-title-row">
            <span class="section-kicker">Constructors</span>
            <h2 class="section-title">Team Standings</h2>
        </div>
        <div class="section-subtitle">Combined points and performance summary by team</div>
    </div>
""")

team_sum = team_summary(session)

if not team_sum.empty:
    team_display = team_sum.copy()
    team_display = team_display.rename(columns={
        "Team": "Team",
        "Drivers": "Drivers",
        "Number of Drivers": "Drivers #",
        "Combined Points": "Points",
        "Best Finish": "Best",
        "Average Finish": "Avg Finish",
        "Combined Laps": "Total Laps",
    })
    team_display["Points"] = team_display["Points"].astype(int)
    team_display["Best"] = team_display["Best"].astype(int)
    team_display["Avg Finish"] = team_display["Avg Finish"].round(1)
    team_display["Total Laps"] = team_display["Total Laps"].astype(int)

    team_display["Team"] = team_display["Team"].apply(
        lambda t: f'<span class="team-color-dot" style="background:{get_team_color(t)}"></span>{html.escape(str(t))}'
    )

    st.write(team_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("Team data not available")

# ==========================================================
# SECTION 4: RACE PACE EVOLUTION
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">04</div>
        <div class="section-title-row">
            <span class="section-kicker">Pace Analysis</span>
            <h2 class="section-title">Race Pace Evolution</h2>
        </div>
        <div class="section-subtitle">Lap-by-lap pace for top drivers (clean laps only)</div>
    </div>
""")

pace_data = race_pace_evolution(session)

if not pace_data.empty:
    # Get top 8 drivers by finish position
    top_drivers = classified.head(8)["Abbreviation"].tolist() if "Abbreviation" in classified.columns else []
    pace_top = pace_data[pace_data["Driver"].isin(top_drivers)].copy()

    if not pace_top.empty:
        fig = go.Figure()

        for driver in top_drivers:
            driver_data = pace_top[pace_top["Driver"] == driver].sort_values("Lap Number")
            if driver_data.empty:
                continue

            team = driver_data["Team"].iloc[0] if "Team" in driver_data.columns else ""
            color = get_team_color(team)

            fig.add_trace(go.Scatter(
                x=driver_data["Lap Number"],
                y=driver_data["Lap Time (s)"],
                mode="lines",
                name=driver,
                line=dict(color=color, width=2),
                hovertemplate="<b>%{fullData.name}</b><br>Lap: %{x}<br>Time: %{y:.3f}s<extra></extra>",
            ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.9)", family="Inter, sans-serif"),
            xaxis=dict(
                title="Lap Number",
                gridcolor="rgba(255,255,255,0.06)",
                zerolinecolor="rgba(255,255,255,0.1)",
                showgrid=True,
            ),
            yaxis=dict(
                title="Lap Time (s)",
                gridcolor="rgba(255,255,255,0.06)",
                zerolinecolor="rgba(255,255,255,0.1)",
                showgrid=True,
                autorange="reversed",  # Lower is better (faster)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11),
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(l=60, r=20, t=40, b=60),
            height=450,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pace data not available for top drivers")
else:
    st.info("Race pace data not available")

# ==========================================================
# SECTION 5: TYRE COMPOUND COMPARISON
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">05</div>
        <div class="section-title-row">
            <span class="section-kicker">Strategy</span>
            <h2 class="section-title">Tyre Compound Comparison</h2>
        </div>
        <div class="section-subtitle">Average lap time by compound (representative race laps only)</div>
    </div>
""")

compound_data = compound_comparison(session)

if not compound_data.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            compound_data,
            x="Compound",
            y="Average Lap Time (s)",
            color="Compound",
            text="Average Lap Time (s)",
            hover_data=["Fastest Lap (s)", "Average Tyre Life", "Maximum Tyre Life", "Number of Laps", "Drivers Using Compound"],
        )

        fig.update_traces(
            texttemplate="%{y:.3f}s",
            textposition="outside",
            marker_line_width=0,
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.9)", family="Inter, sans-serif"),
            xaxis=dict(
                title="",
                gridcolor="rgba(255,255,255,0.06)",
                showgrid=False,
            ),
            yaxis=dict(
                title="Average Lap Time (s)",
                gridcolor="rgba(255,255,255,0.06)",
                zerolinecolor="rgba(255,255,255,0.1)",
                autorange="reversed",
            ),
            showlegend=False,
            margin=dict(l=60, r=20, t=20, b=60),
            height=380,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        comp_display = compound_data.copy()
        comp_display = comp_display.rename(columns={
            "Average Lap Time (s)": "Avg Time (s)",
            "Fastest Lap (s)": "Best (s)",
            "Average Tyre Life": "Avg Life",
            "Maximum Tyre Life": "Max Life",
            "Number of Laps": "Laps",
            "Drivers Using Compound": "Drivers",
        })
        comp_display["Avg Time (s)"] = comp_display["Avg Time (s)"].round(3)
        comp_display["Best (s)"] = comp_display["Best (s)"].round(3)
        comp_display["Avg Life"] = comp_display["Avg Life"].round(1)
        comp_display["Max Life"] = comp_display["Max Life"].astype(int)

        st.write(comp_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("Tyre compound data not available")

# ==========================================================
# SECTION 6: PIT STOP SUMMARY
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">06</div>
        <div class="section-title-row">
            <span class="section-kicker">Strategy</span>
            <h2 class="section-title">Pit Stop Summary</h2>
        </div>
        <div class="section-subtitle">Strategic pit stops with compounds and stint lengths</div>
    </div>
""")

pit_data = pit_stop_analysis(session)

if not pit_data.empty:
    pit_display = pit_data.copy()
    pit_display = pit_display.rename(columns={
        "Driver": "Driver",
        "Team": "Team",
        "Pit Stop": "Stop #",
        "Pit Lap": "Lap",
        "Old Compound": "From",
        "New Compound": "To",
        "Previous Stint Length": "Stint",
    })

    pit_display["Driver"] = pit_display.apply(
        lambda r: f'<span class="team-color-dot" style="background:{get_team_color(r["Team"])}"></span>{html.escape(str(r["Driver"]))}',
        axis=1
    )
    pit_display["Strategy"] = pit_display["From"] + " → " + pit_display["To"]

    display_cols = [c for c in ["Driver", "Team", "Stop #", "Lap", "Strategy", "Stint"] if c in pit_display.columns]
    pit_display = pit_display[display_cols]

    st.write(pit_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No pit stops recorded (single-stint race or data unavailable)")

# ==========================================================
# SECTION 7: FASTEST LAPS
# ==========================================================

st.html("""
    <div class="section-banner">
        <div class="section-number">07</div>
        <div class="section-title-row">
            <span class="section-kicker">Performance</span>
            <h2 class="section-title">Fastest Laps Overall</h2>
        </div>
        <div class="section-subtitle">Top 10 fastest individual laps of the race</div>
    </div>
""")

fastest_laps = fastest_laps_overall(session, top_n=10)

if not fastest_laps.empty:
    fl_display = fastest_laps.copy()
    fl_display = fl_display.rename(columns={
        "Driver": "Driver",
        "Team": "Team",
        "Lap #": "Lap",
        "Lap Time": "Time",
        "Compound": "Compound",
        "Tyre Life": "Tyre Life",
        "Stint": "Stint",
    })

    fl_display["Driver"] = fl_display.apply(
        lambda r: f'<span class="team-color-dot" style="background:{get_team_color(r["Team"])}"></span>{html.escape(str(r["Driver"]))}',
        axis=1
    )

    display_cols = [c for c in ["Driver", "Team", "Lap", "Time", "Compound", "Tyre Life", "Stint"] if c in fl_display.columns]
    fl_display = fl_display[display_cols]

    st.write(fl_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("Fastest laps data not available")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()
st.caption("Data sourced from FastF1 · Race Overview analysis")