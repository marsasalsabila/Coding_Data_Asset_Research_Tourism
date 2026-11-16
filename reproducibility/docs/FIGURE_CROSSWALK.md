# Figure-to-code crosswalk — revision of 14 November 2026

This table describes the **current manuscript revision**. The seven original root-level subsystem notebooks have been preserved as legacy source artifacts and should not be described as a single coupled implementation. The revised Figures 6–8 come from separate, explicitly parameterized Python scenario notebooks now included in `reproducibility/notebooks/` on the public **main** branch. The executed Monte Carlo notebook is also available there. These are distinct from the seven preserved historical subsystem notebooks and do not constitute a single empirically calibrated coupled solver.

| Manuscript item | Source and status | Required interpretation |
|---|---|---|
| Fig. 1: research workflow | Schematic / Methods | Themes feed conceptual mapping, not Bromo numerical parameter estimation |
| Fig. 2: topic model | `BERTopic.ipynb` | Topic representations and source corpus must be checked |
| Fig. 3: causal-loop diagram | Vensim diagram | 26 original candidate links and six later explanatory connectors, see Supplementary S3.6 |
| Fig. 4: stock-and-flow | Vensim diagram | Conceptual diagram, not an executable fully coupled simulation |
| Fig. 5: recorded observations | Historical Bromo source records | Observed 2023–2024 admissions and non-tax state revenue, **not a MAPE plot** |
| Fig. 6: visitor admissions / waste | [`ATR_Fig6_Socioecological_Executed.ipynb`](../notebooks/ATR_Fig6_Socioecological_Executed.ipynb) in this repository | Annual-mean admissions and assumed 0.5 kg/admission waste rate, not a legacy population-stock rerun |
| Fig. 7: ticket receipts / facilities | [`ATR_Fig7_Revenue_Facilities_Executed.ipynb`](../notebooks/ATR_Fig7_Revenue_Facilities_Executed.ipynb) in this repository | Hypothetical gross receipts and model-equivalent facility capacity, not observed PNBP or authorized budgets |
| Fig. 8: service / culture / vendors | [`ATR_Fig8_Sociocultural_Economy_Executed.ipynb`](../notebooks/ATR_Fig8_Sociocultural_Economy_Executed.ipynb) in this repository | Separate assumptions for service/culture/vendor dynamics, not empirically validated site indicators |
| Supplemental Monte Carlo | [`ATR_Bromo_Monte_Carlo_Executed.ipynb`](../notebooks/ATR_Bromo_Monte_Carlo_Executed.ipynb), [`ATR_Bromo_Monte_Carlo_2026-11-13.ipynb`](../notebooks/ATR_Bromo_Monte_Carlo_2026-11-13.ipynb), and `reproducibility/scripts/bromo_monte_carlo_assumptions.py` | Assumption-conditioned 10,000 runs, seed 20261113. Bounds are not calibrated confidence intervals |

## Current 2026 revision

- The annual-average visitor-demand BAU series first reaches the assumed **2,752 admissions/day** operational reference in **2040**.
- The separately modeled cultural index first falls below the assumed **60** threshold at **year-end 2032**.
- Earlier values around **2031** and **August 2038** relate to other, earlier scenario versions or variable definitions. They should not be substituted for the current 2032/2040 claims.
- A seven-subsystem original-equation extreme-input test was carried out separately. In the original code, 17 of 21 cases passed and four revealed edge-case limitations. Candidate in-memory guards were tested without changing the original notebooks.
- Monte Carlo inputs have assumed independent bounded variation. Crossing times are conditional outcomes, not field forecasts.

## Replication boundary

The four executed figure-related notebooks have now been published on `main` with their saved outputs. File integrity was checked against recovered Library exports by matching Git blob hashes. **Public source availability is not the same as independent numerical replication**: third-party reviewers should run the notebooks in a clean environment, check dependencies and generated CSV/figure outputs, and confirm that the produced results match the submitted manuscript. GitHub Actions for unrelated utility tests do not establish figure-level replication.

| Executed notebook | SHA-256 of published file |
|---|---|
| Fig. 6 | `49c171d96f2da8cfa6c5dfc8ca32250c013a769e630a5bc50059d81ce8f6939f` |
| Fig. 7 | `e67833b4cdd67778dbb2fb270130a50782a4ffda3e77c05c7ed370ce7ebb52c1` |
| Fig. 8 | `d1193a9b8c85b532a3654b2bcb5fde98964c4b31a7dec71537117e9a7b0e0ad1` |
| Monte Carlo (executed) | `2eee74c2c5355cdc26361b97880de01b06183f92159ecba01fe9e769e88c2990` |
