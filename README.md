# Coding Data Asset Research Tourism 🏖️📊

This repository contains research and data analysis on coding assets and tourism research using Jupyter Notebook.

## 🎯 About the Research

This project is a multidisciplinary research initiative at the intersection of Natural Language Processing (NLP), data science, and sustainable tourism governance. Rather than relying on static lagging indicators, this repository serves as the computational backbone for predicting ecological tipping points in nature-based destinations. 

Our core focus areas include:
- **Big Data Analytics & NLP:** Processing massive unstructured tourist feedback (`final_data_for_25_destinations_with_coordinates.zip`) using advanced transformer-based topic modeling (`BERTopic.ipynb`) to extract empirically grounded system variables.
- **Complex Systems Modeling:** Mathematically operationalizing the "ecotourism paradox" by mapping socio-ecological interactions across seven distinct subsystems (e.g., Environmental Sanitation, Cultural Preservation, Local Economy).
- **Scenario Simulation & Visualization:** Executing long-term behavioral projections to visualize the exact temporal gap between ecological degradation and physical overcrowding.
- **Evidence-Based Governance:** Delivering predictive, data-driven policy interventions (such as dynamic pricing and vendor quotas) to ensure the long-term resilience of the tourism sector.

## 📂 Repository Structure

```
Coding_Data_Asset_Research_Tourism/
│
├── BERTopic.ipynb                                                              # ipynb for BERTopic Processing
├── Cultural_Preservation_Subsystem.ipynb                                       # ipynb for Cultural Prservation
├── Economic_Subsystem_of_The_Local_Community_in_the_Tourism_Sector.ipynb       # ipynb for Local Economy Community Subsystem
├── Environmental_Sanitation_Subsystem.ipynb                                    # ipynb for Sanitation Subsystem
├── Tourism_Facilitites_Availibility_Subsystem.ipynb                            # ipynb for Facilities Availibility Subsystem
├── Tourism_Revenue_Subsystem.ipynb                                             # ipynb for Revenue Subsystem
├── Tourism_Services_Subsystem.ipynb                                            # ipynb for Services Subsystem
├── Tourism_Population_Subsystem.ipynb                                          # ipynb for Tourism Population Subsystem
├── final_data_for_25_destinations_with_coordinates.zip                         # Dataset Files
```

## 🚀 How to Run the Notebooks

Since this repository consists entirely of Jupyter Notebooks (`.ipynb`) and datasets, no formal software installation is required. You can explore and reproduce the simulations using either a cloud-based environment or your local machine.

### Option 1: Run in the Cloud (No Installation Required)
This is the fastest way to explore the data without configuring your local environment.
1. Download the specific `.ipynb` file and the dataset (`final_data_for_25_destinations_with_coordinates.zip`).
2. Upload them to a cloud environment like [Google Colab](https://colab.research.google.com/).
3. Install any missing packages directly in the first cell of the notebook (e.g., `!pip install bertopic`).

### Option 2: Local Execution (For Reproducibility)
If you prefer to run the simulations locally, we highly recommend setting up a virtual environment. Complex NLP libraries (like BERTopic) require specific package versions to avoid dependency conflicts.

1. **Clone The Repository**
   ```bash
   git clone https://github.com/marsasalsabila/Coding_Data_Asset_Research_Tourism.git
   cd Coding_Data_Asset_Research_Tourism
   ```

2. **Create a Virtual Environment**
   ```bash
   # Menggunakan venv
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate 
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook
   ```
## 🔗 Links
- **Paper (On Publication Process):** [Read the Manuscript Draft Here](https://telkomuniversityofficial-my.sharepoint.com/:w:/g/personal/andrya_telkomuniversity_ac_id/IQCI7YBh4l_UQ4_3OtjorcuYAesqv4fWb_YzqlgHv9BReco?e=r0AGPM)
- **GitHub Repository:** [Coding_Data_Asset_Research_Tourism](https://github.com/marsasalsabila/Coding_Data_Asset_Research_Tourism.git)

## 📊 Key Findings & Simulation Projections
- **The Ecotourism Paradox & Degradation Pattern:** Simulations prove that the waste and ecological management crisis will emerge first in 2031, while physical carrying capacity will not be breached until 2038.
- **The 7-Year Governance Window:** The time gap between the early indicators of environmental degradation (2031) and total physical overcrowding (2038) provides a critical window for policymakers to intervene before ecosystem damage becomes irreversible.
- **Integrated Intervention Scenario:** The combination of strategic demarketing policies (dynamic ticket pricing), informal vendor quota restrictions (capped at 450 units), and an annual sanitation budget increase of 5% is mathematically proven to sustain the socio-ecological resilience of TNBTS through 2045.

## 📜 Data Availability Policy & License
- **Source Code:** All source code in this repository is released under the MIT License.
- **Annotated Data:** Document-topic matrices, AI prompt transcripts, and extracted variables are licensed under CC BY 4.0.
- **Raw Corpora:** In accordance with Google Maps' Terms of Service, massive raw text reviews are not openly redistributed in this repository. However, anonymized reviews for academic reproduction purposes may be requested formally from the corresponding author.

## ⚖️ License
This project is licensed under the MIT License. See the LICENSE file in this repository for full details.

## ✍️ Author Contributions (CRediT)
- **Marsa Salsabila:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing — original draft, Visualization
- **Dian Puteri Ramadhani:** Methodology, Validation, Writing — review and editing, Supervision.
- **Andry Alamsyah:** Conceptualization, Methodology, Validation, Writing — review and editing, Supervision.

## 📬 Contact
For any inquiries regarding the code, data, or research findings, please feel free to reach out to the authors:
- Marsa Salsabila: marsasalsabila@student.telkomuniversity.ac.id
- Dian Puteri Ramadhani: dianpramadhani@telkomuniversity.ac.id
- Andry Alamsyah (Corresponding Author): andrya@telkomuniversity.ac.id

## 🙏 Acknowledgements
- We would like to express our gratitude to Telkom University for the continuous support of this research initiative.
- Special thanks to the open-source community, particularly the developers of BERTopic and the advanced Python libraries utilized in this study.
- We also acknowledge the expert panel for their rigorous validation of the System Dynamics parameters.
