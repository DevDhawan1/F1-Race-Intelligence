# F1 Race Intelligence

F1 Race Intelligence is a local-only Streamlit dashboard for exploring Formula 1 sessions with FastF1. It is designed for local development and analysis, where FastF1 can download and cache the session data required by the dashboard.

This repository is the local Streamlit version of the project. A separate hosted/web application may be developed later with a different data source and frontend architecture.

## Features

- **Dashboard** - Session selection, podium, weather, highlights, and circuit map
- **Driver Analysis** - Lap pace, sectors, speed traps, position changes, and tyre usage
- **Strategy Analysis** - Stints, pit stops, compound performance, degradation, and race pace
- **Team Analysis** - Teammate comparison, team pace, tyre strategy, and team summaries
- **Race Overview** - Finishers, position changes, team standings, compound performance, pit stops, and fastest laps

## Run locally

```bash
python -m venv .venv

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

## Local-only data behavior

- The session selector supports seasons from 2018 onward. Seasons before 2018 are not currently exposed by the app.
- FastF1 downloads session data from its upstream timing sources when a session is selected.
- Downloaded files are cached locally under `data/cache/`.
- The cache is intentionally ignored by Git and is not deployed with this repository.
- Detailed lap, tyre, weather, and telemetry analysis depends on the data FastF1 successfully retrieves for each session.
- If FastF1 returns partial data, the affected sections display a clear no-data state instead of stopping the whole app.

The app is intended to be run locally. The previous Streamlit Cloud deployment is not part of the supported workflow because FastF1 data loading is not reliable there for this project.

## Project structure

```text
|- app.py                         # Streamlit entry point and navigation
|- pages/
|  |- 0_Dashboard.py              # Session overview
|  |- 1_Driver_Analysis.py        # Driver deep-dive
|  |- 2_Strategy_Analysis.py      # Tyre strategy and pit stops
|  |- 3_Team_Analysis.py          # Team and teammate comparison
|  `- 4_Race_Overview.py          # Race summary and comparisons
|- src/
|  |- analytics/                  # Driver, strategy, and team analysis
|  |- data/                       # FastF1 loading and cache setup
|  |- services/                   # FastF1, API, and asset services
|  |- ui/                         # Shared Streamlit UI components
|  |- utils/                      # Formatting and lap filters
|  `- visualization/              # Visualization package marker
|- data/cache/                    # Local FastF1 cache; ignored by Git
|- notebooks/                     # FastF1 exploration and analysis notebooks
|  `- setup.py                    # Portable notebook import setup
|- tests/                         # Regression tests
|- .streamlit/config.toml         # Local Streamlit theme and server settings
|- requirements.txt               # Pinned Python dependencies
`- LICENSE
```

The notebooks are exploratory documentation for the FastF1 investigation. They are not required when running the Streamlit app. The application runtime starts at `app.py` and uses the modules under `src/`.

## Data sources

- [FastF1](https://github.com/theOehrly/Fast-F1) for session timing, lap, tyre, weather, and telemetry data
- Jolpica/Ergast-compatible endpoints for driver metadata and standings where used by the services layer
- Formula1.com assets for driver images where available

## Development checks

```bash
.venv\\Scripts\\python.exe -m unittest discover -s tests -v
.venv\\Scripts\\python.exe -m compileall -q app.py src pages tests
```

## License

MIT
