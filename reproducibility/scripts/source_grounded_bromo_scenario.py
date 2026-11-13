"""Export audited observed counts and a NEW, illustrative Bromo annual-mean scenario."""
import argparse
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.bromo_sources import (
    OBSERVED_VISITS, OBSERVED_VISITS_2025_H1, OBSERVED_PNBP_IDR,
    OPERATIONAL_QUOTA_2024_PER_DAY, daily_annual_average,
    daily_2025_first_half_average, scenario_row, first_annual_mean_quota_reference_year
)

def export(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", default="reproducibility/outputs/source-grounded")
    p.add_argument("--end-year", type=int, default=2045)
    p.add_argument("--bau-growth", type=float, default=0.0468,
                   help="assumption, not empirically estimated")
    p.add_argument("--intervention-growth", type=float, default=0.035,
                   help="assumption, not empirically estimated")
    p.add_argument("--assumed-elasticity", type=float, default=-0.504,
                   help="assumption, not empirically estimated")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()
    if args.end_year < 2025:
        p.error("--end-year must be >= 2025")
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    observed = [
        {"period": "2023_FULL_YEAR", **OBSERVED_VISITS[2023]},
        {"period": "2024_FULL_YEAR", **OBSERVED_VISITS[2024]},
        {"period": "2025_JAN_JUN_ONLY", **OBSERVED_VISITS_2025_H1},
    ]
    export(output/"observed_bromo_visits.csv", observed)
    rows = [scenario_row(year, bau_growth=args.bau_growth,
                         intervention_growth=args.intervention_growth,
                         assumed_elasticity=args.assumed_elasticity)
            for year in range(2025, args.end_year+1)]
    export(output/"provisional_annual_mean_scenarios.csv", rows)
    print("OBSERVED annual arithmetic averages 2023 / 2024:",
          round(daily_annual_average(2023),2), round(daily_annual_average(2024),2))
    print("OBSERVED 2025 JAN-JUN average (not 2025 annual):",
          round(daily_2025_first_half_average(),2))
    print("Observed PNBP, NOT modeled ticket receipts:", OBSERVED_PNBP_IDR)
    for key in ("bau_annual_mean_admissions_per_day",
                "intervention_annual_mean_admissions_per_day"):
        print(key, "first annual-mean quota-reference YEAR:",
              first_annual_mean_quota_reference_year(rows,key))
    if not args.no_plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(11,6))
        years=[r["year"] for r in rows]
        ax.plot(years,[r["bau_annual_mean_admissions_per_day"] for r in rows],
                label="Assumed BAU annual mean")
        ax.plot(years,[r["intervention_annual_mean_admissions_per_day"] for r in rows],
                label="Assumed pricing + growth intervention annual mean")
        ax.scatter([2023,2024],[daily_annual_average(2023),daily_annual_average(2024)],
                   label="Observed full-year admission means",zorder=5)
        ax.axhline(OPERATIONAL_QUOTA_2024_PER_DAY,linestyle=":",
                   label="2024 operational quota reference; NOT ecological capacity")
        ax.set(xlabel="Year",ylabel="Annual-mean admissions/day (observed proxy or scenario)",
               title="Bromo exploratory annual-mean admission scenarios — NOT original manuscript figure")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(output/"bromo_provisional_visitor_scenario.png",dpi=180)
        plt.close(fig)
    print("Wrote source records and scenario exports:",output)

if __name__ == "__main__":
    main()
