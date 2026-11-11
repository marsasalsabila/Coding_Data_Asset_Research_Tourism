# Reproducibility utilities

These additional tools support inspection of the **existing eight notebooks** at the repository root. They are not replacements for the original simulation equations and are not themselves a reproduction of Figures 5–8.

## Install and test

From the repository root:

```bash
python -m pip install -r reproducibility/requirements.txt
python -m unittest discover -s reproducibility/tests -v
```

## Examples

```bash
# Inventory existing notebook filenames and SHA-256 values without execution
python reproducibility/scripts/inventory_notebooks.py

# Apply the eight-substring sustainability filter to authorized CSV data
python reproducibility/scripts/filter_reviews.py path/to/reviews.csv --text-column text_id --output reproducibility/outputs/filtered.csv

# Calculate MAPE from paired actual/predicted rows
python reproducibility/scripts/compute_mape.py reproducibility/examples/synthetic_fit.csv

# Find the first modeled visitor crossing, using synthetic fixture data
python reproducibility/scripts/find_crossings.py reproducibility/examples/synthetic_visitor_daily.csv --value-column visitors --threshold 2752

# Create a visual comparison from an existing CSV export
python reproducibility/scripts/plot_trajectories.py reproducibility/examples/synthetic_scenarios.csv
```

To execute a **trusted, previously reviewed** original notebook and save a separate output copy, first install `reproducibility/requirements-notebook-tools.txt`, then run:

```bash
python reproducibility/scripts/run_original_notebook.py Tourist_Population_Subsystem.ipynb --allow-execution
```

Notebook execution may access files and external services. Check for personal paths, API keys, private outputs, and permissions beforehand. Never commit real credentials or output datasets with incompatible redistribution terms.

All data files inside `examples/` are **synthetic demonstration data**. Passing tests confirms utility behavior only. It does **not** establish that notebook outputs precisely match manuscript figures or empirically validate the projected thresholds.

## Provenance and interpretation

- The original BERTopic analysis, seven Python subsystems, and subsequent sensitivity checks should retain distinct provenance.
- Do not describe seven individual numerical subsystem scripts as one fully coupled implementation.
- The cultural index of 60 and operational visitor benchmark of 2,752 visitors/day are distinct.
- Figure versions, input files, and date ranges must be confirmed before claiming precise plot replication.
