"""Calculate grouped MAPE from an existing CSV of observed and modeled values."""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.analysis import mape

p = argparse.ArgumentParser()
p.add_argument("input_csv")
p.add_argument("--actual", default="actual")
p.add_argument("--predicted", default="predicted")
p.add_argument("--group", default="subsystem")
p.add_argument("--output")
args = p.parse_args()
df = pd.read_csv(args.input_csv)
for column in (args.actual, args.predicted):
    if column not in df:
        raise ValueError("Missing column: " + column)
if args.group in df:
    rows = [
        {args.group: name, "observations": len(group), "mape_percent": mape(group[args.actual], group[args.predicted])}
        for name, group in df.groupby(args.group, sort=False)
    ]
else:
    rows = [{"observations": len(df), "mape_percent": mape(df[args.actual], df[args.predicted])}]
result = pd.DataFrame(rows)
print(result.to_string(index=False))
if args.output:
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
