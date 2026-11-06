"""Extract embedded PNG outputs for visual comparison without notebook execution."""
import argparse
import base64
from pathlib import Path

import nbformat

p = argparse.ArgumentParser()
p.add_argument("notebook")
p.add_argument("--destination", default="reproducibility/outputs/extracted_figures")
args = p.parse_args()
notebook = nbformat.read(args.notebook, as_version=4)
destination = Path(args.destination)
destination.mkdir(parents=True, exist_ok=True)
count = 0
for cell_index, cell in enumerate(notebook.cells):
    if cell.cell_type != "code":
        continue
    for output_index, output in enumerate(cell.get("outputs", [])):
        figure_data = output.get("data", {}).get("image/png")
        if not figure_data:
            continue
        encoded = figure_data if isinstance(figure_data, str) else "".join(figure_data)
        image_bytes = base64.b64decode(encoded)
        target = destination / f"{Path(args.notebook).stem}_cell{cell_index:03d}_output{output_index:02d}.png"
        target.write_bytes(image_bytes)
        print(target)
        count += 1
print("Exported PNG outputs:", count)
