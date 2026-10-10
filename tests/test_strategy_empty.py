import unittest

import pandas as pd


class EmptyStrategyTests(unittest.TestCase):
    def test_strategy_analytics_return_empty_frames_without_lap_data(self):
        from src.analytics.strategy_analysis import (
            compound_comparison,
            pit_stop_analysis,
            race_pace_evolution,
            stint_analysis,
            tyre_degradation,
        )

        session = type("Session", (), {"laps": pd.DataFrame()})()

        for analysis in (
            stint_analysis,
            tyre_degradation,
            pit_stop_analysis,
            race_pace_evolution,
            compound_comparison,
        ):
            with self.subTest(analysis=analysis.__name__):
                self.assertTrue(analysis(session).empty)


if __name__ == "__main__":
    unittest.main()
