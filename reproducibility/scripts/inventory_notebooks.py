"""Inspect original notebook structure and hashes without running code."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--directory", default=".")
p.add_argument("--write-manifest", default="reproducibility/docs/notebook_checksums.csv")
args = p.parse_args()
folder = Path(args.directory)
patterns = [
    re.compile(r"(?i)(?:api[_-]?key|secret|token|password)\s*[=:]\s*['\"][^'\"]{8,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}")
]
rows = []
for path in sorted(folder.glob("*.ipynb")):
    raw = path.read_bytes()
    try:
        doc = json.loads(raw)
        cells = doc.get("cells", [])
        if doc.get("nbformat", 0) < 4 or not isinstance(cells, list):
            raise ValueError("Notebook version or cells invalid")
        code = "\n".join(
            "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list)
            else cell.get("source", "")
            for cell in cells if cell.get("cell_type") == "code"
        )
        warnings = sum(bool(pattern.search(code)) for pattern in patterns)
        code_cells = sum(cell.get("cell_type") == "code" for cell in cells)
        output_cells = sum(bool(cell.get("outputs")) for cell in cells if cell.get("cell_type") == "code")
        status = "manual_review_required"
    except Exception as exc:
        code_cells = output_cells = warnings = 0
        status = "invalid_notebook: " + str(exc)
    rows.append({
        "filename": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "code_cells": code_cells,
        "code_cells_with_outputs": output_cells,
        "possible_secret_flags": warnings,
        "status": status
    })
out = Path(args.write_manifest)
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()) if rows else [
        "filename", "sha256", "bytes", "code_cells", "code_cells_with_outputs",
        "possible_secret_flags", "status"
    ])
    writer.writeheader()
    writer.writerows(rows)
print("Recorded", len(rows), "notebooks at", out)
print("Manual review remains necessary before republishing original notebooks.")
