![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Paleodiversity Index Calculator
 
*For paleontologists and ecologists: enter species abundances to instantly compute species richness, Shannon index, Simpson index, and Pielou's evenness with a bar plot.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Paleontology
 
The user provides a list of species names (text) and their corresponding abundances (non‑negative integers or floats, e.g., specimen counts or relative percentages). The tool requires at least one species and allows up to 30 species. The user can also select whether abundance input is absolute counts or percentages (if percentages, they are normalized to sum to 1.0). The core calculation proceeds as follows: sum abundances to get total N (if counts) or total fraction (if percentages). Compute number of species S. For each species i, calculate proportion p_i = abundance_i / total. Shannon index H' = -Σ(p_i * ln(p_i)) (using natural log; if any p_i = 0, treat p_i*ln(p_i)=0). Simpson's index D = Σ(p_i^2) (the dominance measure); the tool also reports 1-D (the Simpson diversity) and 1/D (the inverse Simpson). Pielou's evenness J' = H' / ln(S) (only defined if S>1; if S=1, J'=1). The Gradio UI consists of a 'Species Abundance' data table (DataFrame editor) with columns 'Species' (text) and 'Abundance' (number), plus a radio button to choose between 'Counts' and 'Percentages'. A 'Compute' button triggers the calculation. Outputs: a set of numeric readouts (large, clear numbers) for S, N (total count or total %, depending on input), H', D, 1-D, 1/D, and J'. Additionally, a bar plot shows each species abundance as a bar, with species names on the x-axis and abundance on the y-axis, sorted from highest to lowest. Optionally, a 'Download Results' button exports the output numbers and the plot as a CSV and PNG, respectively. No AI/ML component is used; it is a pure statistical calculation.
 
## Run it
 
```bash
docker build -t paleodiversity-index-calculator .
docker run -p 7860:7860 paleodiversity-index-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-10-02.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
