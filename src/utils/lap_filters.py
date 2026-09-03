import pandas as pd


def remove_outlier_laps(laps, max_lap_time=300):
    # Remove laps with unrealistic lap times.

    return laps[laps["Lap Time (s)"] < max_lap_time].copy()



