import matplotlib.pyplot as plt

from src.analytics.strategy_analysis import tyre_degradation


def plot_tyre_degradation(session, driver):
    """
    Plot tyre degradation for a single driver.

    Parameters
    ----------
    session : fastf1.core.Session

    driver : str
        Driver abbreviation (e.g. "NOR", "VER")
    """

    tyre_df = tyre_degradation(session)

    driver_df = tyre_df[tyre_df["Driver"] == driver.upper()]

    if driver_df.empty:
        raise ValueError(f"No data found for driver '{driver}'.")

    plt.figure(figsize=(10, 6))

    for stint in sorted(driver_df["Stint"].unique()):

        stint_data = driver_df[driver_df["Stint"] == stint]

        compound = stint_data["Compound"].iloc[0]

        plt.plot(
            stint_data["Tyre Life"],
            stint_data["Lap Time (s)"],
            marker="o",
            linewidth=2,
            label=f"Stint {int(stint)} ({compound})",
        )

    plt.title(f"Tyre Degradation - {driver.upper()}")

    plt.xlabel("Tyre Life (laps)")

    plt.ylabel("Lap Time (seconds)")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()

