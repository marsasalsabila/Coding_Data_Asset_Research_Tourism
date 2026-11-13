"""Regression checks for Figures 6a/8b baseline and Monte Carlo assumptions."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from bromo_monte_carlo_assumptions import simulate,describe


class MonteCarloTests(unittest.TestCase):
    def test_baseline_reproduces_approved_crossings(self):
        draws, trajectory=simulate(n=1,seed=0,stochastic=False)
        summary=describe(draws)
        self.assertEqual(summary["bau_visitor"]["earliest_crossing_year"],2040)
        self.assertEqual(summary["bau_culture"]["earliest_crossing_year"],2032)
        self.assertEqual(summary["intervention_visitor"]["not_crossed_by_2045"],1)
        self.assertEqual(summary["intervention_culture"]["not_crossed_by_2045"],1)
        year2045=trajectory.loc[trajectory.year==2045]
        def value(scenario,indicator):
            return float(year2045.loc[
                (year2045.scenario==scenario)&(year2045.indicator==indicator),
                "median"].iloc[0])
        self.assertAlmostEqual(value("BAU","annual_mean_admissions_day"),3467.539642,places=3)
        self.assertAlmostEqual(value("Intervention","annual_mean_admissions_day"),2642.937895,places=3)
        self.assertAlmostEqual(value("BAU","culture_index_end_year"),10.354067,places=3)
        self.assertAlmostEqual(value("Intervention","culture_index_end_year"),70.366914,places=3)

    def test_reproducible_and_non_crossing_preserved(self):
        first,_=simulate(n=30,seed=123)
        second,_=simulate(n=30,seed=123)
        self.assertTrue(first.equals(second))
        for name in ["bau_visitor","intervention_visitor",
                     "bau_culture","intervention_culture"]:
            col=name+"_crossing_year"
            self.assertTrue(((first[col]==-1)|first[col].between(2025,2045)).all())
            d=describe(first)[name]
            self.assertEqual(d["crossed_by_2045"]+d["not_crossed_by_2045"],30)

    def test_uniform_alternative_uses_same_base_model(self):
        draws,_=simulate(n=30,seed=123,distribution="uniform")
        self.assertEqual(len(draws),30)
        self.assertTrue(draws["bau_growth"].between(.0468*.9,.0468*1.1).all())


if __name__=="__main__":
    unittest.main()
