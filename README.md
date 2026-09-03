# F1 Race Intelligence

A Streamlit-based Formula 1 race analytics dashboard powered by FastF1.

## Features

- **Dashboard** — Session selection, live weather, podium, circuit map
- **Driver Analysis** — Lap times, sectors, speed traps, position changes, tyre usage
- **Strategy Analysis** — Stint breakdown, pit stops, compound comparison, pace evolution
- **Team Analysis** — Teammate comparison, team pace, tyre strategy, performance summary
- **Race Overview** — Top 10 finishers, position changes, team standings, fastest laps

## Quick Start (Local)

```bash
# Clone and enter directory
git clone <repo-url>
cd F1-Race-Intelligence

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Project Structure

```
├── app.py                    # Entry point & navigation
├── pages/
│   ├── 0_Dashboard.py        # Session overview, podium, weather
│   ├── 1_Driver_Analysis.py  # Driver deep-dive
│   ├── 2_Strategy_Analysis.py# Tyre strategy, pit stops
│   ├── 3_Team_Analysis.py    # Team & teammate comparison
│   └── 4_Race_Overview.py    # Race summary, pace, fastest laps
├── src/
│   ├── analytics/            # Core analysis functions (cached)
│   ├── services/             # FastF1 API, driver profiles, weather
│   ├── ui/                   # Reusable UI components
│   └── utils/                # Formatters, lap filters
├── .streamlit/config.toml    # Theme & server config
├── requirements.txt
├── LICENSE
└── README.md
```

## Data Source

- [FastF1](https://github.com/theOehrly/FastF1) — F1 telemetry & timing data
- Ergast API — Historical race results (via FastF1)

## License

MIT