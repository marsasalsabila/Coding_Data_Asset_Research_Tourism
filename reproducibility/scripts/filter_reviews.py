"""Apply the eight-keyword filter to an author-supplied CSV, not to a redistributed dataset."""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atr_repro.analysis import KEYWORDS, filter_sustainability

p = argparse.ArgumentParser()
p.add_argument("input_csv")
p.add_argument("--text-column", required=True)
p.add_argument("--output", default="reproducibility/outputs/filtered_reviews.csv")
args = p.parse_args()
frame = pd.read_csv(args.input_csv)
if args.text_column not in frame:
    raise ValueError("Missing text column: " + args.text_column)
mask = filter_sustainability(frame[args.text_column])
path = Path(args.output)
path.parent.mkdir(parents=True, exist_ok=True)
frame.loc[mask].to_csv(path, index=False)
print(json.dumps({
    "total_rows": len(frame),
    "non_null_text_rows": int(frame[args.text_column].notna().sum()),
    "selected_rows": int(mask.sum()),
    "keywords": KEYWORDS,
    "output": str(path)
}, indent=2))
