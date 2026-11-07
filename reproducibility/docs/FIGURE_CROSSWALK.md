# Figure-to-code crosswalk

This table indicates which **existing** notebooks are relevant when inspecting outputs discussed in the manuscript. It does not assert that the checked-in notebook revision exactly generated a particular published figure.

| Manuscript item | Relevant artifact | Required check |
|---|---|---|
| Figure 1: research workflow | Manuscript methods | Schematic, not a numerical notebook output |
| Figure 2: BERTopic results | `BERTopic.ipynb` | Topic representations, preprocessing, clustering settings, and source review identifiers |
| Figure 3: causal loop diagram | Conceptual Vensim diagram | Diagram source and directed-link provenance |
| Figure 4: stock-and-flow diagram | Conceptual Vensim diagram | Structure is not a complete coupled numerical solver |
| Figure 5: historical MAPE | Seven subsystem notebooks | Identify reference observations, baseline alignment and aggregation procedure |
| Figure 6a: visitor activity | `Tourist_Population_Subsystem.ipynb` | Confirm visitor variable, operational 2,752/day benchmark and plotted date |
| Figure 6b: waste management | `Environmental_Sanitation_Subsystem.ipynb` | Confirm handling-capacity series, starting capacity, budget growth and final observation |
| Figure 7a: tourism revenue | `Tourism_Revenue_Subsystem.ipynb` | Match tariff inputs, annual receipts and graph's exact ending year |
| Figure 7b: facility capacity | `Tourism_Facilities_Availability_Subsystem.ipynb` | Identify unit conversion and distinguish modeled facility capacity from admissions |
| Figure 8a: service quality | `Tourism_Services_Subsystem.ipynb` | Confirm index definition, ceiling of 100, and temporal trajectory |
| Figure 8b: cultural sustainability | `Cultural_Preservation_Subsystem.ipynb` | Confirm the assumed cultural-index threshold of 60 and crossing date |
| Figure 8c: vendors and income | `Economic_Subsystem_of_the_Local_Community_in_the_Tourism_Sector.ipynb` | Confirm vendor population, income scale and quota settings |

## Important distinctions

- The cultural-index date near 2031 is not an ecosystem-health 80% crossing date.
- The operational visitor threshold in August 2038 is not independently established ecological carrying capacity.
- Seven independently simulated subsystems should not be described as a single coupled numerical solver.
- Figure endpoints showing 2046 and available daily notebook output ending in 2045 require version matching before reporting exact replication.
- Extracted PNGs from notebooks can be compared to published figures using `scripts/export_notebook_pngs.py`, but visual similarity alone is not numerical reproducibility.
