import unittest
from datetime import datetime
from pathlib import Path

import pandas as pd


class FourthBatchTests(unittest.TestCase):
    def test_event_mapping_excludes_future_events(self):
        from src.ui.session_selector import get_event_mapping

        schedule = pd.DataFrame([
            {"Location": "Past", "Country": "X", "EventDate": datetime(2025, 1, 1)},
            {"Location": "Future", "Country": "Y", "EventDate": datetime(2030, 1, 1)},
        ])

        mapping = get_event_mapping(schedule, today=datetime(2026, 1, 1))

        self.assertIn("Past (X)", mapping)
        self.assertNotIn("Future (Y)", mapping)

    def test_project_python_files_compile_as_smoke_check(self):
        import py_compile

        files = [Path("app.py"), *Path("src").rglob("*.py"), *Path("pages").rglob("*.py")]
        for path in files:
            py_compile.compile(str(path), doraise=True)


if __name__ == "__main__":
    unittest.main()
