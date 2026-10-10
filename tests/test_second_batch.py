import unittest
from unittest.mock import patch


class SecondBatchTests(unittest.TestCase):
    def test_driver_image_parser_returns_empty_for_invalid_html(self):
        from src.services.formula1_assets import parse_driver_images

        self.assertEqual(parse_driver_images("<html>no driver assets</html>"), {})

    def test_session_loader_raises_actionable_error_on_fastf1_failure(self):
        from src.data.loader import SessionLoadError, load_session

        load_session.clear()
        with patch("src.data.loader.fastf1.get_session", side_effect=RuntimeError("offline")):
            with self.assertRaisesRegex(SessionLoadError, "Unable to load F1 session"):
                load_session(2025, "Monza", "R")


if __name__ == "__main__":
    unittest.main()
