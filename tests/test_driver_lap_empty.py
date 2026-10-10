import unittest

import pandas as pd


class EmptyLapAnalysisTests(unittest.TestCase):
    def test_driver_lap_analysis_returns_empty_when_lap_schema_is_unavailable(self):
        from src.analytics.driver_analysis import driver_lap_analysis

        session = type("Session", (), {"laps": pd.DataFrame()})()

        result = driver_lap_analysis(session, "VER")

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
