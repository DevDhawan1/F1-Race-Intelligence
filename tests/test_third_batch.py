import unittest
from datetime import timedelta


class ThirdBatchTests(unittest.TestCase):
    def test_format_lap_time_handles_valid_and_invalid_values(self):
        from src.utils.formatting import format_lap_time

        self.assertEqual(format_lap_time(84.062), "1:24.062")
        self.assertEqual(format_lap_time(None), "-")
        self.assertEqual(format_lap_time("not-a-time"), "-")

    def test_format_duration_handles_timedelta_and_seconds(self):
        from src.utils.formatting import format_duration

        self.assertEqual(format_duration(timedelta(seconds=92)), "1m 32s")
        self.assertEqual(format_duration(3661), "1h 1m 1s")
        self.assertEqual(format_duration(None), "-")


if __name__ == "__main__":
    unittest.main()
