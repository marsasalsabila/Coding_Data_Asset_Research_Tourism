import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.bromo_sources import (
    OBSERVED_VISITS, OBSERVED_VISITS_2025_H1, OBSERVED_PNBP_IDR,
    TARIFF_EFFECTIVE, TARIFF_IDR, audit_sources, daily_annual_average,
    daily_2025_first_half_average, scenario_row, first_annual_mean_quota_reference_year
)

class SourceAuditTests(unittest.TestCase):
    def test_reported_counts_reconcile(self):
        audit_sources()
        self.assertEqual(OBSERVED_VISITS[2023]["total"], 368507)
        self.assertEqual(OBSERVED_VISITS[2024]["domestic"], 465770)
        self.assertEqual(OBSERVED_VISITS[2024]["foreign"], 19926)
        self.assertEqual(OBSERVED_VISITS[2024]["total"], 485696)
        self.assertEqual(OBSERVED_VISITS_2025_H1["total"], 321732)

    def test_periods_and_leap_year(self):
        self.assertAlmostEqual(daily_annual_average(2024),485696/366)
        self.assertAlmostEqual(daily_annual_average(2023),368507/365)
        self.assertAlmostEqual(daily_2025_first_half_average(),321732/181)
        self.assertNotIn(2025,OBSERVED_VISITS)

    def test_pnbp_and_tariff(self):
        self.assertEqual(OBSERVED_PNBP_IDR[2024],21_150_000_000)
        self.assertEqual(TARIFF_EFFECTIVE.isoformat(),"2024-10-30")
        self.assertEqual(TARIFF_IDR["domestic_weekday"],54000)
        self.assertEqual(TARIFF_IDR["domestic_holiday"],79000)
        self.assertEqual(TARIFF_IDR["foreign"],255000)

    def test_scenarios_not_data(self):
        previous=scenario_row(2025)
        self.assertAlmostEqual(previous["bau_annual_mean_admissions_per_day"],
                               daily_annual_average(2024)*1.0468)
        self.assertAlmostEqual(previous["bau_annual_mean_admissions_per_day"],
                               previous["intervention_annual_mean_admissions_per_day"])
        changed=scenario_row(2026)
        self.assertLess(changed["intervention_annual_mean_admissions_per_day"],
                        changed["bau_annual_mean_admissions_per_day"])
        self.assertGreater(scenario_row(2026,assumed_elasticity=0)["intervention_annual_mean_admissions_per_day"],
                           changed["intervention_annual_mean_admissions_per_day"])

    def test_year_not_day(self):
        rows=[scenario_row(y) for y in range(2025,2046)]
        year=first_annual_mean_quota_reference_year(rows)
        self.assertTrue(year is None or isinstance(year,int))

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError): scenario_row(2024)
        with self.assertRaises(ValueError): scenario_row(2026,domestic_price_factor=0)
        with self.assertRaises(ValueError): scenario_row(2026,assumed_elasticity=-100)

if __name__=="__main__":
    unittest.main()
