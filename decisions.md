# Decisions Log

## 2026-09-01 - Project Initialization

### Decision 1: Use Streamlit's native theming over inline CSS
**Context**: The app uses extensive inline CSS via `st.html()` and `st.markdown(unsafe_allow_html=True)`
**Choice**: Migrate to `.streamlit/config.toml` for theme colors, use native widgets where possible
**Reasoning**: 
- Native theming is maintainable, accessible, and works with Streamlit updates
- Inline CSS breaks with Streamlit version changes
- Reduces code by ~400 lines per page
- **Reference**: `developing-with-streamlit` skill → `references/theme.md`

### Decision 2: Replace deprecated `use_container_width` with `width="stretch"`
**Context**: Multiple files use `use_container_width=True` on metrics, dataframes, charts
**Choice**: Use `width="stretch"` (or `width="content"` for fixed width)
**Reasoning**: 
- `use_container_width` is deprecated since Streamlit 1.37
- New API is more explicit about behavior
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 98

### Decision 3: Use `st.fragment` for independent rerunnable sections
**Context**: Pages have sections like tyre strategy, pit stops, weather that don't need full page rerun
**Choice**: Wrap independent sections in `@st.fragment`
**Reasoning**: 
- Prevents expensive re-computation on widget interactions
- Improves perceived performance
- **Reference**: `developing-with-streamlit` skill → `references/performance.md`

### Decision 4: Use `st.segmented_control` instead of `st.radio(horizontal=True)`
**Context**: Session selector uses horizontal radio buttons
**Choice**: Migrate to `st.segmented_control`
**Reasoning**: 
- Modern, accessible, mobile-friendly
- Better visual design out of the box
- **Reference**: `developing-with-streamlit` skill → `references/selection-widgets.md`

### Decision 5: Use Material Symbols icons over emojis
**Context**: App uses emojis (🏎️, 🏁, 🛞, etc.) throughout
**Choice**: Replace with `:material/icon_name:` syntax
**Reasoning**: 
- Consistent rendering across platforms
- Scalable, styleable with CSS
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 102

### Decision 6: Use `st.container(border=True)` for visual grouping
**Context**: Custom HTML cards for metrics, driver panels, stint cards
**Choice**: Replace with native bordered containers
**Reasoning**: 
- Responsive, accessible, theme-aware
- Reduces custom HTML/CSS maintenance
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 105

### Decision 7: Cache expensive FastF1 operations with `st.cache_data`
**Context**: Analytics functions called on every page load
**Choice**: Add `@st.cache_data(ttl=3600)` to analytics functions
**Reasoning**: 
- FastF1 data loading is slow (network + processing)
- Session data doesn't change during analysis
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 107
**Implementation**: Added cache key helper `_session_cache_key(session)` using year, event name, session name. Applied to all main analytics functions in `driver_analysis.py`, `strategy_analysis.py`, `team_analysis.py`

### Decision 8: Fix duplicate code in `f1_api.py`
**Context**: `load_driver_standings` and `get_driver_standings` defined twice (lines 75-131 and 134-186)
**Choice**: Remove duplicate definitions (kept first occurrence)
**Reasoning**: 
- Bug risk (which one gets called?)
- Code clarity
- Reduced file from 186 to 132 lines

### Decision 9: Create `.streamlit/config.toml` for native theming
**Context**: App uses 2000+ lines of inline CSS across pages
**Choice**: Created config.toml with F1 brand colors (primary: #FF1801, backgrounds: #0E0E11/#15151E)
**Reasoning**: 
- Centralizes theme configuration
- Works with Streamlit's native theming system
- Enables future migration from inline CSS to native widgets
- **Reference**: `developing-with-streamlit` skill → `references/theme.md`

### Decision 10: Replace deprecated `use_container_width` with `width="stretch"` in project files
**Context**: Found 3 usages in project code (not .venv):
- `pages/1_Driver_Analysis.py:1235` - st.dataframe
- `pages/2_Strategy_Analysis.py:877` - st.dataframe  
- `src/ui/session_selector.py:226` - st.button
**Choice**: Replace with `width="stretch"` for dataframes/button
**Reasoning**: 
- `use_container_width` deprecated since Streamlit 1.37
- `width="stretch"` is the explicit replacement for True
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 98
- **Implementation**: All 3 occurrences fixed, syntax verified

### Decision 11: Replace emojis with Material Symbols icons
**Context**: App uses emojis (🏎️, 🏠, 👤, 🛞, 🏁, 📊) in navigation and UI
**Choice**: Replace with `:material/icon_name:` syntax
**Reasoning**: 
- Consistent rendering across platforms
- Scalable, styleable with CSS, theme-aware
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 102
- **Implementation**: Updated `app.py` page icons (sports_motorsports, dashboard, person, tire_repair, flag, analytics)

### Decision 12: Use `st.segmented_control` for session type selection
**Context**: Session selector used `st.selectbox` for session type
**Choice**: Migrate to `st.segmented_control` in `session_selector.py`
**Reasoning**: 
- Modern, accessible, mobile-friendly horizontal selection
- Better visual design, clearer options
- **Reference**: `developing-with-streamlit` skill → `references/selection-widgets.md`
- **Implementation**: Refactored `session_selector.py` - cleaner layout, removed col3, added segmented control for session type

### Decision 13: Add `st.fragment` to independent dashboard sections
**Context**: Dashboard renders podium, weather, highlights on every interaction
**Choice**: Wrap each section in `@st.fragment` for independent reruns
**Reasoning**: 
- Prevents full page rerun when interacting with one section
- Improves perceived performance significantly
- **Reference**: `developing-with-streamlit` skill → `references/performance.md`
- **Implementation**: Added `render_podium()`, `render_weather()`, `render_highlights()` functions with `@st.fragment` in `0_Dashboard.py`

### Decision 14: Replace emojis with Material Symbols in dashboard
**Context**: Dashboard used emojis (🏁, ⚡, 🏆, 🌤️, 📊, 🥇, 🥈, 🥉, 🌧️, ☀️)
**Choice**: Replace with `:material/icon_name:` syntax
**Reasoning**: 
- Consistent rendering, theme-aware, scalable
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 102
- **Implementation**: Updated result titles, weather icons, session highlights in `0_Dashboard.py`

### Decision 15: Add `st.fragment` to strategy page sections
**Context**: Strategy page renders stint timeline, stint cards, pit stops on every interaction
**Choice**: Wrap stint strategy and pit stop sections in `@st.fragment`
**Reasoning**: 
- Independent reruns when driver selection changes
- Prevents re-computing other sections (compound comparison, degradation, pace)
- **Reference**: `developing-with-streamlit` skill → `references/performance.md`
- **Implementation**: Added `render_stint_strategy()` and `render_pit_stops()` with `@st.fragment` in `2_Strategy_Analysis.py`

### Decision 16: Replace all em dashes (—) with hyphens (-)
**Context**: Codebase used em dashes in comments, strings, and section headers
**Choice**: Replace all em dashes with regular hyphens
**Reasoning**: 
- Em dashes can cause encoding issues in some environments
- Hyphens are ASCII-safe and universally compatible
- **Implementation**: Replaced in all project files (22 files)

### Decision 17: Replace all emojis with Material Symbols icons
**Context**: Remaining emojis in page configs and dashboard header
**Choice**: Replace with `:material/icon_name:` syntax
**Reasoning**: 
- Consistent rendering, theme-aware, scalable
- **Reference**: `developing-with-streamlit` skill → `references/best-practices.md` line 102
- **Implementation**: 
  - Page icons: `🛞`→`:material/tire_repair:`, `🏎️`→`:material/flag:`, `👤`→`:material/person:`
  - Dashboard banner: `🏎️`→`:material/sports_motorsports:`
  - Expander title: `⚙️`→`:material/settings:`