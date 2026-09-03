# Execution Flow

## App Entry Point: `app.py`

```
app.py
├── st.set_page_config() - Page title, icon, wide layout
├── st.Page() definitions for 5 pages
│   ├── 0_Dashboard.py (default)
│   ├── 1_Driver_Analysis.py
│   ├── 2_Strategy_Analysis.py
│   ├── 3_Team_Analysis.py
│   └── 4_Race_Overview.py
└── st.navigation(pages).run() - Starts multi-page app
```

## Page Execution Flow (each page follows similar pattern)

### 0_Dashboard.py
```
1. st.set_page_config() - Duplicate config (override)
2. Inject 700+ lines of custom CSS via st.html()
3. Render project banner (HTML)
4. Session Selection
   └── session_selector() from src/ui/session_selector.py
       ├── st.session_state.session_config initialization
       ├── Season selectbox (2018-current_year)
       ├── Circuit selectbox (from FastF1 schedule)
       ├── Session selectbox (FP1, FP2, FP3, Q, R, S, SQ)
       └── Load Session button → load_session() from src/data/loader.py
           ├── fastf1.get_session(year, gp, session_type)
           ├── session.load() - Downloads/caches data
           └── Returns Session object
5. If session loaded:
   ├── Extract event metadata (season, circuit, location, session_name)
   ├── Load session.results
   ├── Render "Currently Loaded Session" (HTML + circuit map)
   ├── Render Podium (Top 3) - fetches driver profiles via get_driver_profile()
   ├── Render Weather metrics (from session.weather_data)
   └── Render Session Highlights (drivers, laps, fastest lap, duration)
```

### 1_Driver_Analysis.py
```
1. st.set_page_config()
2. Inject 900+ lines custom CSS
3. Render page header (HTML)
4. Session Selection (expander) → session_selector()
5. Driver Selection → driver_selector() from src/ui/driver_selector.py
   └── st.selectbox from session.results["Abbreviation"]
6. Get driver profile → get_driver_profile() from src/services/driver_service.py
   ├── get_driver_metadata() from f1_api.py (Jolpica API)
   ├── get_driver_standings() from f1_api.py (Jolpica API)
   └── get_driver_image() from formula1_assets.py (F1.com scraping)
7. Render Driver Card (HTML)
8. Session Statistics → get_session_driver_stats()
9. Lap Pace Analysis → driver_lap_analysis() from src/analytics/driver_analysis.py
   ├── _get_valid_laps() - filter NaN LapTime
   ├── _convert_lap_time() - LapTime → seconds
   └── Returns DataFrame with LapNumber, Lap Time, Compound, TyreLife, Stint
10. Render lap metrics + line chart + data table
11. Speed Analysis → speed_analysis() from driver_analysis.py
12. Sector Analysis → sector_analysis() from driver_analysis.py
13. Position Analysis → position_changes() from driver_analysis.py
14. Tyre Strategy → tyre_usage() from driver_analysis.py
    └── Builds stint timeline + cards from lap data
```

### 2_Strategy_Analysis.py
```
1. st.set_page_config()
2. Inject 500+ lines custom CSS
3. Session Selection (expander) → session_selector()
4. Load all analytics (try/except each):
   ├── stint_analysis()
   ├── tyre_degradation()
   ├── pit_stop_analysis()
   ├── race_pace_evolution()
   └── compound_comparison()
   All from src/analytics/strategy_analysis.py
5. Strategy Overview - metric cards
6. Stint Strategy
   ├── Driver selectbox
   ├── Timeline (HTML flexbox)
   └── Stint cards (HTML)
7. Tyre Performance - compound comparison table
8. Tyre Degradation
   ├── Driver selectbox
   └── Line chart (Tyre Life vs Lap Time)
9. Pit Stop Analysis - pit cards per driver
10. Race Pace - pace evolution chart per driver
11. Strategy Insight - text summary
```

### 3_Team_Analysis.py
```
1. st.set_page_config()
2. Inject 500+ lines custom CSS
3. Session Selection (expander) → session_selector()
4. Team Selection - selectbox from unique TeamName in results
5. Get both team drivers
6. For each driver: get_driver_comparison_data()
   ├── session.results
   ├── driver_lap_analysis() for pace
   ├── get_driver_profile() for image
   └── Calculates positions gained
7. Render two driver cards side-by-side (HTML grid)
8. Team Summary - combined points, best finish, pace gap
```

### 4_Race_Overview.py
```
EMPTY - placeholder page
```

## Data Layer

```
src/data/loader.py
├── PROJECT_ROOT = Path(__file__).parents[2]
├── CACHE_DIR = PROJECT_ROOT / "data" / "cache"
├── fastf1.Cache.enable_cache(CACHE_DIR)
└── load_session(year, gp, session_type) → Session
```

## Analytics Layer

```
src/analytics/
├── driver_analysis.py
│   ├── _get_valid_laps()
│   ├── _convert_lap_time()
│   ├── _convert_sector_times()
│   ├── driver_summary()
│   ├── sector_analysis()
│   ├── speed_analysis()
│   ├── driver_report()
│   ├── position_changes()
│   ├── tyre_usage()
│   ├── driver_lap_analysis()
│   └── format_lap_time()
├── strategy_analysis.py
│   ├── _get_valid_laps()
│   ├── stint_analysis()
│   ├── tyre_degradation()
│   ├── pit_stop_analysis()
│   ├── race_pace_evolution()
│   └── compound_comparison()
└── team_analysis.py
    ├── _get_valid_laps()
    ├── _get_clean_race_laps()
    ├── _clean_numeric()
    ├── team_summary()
    ├── teammate_comparison()
    ├── team_pace_comparison()
    ├── team_tyre_strategy()
    └── team_performance()
```

## Services Layer

```
src/services/
├── f1_api.py
│   ├── BASE_URL = "https://api.jolpi.ca/ergast/f1"
│   ├── load_all_drivers(season) @st.cache_data
│   ├── get_driver_metadata()
│   ├── load_driver_standings(season) @st.cache_data  [FIXED: removed duplicate]
│   └── get_driver_standings()  [FIXED: removed duplicate]
├── driver_service.py
│   ├── get_driver_profile() - combines metadata + standings + image
│   └── get_session_driver_stats() - from FastF1 session.results
└── formula1_assets.py
    ├── load_driver_images() @st.cache_data - scrapes F1.com
    └── get_driver_image(slug)
```

## Analytics Layer (NEW: Added @st.cache_data to all main functions)

```
src/analytics/
├── driver_analysis.py
│   ├── _session_cache_key() - generates cache key from session metadata
│   ├── _get_valid_laps()
│   ├── _convert_lap_time()
│   ├── _convert_sector_times()
│   ├── driver_summary() @st.cache_data(ttl=3600)
│   ├── sector_analysis() @st.cache_data(ttl=3600)
│   ├── speed_analysis() @st.cache_data(ttl=3600)
│   ├── driver_report()
│   ├── position_changes() @st.cache_data(ttl=3600)
│   ├── tyre_usage() @st.cache_data(ttl=3600)
│   ├── driver_lap_analysis()
│   └── format_lap_time()
├── strategy_analysis.py
│   ├── _session_cache_key() - generates cache key from session metadata
│   ├── _get_valid_laps()
│   ├── stint_analysis() @st.cache_data(ttl=3600)
│   ├── tyre_degradation() @st.cache_data(ttl=3600)
│   ├── pit_stop_analysis() @st.cache_data(ttl=3600)
│   ├── race_pace_evolution() @st.cache_data(ttl=3600)
│   └── compound_comparison() @st.cache_data(ttl=3600)
└── team_analysis.py
    ├── _session_cache_key() - generates cache key from session metadata
    ├── _get_valid_laps()
    ├── _get_clean_race_laps()
    ├── _clean_numeric()
    ├── team_summary() @st.cache_data(ttl=3600)
    ├── teammate_comparison() @st.cache_data(ttl=3600)
    ├── team_pace_comparison() @st.cache_data(ttl=3600)
    ├── team_tyre_strategy() @st.cache_data(ttl=3600)
    └── team_performance() @st.cache_data(ttl=3600)
```

## New: Theme Configuration

```
.streamlit/config.toml
├── [theme]
│   ├── primaryColor = "#FF1801" (F1 Red)
│   ├── backgroundColor = "#0E0E11" (Carbon)
│   ├── secondaryBackgroundColor = "#15151E" (Dark)
│   ├── textColor = "#FFFFFF"
│   └── font = "sans serif"
├── [sidebar] backgroundColor = "#15151E"
├── [server] port=8501, CORS disabled
├── [browser] gatherUsageStats = false
├── [runner] fixMatplotlib = true
└── [global] suppressDeprecationWarnings = true
```

## UI Components

```
src/ui/
├── session_selector.py
│   ├── get_schedule(year) @st.cache_data
│   ├── get_event_mapping(schedule)
│   └── session_selector() - full UI + state management
├── driver_selector.py - simple selectbox
├── circuit_map.py
│   └── create_circuit_map() - matplotlib → base64 PNG
└── components/
    ├── driver_card.py
    ├── team_card.py
    ├── podium_card.py
    └── weather_card.py
```

## Utilities

```
src/utils/
├── lap_filters.py - remove_outlier_laps()
├── formatters.py
└── formatting.py
```

## Cache Structure

```
data/cache/
├── fastf1_http_cache.sqlite
└── {year}/{event}/{session}/
    ├── _extended_timing_data.ff1pkl
    ├── weather_data.ff1pkl
    ├── track_status_data.ff1pkl
    ├── timing_app_data.ff1pkl
    ├── session_status_data.ff1pkl
    ├── session_info.ff1pkl
    ├── race_control_messages.ff1pkl
    ├── position_data.ff1pkl
    ├── lap_count.ff1pkl
    ├── driver_info.ff1pkl
    └── car_data.ff1pkl
```

## Key Execution Notes

1. **Session state persists across pages** - `st.session_state.session_config` holds loaded session
2. **FastF1 caching** - HTTP requests cached in SQLite, session data pickled per event
3. **API caching** - Jolpica API calls cached via `@st.cache_data` (1hr default)
4. **Image caching** - F1.com driver images cached via `@st.cache_data`
5. **Analytics caching (NEW)** - All main analytics functions cached with `@st.cache_data(ttl=3600)` using session-based cache keys
6. **No fragmentation** - Full page reruns on every widget interaction
7. **CSS injection on every run** - 2000+ lines of HTML/CSS injected per page load
8. **Native theming (NEW)** - `.streamlit/config.toml` defines F1 brand colors, ready for CSS migration

## Changes Applied (2026-09-01)

### Completed
- ✅ Created `.streamlit/config.toml` with F1 theme
- ✅ Fixed duplicate code in `src/services/f1_api.py` (removed 54 lines)
- ✅ Added `@st.cache_data(ttl=3600)` to all main analytics functions:
  - `driver_analysis.py`: 5 functions cached
  - `strategy_analysis.py`: 5 functions cached  
  - `team_analysis.py`: 6 functions cached
- ✅ Added `_session_cache_key()` helper to each analytics module for consistent cache keys
- ✅ Replaced deprecated `use_container_width=True` with `width="stretch"` in 3 files:
  - `pages/1_Driver_Analysis.py:1235` (st.dataframe)
  - `pages/2_Strategy_Analysis.py:877` (st.dataframe)
  - `src/ui/session_selector.py:226` (st.button)
- ✅ Replaced emojis with Material Symbols icons in `app.py` navigation
- ✅ Migrated session type selector to `st.segmented_control` in `src/ui/session_selector.py`
- ✅ Refactored `session_selector.py` - cleaner layout, type hints, better UX
- ✅ Added `@st.fragment` to dashboard sections: podium, weather, highlights (`0_Dashboard.py`)
- ✅ Replaced emojis with Material Symbols in dashboard (result titles, weather, highlights)
- ✅ Added `@st.fragment` to strategy sections: stint timeline/cards, pit stops (`2_Strategy_Analysis.py`)
- ✅ Replaced all em dashes (—) with hyphens (-) in 22 project files
- ✅ Replaced all remaining emojis with Material Symbols:
  - Page icons: `🛞`→`:material/tire_repair:`, `🏎️`→`:material/flag:`, `👤`→`:material/person:`
  - Dashboard banner: `🏎️`→`:material/sports_motorsports:`
  - Expander title: `⚙️`→`:material/settings:`
- ✅ Verified syntax on all modified files

### Next Steps (Planned)
- Migrate inline CSS to native widgets + config.toml theme
- Replace custom HTML cards with `st.container(border=True)`
- Implement `4_Race_Overview.py`
- Add driver/team images using native `st.image` instead of HTML