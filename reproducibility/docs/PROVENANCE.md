# Computational provenance and interpretation

## Existing code

The eight notebooks in the repository root are the research artifacts available for inspection. This update does not alter their source bytes. The BERTopic notebook concerns the review corpus, while seven simulation notebooks treat destination subsystems separately.

## Additional code in this update

Files in `reproducibility/scripts/` and `reproducibility/src/` provide post-processing and diagnostic utilities. Their date outputs depend exclusively on supplied CSVs. The `examples/` records are synthetic fixtures and **must not** be cited as empirical Bromo data.

## Reproducibility workflow

1. Save the exact checked-in revision or commit SHA.
2. Record the SHA-256 hashes of the original notebook files using `inventory_notebooks.py`.
3. Document input files, observation windows, simulation intervals, Python version, and installed dependency versions.
4. Review original code and outputs for embedded secrets, private paths, or third-party data before sharing.
5. Execute original notebooks only after explicit opt-in. Save executed results as separate, ignored files.
6. Compare numerical CSV outputs and produced figure images to manuscript figures before claiming exact reproduction.

## Scope of inference

The 25-destination review corpus and the Bromo scenario simulations are separate analytical scopes. Review-based theme identification does not imply observed ecological causal effects. Conceptual causal-loop arrows and numerical equations are different types of model artifacts.

Reported MAPE results describe the specified historical comparisons and are not independent prospective validation. Thresholds such as cultural index 60, operational 2,752 visitors/day, and environmental reference 80% are different constructs and should not be conflated.

The original language-model exchanges should not be reconstructed as if they were authenticated historical prompts. Any new prompts or additional language-model experiments must be clearly labeled by their actual execution context.
