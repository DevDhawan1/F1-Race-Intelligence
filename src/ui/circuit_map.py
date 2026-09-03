import matplotlib.pyplot as plt
import io
import base64


def create_circuit_map(session):
    """
    Generate a circuit layout from FastF1 telemetry
    and return it as a base64 PNG string.
    """

    try:
        laps = session.laps

        if laps is None or laps.empty:
            return None

        fastest_lap = laps.pick_fastest()

        if fastest_lap is None:
            return None

        telemetry = fastest_lap.get_telemetry()

        if telemetry is None or telemetry.empty:
            return None

        if "X" not in telemetry.columns or "Y" not in telemetry.columns:
            return None

        x = telemetry["X"]
        y = telemetry["Y"]

        fig, ax = plt.subplots(
            figsize=(5, 3.8),
            dpi=150,
        )

        ax.plot(
            x,
            y,
            linewidth=3,
        )

        ax.set_aspect(
            "equal",
            adjustable="datalim",
        )

        ax.axis("off")

        # Transparent background
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        fig.subplots_adjust(
            left=0,
            right=1,
            top=1,
            bottom=0,
        )

        # Convert matplotlib figure to PNG
        buffer = io.BytesIO()

        fig.savefig(
            buffer,
            format="png",
            transparent=True,
            bbox_inches="tight",
            pad_inches=0,
        )

        plt.close(fig)

        buffer.seek(0)

        # Convert image to base64
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return image_base64

    except Exception:
        return None



