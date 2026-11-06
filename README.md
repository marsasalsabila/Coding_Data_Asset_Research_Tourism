# Coding Data Asset Research Tourism

**Research code and supporting materials for _Language Models and System Dynamics for Overtourism_**

This repository contains research assets for an exploratory study combining online tourist reviews, language-model-assisted conceptual mapping, and system dynamics scenario analysis. Causal loop and stock-and-flow diagrams were prepared using Vensim. Numerical simulations were implemented separately in Python through Google Colab.

## Research scope

The study contains two analytically distinct components:

1. **Review analysis:** 100,162 assembled Google Maps review records from 25 Indonesian destination labels. An eight-keyword sustainability filter retained 9,469 texts for the reported BERTopic analysis, yielding twelve interpreted non-outlier topics.
2. **Bromo scenario analysis:** Bromo Tengger Semeru National Park was used as an illustrative destination. Review themes informed 23 candidate variables and 26 hypothesized causal links. Institutional sources, literature, expert judgment, and explicit modeling assumptions supplied numerical inputs.

Review-derived themes inform exploratory model conceptualization. They are not direct measurements of ecological conditions or numerical calibration series. The corpus is not a statistically representative survey of Indonesian destinations.

## Existing notebooks

These eight notebooks are retained at the repository root and are **not changed** by the reproducibility update:

| Notebook | Research component |
|---|---|
| `BERTopic.ipynb` | Topic modeling of the review corpus |
| `Tourist_Population_Subsystem.ipynb` | Visitor population and an operational reference benchmark |
| `Environmental_Sanitation_Subsystem.ipynb` | Waste generation and sanitation handling |
| `Tourism_Revenue_Subsystem.ipynb` | Tourism revenue and ticket-price settings |
| `Tourism_Facilities_Availability_Subsystem.ipynb` | Facility investment and modeled capacity |
| `Tourism_Services_Subsystem.ipynb` | Service quality and workforce training |
| `Cultural_Preservation_Subsystem.ipynb` | Cultural sustainability and preservation |
| `Economic_Subsystem_of_the_Local_Community_in_the_Tourism_Sector.ipynb` | Street vendors and local-economy outcomes |

The seven subsystem notebooks are **separate numerical implementations**. A conceptual Vensim diagram does not in itself establish that all seven subsystems were solved as one integrated numerical system.

## Interpreting the scenario results

The manuscript's scenario values are conditional outputs, not independent empirical forecasts:

- **Cultural sustainability:** a modeled index crosses its assumed threshold of 60 around **2031** under business-as-usual.
- **Operational visitor activity:** an assumed benchmark of approximately **2,752 visitors/day** is reached around **2039** in the reported business-as-usual scenario.
- **Ecosystem health:** the separately discussed 80% reference threshold is an assumption, with no independently established crossing date.
- Interventions compare specified settings for ticket pricing, sanitation, facilities, training, cultural preservation and vendor management. The comparison does not isolate the causal effect of each measure.

The 2031 cultural-index date and the 2039 visitor benchmark measure **different constructs**. They must not be described as a confirmed seven-year ecological warning window. Numerical and plotted end dates should also be matched to their particular source revisions before reporting exact reproduction of figures.

## Historical-fit reporting

The manuscript reports mean absolute percentage error (MAPE) values for seven subsystems, with an unweighted mean of **6.45%**. The local-economy subsystem reports **15.60%**. Some 2023 simulated reference values were aligned with their baseline observations before these calculations. Consequently, the reported MAPE should not be treated as evidence of independently validated long-term forecasting accuracy.

## Reproducibility tools

The `reproducibility/` directory contains **additional supporting utilities**, not substitutes for the historical simulation notebooks. These include review filtering, MAPE calculation from supplied data, detection of modeled threshold crossings, CSV plotting, source-notebook inventory, and opt-in notebook execution.

Install the lightweight tool requirements and run tests:

```bash
python -m pip install -r reproducibility/requirements.txt
python -m unittest discover -s reproducibility/tests -v
```

For examples, commands, and interpretive limits, read [reproducibility/README.md](reproducibility/README.md). All CSV fixtures in `reproducibility/examples/` are synthetic and are **not historical Bromo measurements**.

## Data and reuse

The repository already contains `final_data_for_25_destinations_with_coordinates.zip`. The contents and source-platform terms should be reviewed before redistribution. A publicly hosted dataset does not necessarily carry unrestricted permission to republish third-party review text.

Software is subject to this repository's `LICENSE`. Additional claims about the licensing of raw reviews, prompt transcripts, or annotations require confirmation that the relevant rights are held by the authors.

## Manuscript

_**Language Models and System Dynamics for Overtourism**_, manuscript ANNALE-D-26-00377, submitted to _Annals of Tourism Research Empirical Insights_. Publication metadata and DOI may be added after publication.

## Authors

- **Marsa Salsabila:** Conceptualization, methodology, software, validation, formal analysis, investigation, data curation, writing original draft, visualization.
- **Dian Puteri Ramadhani:** Methodology, validation, writing review and editing, supervision.
- **Andry Alamsyah:** Conceptualization, methodology, validation, writing review and editing, supervision.

The authors acknowledge Telkom University, participating experts, and developers of the open-source tools used in this research.
