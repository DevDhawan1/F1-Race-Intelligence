import unittest

import pandas as pd


class EmptyPositionChangesTests(unittest.TestCase):
    def test_position_analysis_returns_empty_without_lap_schema(self):
        from src.analytics.driver_analysis import driver_summary, position_changes

        session = type("Session", (), {"laps": pd.DataFrame(), "results": pd.DataFrame()})()

        self.assertTrue(driver_summary(session).empty)
        self.assertTrue(position_changes(session).empty)


if __name__ == "__main__":
    unittest.main()
