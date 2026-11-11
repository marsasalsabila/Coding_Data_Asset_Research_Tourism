"""Find first threshold crossing in exported model output CSV."""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.analysis import first_crossing

p = argparse.ArgumentParser()
p.add_argument("input_csv")
p.add_argument("--date-column", default="date")
p.add_argument("--value-column", required=True)
p.add_argument("--threshold", type=float, required=True)
p.add_argument("--direction", choices=["above", "below"], default="above")
p.add_argument("--smoothing-days", type=int, default=0)
args = p.parse_args()
data = pd.read_csv(args.input_csv)
print(
    first_crossing(data, args.date_column, args.value_column,
                   args.threshold, args.direction, args.smoothing_days)
    or "No crossing in supplied data"
)
