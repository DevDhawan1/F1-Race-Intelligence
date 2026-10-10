import pandas as pd
import unittest


class FirstBatchTests(unittest.TestCase):
    def test_reset_loaded_session_when_selection_changes(self):
        from src.ui.session_selector import reset_loaded_session_on_change

        config = {
            "year": 2025,
            "circuit": "Monza (Italy)",
            "session": "Race",
            "loaded_session": object(),
        }

        reset_loaded_session_on_change(config, 2025, "Monza (Italy)", "Qualifying")

        self.assertIsNone(config["loaded_session"])

    def test_driver_slug_uses_explicit_mapping_and_fallback(self):
        from src.services.driver_service import driver_image_slug

        self.assertEqual(driver_image_slug("COL"), "colapinto01")
        self.assertEqual(
            driver_image_slug("VER", first_name="Max", last_name="Verstappen"),
            "maxver01",
        )

    def test_driver_selector_returns_none_for_empty_results(self):
        from src.ui.driver_selector import get_available_drivers

        self.assertEqual(get_available_drivers(None), [])
        self.assertEqual(get_available_drivers(pd.DataFrame()), [])
        self.assertEqual(get_available_drivers(pd.DataFrame({"Position": [1]})), [])

    def test_driver_selector_deduplicates_and_sorts_drivers(self):
        from src.ui.driver_selector import get_available_drivers

        results = pd.DataFrame({"Abbreviation": ["VER", "HAM", "VER"]})

        self.assertEqual(get_available_drivers(results), ["HAM", "VER"])


if __name__ == "__main__":
    unittest.main()
