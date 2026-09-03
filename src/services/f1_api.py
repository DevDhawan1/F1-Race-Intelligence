import requests
import streamlit as st

BASE_URL = "https://api.jolpi.ca/ergast/f1"


@st.cache_data(show_spinner=False)
def load_all_drivers(season: int):
    """
    Load all drivers for a particular season.

    Returns
    -------
    dict
        {
            "NOR": {...},
            "VER": {...}
        }
    """

    url = f"{BASE_URL}/{season}/drivers.json?limit=100"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    drivers = {}

    driver_list = data["MRData"]["DriverTable"]["Drivers"]

    for driver in driver_list:

        code = driver.get("code")

        if not code:
            continue

        drivers[code] = {
            "driver_id": driver.get("driverId"),
            "code": code,
            "first_name": driver.get("givenName"),
            "last_name": driver.get("familyName"),
            "name": f"{driver.get('givenName')} {driver.get('familyName')}",
            "number": driver.get("permanentNumber"),
            "dob": driver.get("dateOfBirth"),
            "nationality": driver.get("nationality"),
            "wiki": driver.get("url"),
        }

    return drivers


def get_driver_metadata(driver_code: str, season: int):
    """
    Return metadata for one driver.
    """

    drivers = load_all_drivers(season)

    return drivers.get(driver_code)


def get_high_res_headshot(url: str) -> str:
    """
    Convert Formula1 thumbnail URL to a high-resolution portrait.
    """

    if not url:
        return None

    return url.replace(".transform/1col/", ".transform/12col/")


@st.cache_data(show_spinner=False)
def load_driver_standings(season: int):
    """
    Load driver championship standings for a season.
    """

    url = f"{BASE_URL}/{season}/driverstandings.json?limit=100"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    standings_lists = (
        data["MRData"]
        ["StandingsTable"]
        ["StandingsLists"]
    )

    if not standings_lists:
        return {}

    standings = standings_lists[0]["DriverStandings"]

    result = {}

    for driver in standings:

        code = driver["Driver"].get("code")

        if not code:
            continue

        constructors = driver.get("Constructors", [])

        team = constructors[0] if constructors else {}

        result[code] = {
            "position": int(driver["position"]),
            "points": float(driver["points"]),
            "wins": int(driver["wins"]),
            "team": team.get("name"),
            "team_id": team.get("constructorId"),
        }

    return result


def get_driver_standings(driver_code: str, season: int):
    """
    Return championship information for one driver.
    """

    standings = load_driver_standings(season)

    return standings.get(driver_code)






