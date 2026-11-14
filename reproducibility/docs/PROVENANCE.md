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

## Manuscript-aligned revision notes (14 November 2026)

The current Fig. 5 shows observed Gunung Bromo admissions and reported non-tax state revenue for 2023–2024, not a historical MAPE chart. The annual-mean Fig. 6 threshold year is 2040 and the Fig. 8 assumed cultural-index threshold year is 2032, under current manuscript definitions. Older README statements with 2031 or August 2038 referred to earlier scenario versions and must not be treated as outputs of the current annual-mean notebook.

The latest scenario notebooks for Figs. 6–8 and the separate assumption-conditioned Monte Carlo experiment are delivered in a sanitized reproducibility bundle outside the repository. The Monte Carlo support script is versioned at `reproducibility/scripts/bromo_monte_carlo_assumptions.py`. That script is not empirical validation of the seven original subsystem scripts. Full public reproducibility will require uploading and versioning the latest sanitized figure notebooks and output CSVs as well.

A source-code extreme-condition screen was executed against seven original notebook engine cells (21 cases, 17 pass, 4 fail). Candidate guards were evaluated in-memory, leaving original notebook bytes unchanged. The guarded condition results must not be mistaken for changes incorporated into the published baseline code.

The original Gemini prompt is unavailable. The ten-run retrospective experiment used a reconstructed prompt, with limited thematic recurrence and low strict reference-network recovery. This evidence concerns prompt-output reproducibility, not causal or numerical model validation.
