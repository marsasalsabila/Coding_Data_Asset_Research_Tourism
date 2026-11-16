# Assumption-conditioned Bromo Monte Carlo — 13 November 2026

## Evidence status and scope

**Exploratory model-assumption stress test, not empirical uncertainty calibration or a reconstructed seven-subsystem Monte Carlo.** The program tests two indicators separately: (i) annual-average admissions/day from the observed 2024 full-year domestic 465,770 and international 19,926 counts divided by 366 days, and (ii) a hypothetical cultural-sustainability stock initialized at 80 on 1 January 2025, with the same expenditure/revitalization rules used in approved Fig. 8b.

The two scenarios are business-as-usual (BAU) and a combined intervention. The 2026 intervention applies a domestic price factor 1.08, a foreign factor 1.25, and a linear demand-response elasticity assumption; from 2026, modeled demand grows at its intervention growth rate. Cultural-stock changes reflect assumed visitor pressure, natural erosion, and financial conservation effort from a **hypothetical modeled resource account**, not from an officially appropriated national-park budget.

**Event definitions:** first **year** with annual-*mean* admissions >= **2,752 per day**; first **calendar-year-end** cultural index < **60**. No simulated ecological-health/80% crossing is asserted. The 2,752 benchmark is a historical *operational* quota, not verified ecological carrying capacity. Missing crossings through 2045 are stored as **-1**, counted separately, and never silently assigned 2046.

## Distributions and numerical protocol

Seed **20261113**; **10,000** independent parameter draws; projections **2025–2045**; NumPy PCG64 default generator. Primary distributions are triangular with mode at the approved point scenario. All draws are independent because joint empirical dependence information is unavailable. The alternative distribution is uniform over exactly the same bounds, revealing how sensitive uncertainty summaries are to the chosen shape.

| Input | Central point | Assumed sampling bounds | Why sampled |
|---|---:|---:|---|
| BAU annual visitor growth | 4.68% | 4.212–5.148% (±10%) | Unverified annual-growth assumption |
| Intervention annual visitor growth | 3.50% | 3.150–3.850% (±10%) | Unverified policy-response trend |
| Linear price-demand elasticity | -0.504 | -0.6048 to -0.4032 (±20% magnitude) | No Bromo-specific statistical estimate |
| Initial cultural index (2025) | 80 | 76–84 (±5%) | Model-defined cultural baseline |
| Annual cultural natural erosion | 0.5% | 0.4–0.6% (±20%) | Model assumption |
| Visitor-pressure coefficient | 4.5e-6 | 3.6e-6 to 5.4e-6 (±20%) | Model assumption |
| Cost per cultural-index point | IDR 350 million | 280–420 million (±20%) | Model assumption |
| BAU conservation spending share | 0.5% | 0.4–0.6% (±20%) | Hypothetical budget rule |
| Intervention conservation spending share (2026+) | 2.5% | 2.0–3.0% (±20%) | Hypothetical budget rule |

Held constant: historical 2024 admissions; 2,752 benchmark; 60 cultural index; blended hypothetical ticket prices (5/7 weekday, 2/7 holiday, IDR 54,000/79,000 domestic, IDR 255,000 foreign); hypothetical 85% receipts-to-budget-account multiplier; starting financial stock IDR 3,976,500,000; model spending absorption 90% annual; linear domestic 8% and foreign 25% price changes. The parameter ranges are **chosen for stress-testing**; they are not observational confidence limits or probabilistic priors fitted to Bromo.

The cultural bookkeeping uses year-constant annual-average admissions and ticket-receipt inputs but updates the modeled cultural and financial stocks on each calendar day using the same daily-step equations as the Fig. 8 exercise. Cultural crossing dates are assessed at **year-end**, not interpolated to fictional exact days.

## Executed results — triangular, 10,000 draws

| Event | Crossed through 2045 | Did not cross | Conditional 5th / median / 95th crossing year |
|---|---:|---:|---|
| BAU visitor admissions >= 2,752/day | 10,000 (100%) | 0 | **2039 / 2040 / 2042** |
| Intervention visitor admissions >= 2,752/day | 824 (8.24%) | 9,176 (91.76%) | **2045 / 2045 / 2045** |
| BAU year-end cultural index < 60 | 10,000 (100%) | 0 | **2031 / 2032 / 2034** |
| Intervention year-end cultural index < 60 | 1,162 (11.62%) | 8,838 (88.38%) | **2039 / 2043 / 2045** |

The year quantiles describe **only simulations that cross** the chosen threshold. They are not unconditional 90% intervals, calibrated likelihoods, or predictive confidence intervals for real-world events.

## Distribution-shape robustness check — uniform, 10,000 draws

| Event | Crossed through 2045 | Did not cross | Conditional 5th / median / 95th crossing year |
|---|---:|---:|---|
| BAU visitor threshold | 10,000 (100%) | 0 | 2039 / 2040 / 2042 |
| Intervention visitor threshold | 1,933 (19.33%) | 8,067 (80.67%) | 2045 / 2045 / 2045 |
| BAU cultural threshold | 10,000 (100%) | 0 | 2031 / 2032 / 2034 |
| Intervention cultural threshold | 1,978 (19.78%) | 8,022 (80.22%) | 2037 / 2041 / 2045 |

The difference between **8.24% and 19.33%**, and between **11.62% and 19.78%**, demonstrates sensitivity to assumed distribution shapes. Do **not** present those fractions as objective probabilities for Bromo.

## Internal reproduction checks

Deterministic point case (set \`stochastic=False\`) matches the approved Fig. 6a and Fig. 8b: BAU visitor threshold **2040**; BAU culture index <60 **2032**; intervention not crossing either threshold through **2045**. At 2045, annual-average BAU admissions **3,467.54/day**, intervention **2,642.94/day**; BAU cultural index **10.354**, intervention **70.367**.

The previously approved **25-case deterministic grid** from Section 4.7 varied growth *and the operational reference level*, yielding **2038–2043**. This Monte Carlo keeps the operational benchmark **fixed at 2,752** and samples growth and other assumptions; its 2039–2042 conditional band is therefore not a contradiction. Both analyses must be distinguished.

## Reproduce

From the root of this repository:

\`\`\`bash
pip install -r reproducibility/requirements.txt
python -m unittest discover -s reproducibility/tests -v
python reproducibility/scripts/bromo_monte_carlo_assumptions.py --n 10000 --seed 20261113 --distribution triangular
python reproducibility/scripts/bromo_monte_carlo_assumptions.py --n 10000 --seed 20261113 --distribution uniform --output-dir reproducibility/outputs/monte-carlo-uniform
\`\`\`

Or open \`reproducibility/notebooks/ATR_Bromo_Monte_Carlo_2026-11-13.ipynb\` and execute all cells. The command produces one per-draw CSV, one annual trajectory-band CSV, one summary JSON, and a publication-quality **300 dpi Matplotlib figure**. No raw visitor reviews, private data, or tokens are required.

## Required manuscript, supplement, and reviewer-response alignment

- **Methods, Section 3.7 or 3.9:** explicitly distinguish the original deterministic scenario analysis, the 25-case growth/benchmark grid, and this new **assumed-distribution Monte Carlo**; specify sample count, seed, sampled inputs, distribution shapes, crossing/noncrossing logic, and nonempirical status.
- **Results, Section 4.7:** retain the approved BERTopic evidence and deterministic 25-case result, then add *separately labeled* Monte Carlo 2039–2042 BAU visitor and 2031–2034 BAU culture conditional bands. Always mention the **91.76% and 88.38% noncrossing fractions** for intervention before interpreting conditional years; clarify the large dependence on sampling distribution.
- **Discussion 5.1 and limitations 5.5:** conditional interval robustness of assumed scenarios, not proof that the model predicts Bromo's ecological or cultural future; observational data and posterior parameter calibration remain absent.
- **Supplementary Material 7:** update stale **S7.2, S7.3, S7.5** tables to the approved figures (not the old August 2038, May 2031, intervention June 2045, revenue and capacity assumptions), and add new Monte Carlo configuration/result tables after the existing sensitivity grid.
- **Supplementary Material 40:** replace the stale statement that *no Monte Carlo had been run* with *assumption-conditioned Monte Carlo has been run for annual-mean admissions and an independently specified cultural index; original fully coupled model's empirical MC is not established*.
- **Response to Reviewer 4, R4.1:** acknowledge the partial answer. A 10,000-draw *assumption-conditioned* Monte Carlo now quantifies sensitivity of the two separately modeled event years; no empirical 90% prediction interval, independent parameter estimation, coupled solver, or ecological 80%-threshold event is claimed.
- **Figures 6 and 8:** retain approved point-scenario plots. New Monte Carlo envelope is a **separate supplementary figure**, not silently relabeled Fig. 6 or Fig. 8.

**Important caveat:** Do not write “95% confidence interval,” “90% probability that actual Bromo capacity is exceeded,” “model validated,” or “original seven-subsystem Monte Carlo.” These conclusions are not supported.
