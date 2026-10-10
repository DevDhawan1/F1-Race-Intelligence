# F1 Race Intelligence

F1 Race Intelligence is a local-only Streamlit dashboard for exploring Formula 1 sessions with FastF1. It is designed for local development and analysis, where FastF1 can download and cache the session data required by the dashboard.

This repository is not the planned hosted/web application. That product will be developed separately with a different data source and frontend architecture.

## Features

- **Dashboard** — Session selection, podium, weather, highlights, and circuit map
- **Driver Analysis** — Lap pace, sectors, speed traps, position changes, and tyre usage
- **Strategy Analysis** — Stints, pit stops, compound performance, degradation, and race pace
- **Team Analysis** — Teammate comparison, team pace, tyre strategy, and team summaries
- **Race Overview** — Finishers, position changes, team standings, compound performance, pit stops, and fastest laps

## Run locally

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

## Important local-only behavior

- FastF1 downloads session data from its upstream timing sources.
- Downloaded files are cached locally under `data/cache/`.
- The cache is intentionally ignored by Git and is not deployed with this repository.
- The dashboard works best locally because the local FastF1 cache and network environment provide the detailed lap and telemetry data used by the analytics pages.
- If FastF1 returns only partial data, the app displays no-data states for affected analysis sections.

## Project structure

```text
├── app.py                         # Streamlit entry point and navigation
├── pages/
│   ├── 0_Dashboard.py             # Session overview
│   ├── 1_Driver_Analysis.py       # Driver deep-dive
│   ├── 2_Strategy_Analysis.py     # Tyre strategy and pit stops
│   ├── 3_Team_Analysis.py         # Team and teammate comparison
│   └── 4_Race_Overview.py         # Race summary and comparisons
├── src/
│   ├── analytics/                 # Driver, strategy, and team analysis
│   ├── data/                      # FastF1 loading and cache setup
│   ├── services/                  # FastF1, API, weather, and asset services
│   ├── ui/                        # Shared Streamlit UI components
│   ├── utils/                     # Formatting, validation, and lap filters
│   └── visualization/             # Reusable plots
├── data/cache/                    # Local FastF1 cache; ignored by Git
├── notebooks/                     # Exploration and analysis notebooks
├── tests/                         # Regression tests
├── .streamlit/config.toml         # Local Streamlit theme and server settings
├── requirements.txt               # Pinned Python dependencies
└── LICENSE
```

## Data sources

- [FastF1](https://github.com/theOehrly/Fast-F1) for session timing, lap, tyre, weather, and telemetry data
- Jolpica/Ergast-compatible endpoints for driver metadata and standings where used by the services layer
- Formula1.com assets for driver images where available

## Development checks

```bash
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m compileall -q app.py src pages tests
```

## License

MIT
