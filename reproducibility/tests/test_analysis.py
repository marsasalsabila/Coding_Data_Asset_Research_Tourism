import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.analysis import filter_sustainability, first_crossing, mape

class AnalyticalUtilitiesTests(unittest.TestCase):
    def test_substring_filter(self):
        results = filter_sustainability(["budaya", "WISATA RAMAH", "pantai", "", None])
        self.assertEqual(results.tolist(), [True, True, False, False, False])

    def test_mape(self):
        self.assertAlmostEqual(mape([100, 200], [90, 220]), 10.0)

    def test_zero_denominator(self):
        with self.assertRaises(ValueError):
            mape([0], [1])

    def test_first_above(self):
        frame = pd.DataFrame({"date": ["2023-01-01", "2023-01-02"], "visitors": [1, 5]})
        self.assertEqual(first_crossing(frame, "date", "visitors", 3), "2023-01-02")

    def test_first_below(self):
        frame = pd.DataFrame({"date": ["2023-01-01", "2023-01-02"], "culture": [80, 60]})
        self.assertEqual(first_crossing(frame, "date", "culture", 60, "below"), "2023-01-02")

    def test_no_crossing(self):
        frame = pd.DataFrame({"date": ["2023-01-01"], "visitors": [1]})
        self.assertIsNone(first_crossing(frame, "date", "visitors", 3))

if __name__ == "__main__":
    unittest.main()
