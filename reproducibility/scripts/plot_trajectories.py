"""Plot trajectory CSVs. Does not regenerate missing simulation equations."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

p = argparse.ArgumentParser()
p.add_argument("input_csv")
p.add_argument("--date-column", default="date")
p.add_argument("--value-column", default="value")
p.add_argument("--group-column", default="scenario")
p.add_argument("--title", default="Scenario trajectories (supplied CSV)")
p.add_argument("--ylabel", default="Output (source-defined units)")
p.add_argument("--output", default="reproducibility/outputs/scenario_plot.png")
args = p.parse_args()
data = pd.read_csv(args.input_csv)
for column in (args.date_column, args.value_column, args.group_column):
    if column not in data:
        raise ValueError("Missing column: " + column)
data[args.date_column] = pd.to_datetime(data[args.date_column])
figure, axis = plt.subplots(figsize=(9, 4.75))
for name, group in data.sort_values(args.date_column).groupby(args.group_column):
    axis.plot(group[args.date_column], group[args.value_column], label=str(name))
axis.set(title=args.title, xlabel="Date", ylabel=args.ylabel)
axis.legend()
figure.autofmt_xdate()
figure.tight_layout()
out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
figure.savefig(out, dpi=180)
plt.close(figure)
print("Created:", out)
