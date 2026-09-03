from datetime import date

from src.services.f1_api import (
    get_driver_metadata,
    get_driver_standings,
)
from src.services.formula1_assets import get_driver_image


def get_driver_profile(driver_code, season):
    """
    Build a complete driver profile for the UI.
    """

    driver = get_driver_metadata(
        driver_code,
        season,
    )

    if driver is None:
        return None

    standings = get_driver_standings(
        driver_code,
        season,
    )

    # --------------------------------------------------
    # Formula 1 image slug
    # --------------------------------------------------

    slug = (driver["first_name"][:3] + driver["last_name"][:3] + "01").lower()

    # --------------------------------------------------
    # Age
    # --------------------------------------------------

    dob = date.fromisoformat(driver["dob"])

    today = date.today()

    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # --------------------------------------------------
    # Return profile
    # --------------------------------------------------

    return {
        "name": driver["name"],
        "first_name": driver["first_name"],
        "last_name": driver["last_name"],
        "nationality": driver["nationality"],
        "number": driver["number"],
        "dob": driver["dob"],
        "age": age,
        "team": (standings["team"] if standings else None),
        "team_id": (standings["team_id"] if standings else None),
        "position": (standings["position"] if standings else None),
        "points": (standings["points"] if standings else None),
        "wins": (standings["wins"] if standings else None),
        "image": get_driver_image(slug),
    }


def get_session_driver_stats(session, driver_code):
    """
    Return driver statistics for the currently loaded FastF1 session.
    """

    if session is None:
        return None

    results = session.results

    if results is None or results.empty:
        return None

    driver_results = results[results["Abbreviation"] == driver_code]

    if driver_results.empty:
        return None

    result = driver_results.iloc[0]

    def clean_value(value):
        if value is None:
            return None

        try:
            if value != value:
                return None
        except Exception:
            pass

        return value

    return {
        "position": clean_value(result.get("Position")),
        "grid_position": clean_value(result.get("GridPosition")),
        "points": clean_value(result.get("Points")),
        "laps": clean_value(result.get("Laps")),
        "status": clean_value(result.get("Status")),
        "q1": clean_value(result.get("Q1")),
        "q2": clean_value(result.get("Q2")),
        "q3": clean_value(result.get("Q3")),
        "fastest_lap": clean_value(result.get("FastestLap")),
        "fastest_lap_time": clean_value(result.get("FastestLapTime")),
    }



