import pandas as pd


def remove_outlier_laps(laps, max_lap_time=300):
    # Remove laps with unrealistic lap times.

    if laps.empty or "Lap Time (s)" not in laps.columns:
        return laps.copy()

    return laps[laps["Lap Time (s)"] < max_lap_time].copy()



