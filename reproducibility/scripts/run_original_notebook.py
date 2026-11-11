"""Opt-in execution of an existing original notebook without overwriting its source."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("notebook")
parser.add_argument("--allow-execution", action="store_true")
parser.add_argument("--timeout", type=int, default=900)
parser.add_argument("--working-dir")
args = parser.parse_args()
if not args.allow_execution:
    parser.error("Review notebook contents and pass --allow-execution to opt in")
try:
    import nbformat
    from nbclient import NotebookClient
except ImportError as exc:
    parser.error("Install requirements-notebook-tools.txt: " + str(exc))
source = Path(args.notebook).resolve()
allowed = {
    "Tourist_Population_Subsystem.ipynb",
    "Environmental_Sanitation_Subsystem.ipynb",
    "Tourism_Revenue_Subsystem.ipynb",
    "Tourism_Facilities_Availability_Subsystem.ipynb",
    "Tourism_Services_Subsystem.ipynb",
    "Cultural_Preservation_Subsystem.ipynb",
    "Economic_Subsystem_of_the_Local_Community_in_the_Tourism_Sector.ipynb",
}
if source.parent != Path.cwd().resolve() or source.name not in allowed or not source.is_file():
    parser.error("Supply an existing subsystem notebook from the repository root")
raw_sha = hashlib.sha256(source.read_bytes()).hexdigest()
notebook = nbformat.read(source, as_version=4)
working_directory = str(Path(args.working_dir).resolve()) if args.working_dir else str(source.parent)
client = NotebookClient(
    notebook, timeout=args.timeout, kernel_name="python3",
    resources={"metadata": {"path": working_directory}}
)
print("Executing source", source.name, "SHA-256", raw_sha)
client.execute()
destination = Path.cwd() / "reproducibility" / "outputs" / "executed"
destination.mkdir(parents=True, exist_ok=True)
output = destination / source.name
nbformat.write(notebook, output)
(destination / (source.stem + ".execution.json")).write_text(
    json.dumps({
        "source_name": source.name,
        "source_sha256": raw_sha,
        "executed_copy": str(output),
        "status": "completed_without_uncaught_error",
        "note": "Execution is not verification of correspondence with manuscript figures"
    }, indent=2), encoding="utf-8"
)
print("Executed copy:", output)
