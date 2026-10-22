# Staple Food Price Volatility Monitoring & Crisis Early Warning for Philippine Consumer Markets

[![Course: DS312](https://img.shields.io/badge/Course-DS312%20Data%20Mining%20%26%20Applications-1B365D?style=flat-square)](https://github.com/Troge-dev)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2026--2027%20(1st%20Sem)-2E5B88?style=flat-square)](https://github.com/Troge-dev)
[![Data Source: UN WFP / HDX](https://img.shields.io/badge/Data-UN%20WFP%20%7C%20HDX-D9381E?style=flat-square)](https://data.humdata.org/dataset/wfp-food-prices-for-philippines)
[![Complexity Tier](https://img.shields.io/badge/Rubric%20Tier-Advanced%20(8%2F8%20Pts)-2E7D32?style=flat-square)](https://github.com/Troge-dev)
[![License: CC-BY 4.0](https://img.shields.io/badge/License-CC--BY%204.0-gray?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)

> **DS312 Final Project (Phase 1 to Phase 5)**  
> **Instructor:** Prof. Nicole S. Menorias  
> **Project Window:** October 12 – December 5, 2026  
> **Repository:** [`Troge-dev/DS312-Philippine-Food-Price-Early-Warning`](https://github.com/Troge-dev/DS312-Philippine-Food-Price-Early-Warning)

---

## 1. Executive Summary

Food security and commodity price stability are central to the socioeconomic welfare of the Philippines. Staple foods—particularly rice, highland vegetables (red onions, tomatoes, cabbage), and animal proteins (pork, poultry, eggs)—account for a large share of household expenditure for low- and middle-income Filipino families. Historical supply disruptions, such as the 2018 national rice crisis, the 2022–2023 onion price surge (where retail prices exceeded ₱1,000/kg), and African Swine Fever (ASF) supply shocks, highlight critical vulnerabilities in the domestic supply chain.

This project implements an end-to-end data mining framework utilizing the official **United Nations World Food Programme (WFP) Vulnerability Analysis and Mapping (VAM)** database for the Philippines, distributed via the Humanitarian Data Exchange (HDX). Spanning over 26 years (January 2000 to August 2026) and comprising **238,623 records across 108 wet markets in 79 provinces**, this initiative couples **Unsupervised Spatial-Temporal Market Clustering** (to uncover provincial market vulnerability archetypes) with **Supervised Gradient-Boosted Classification & Forecasting** (to predict localized price shocks 30–60 days ahead), providing regulatory authorities (**DA, DTI, NFA**) with an actionable, forward-looking decision instrument.

---

## 2. The "Palengke Food Basket" Framework

Rather than analyzing rice in isolation, this study curates an **8-commodity representative basket (~60,157 observations)** reflecting three distinct supply-chain and volatility profiles:

| Class | Key Commodities | Observations | Behavioral Profile & Drivers |
| :--- | :--- | :---: | :--- |
| **1. Staple Grains** | • Rice (regular, milled)<br>• Rice (well milled) | 9,920<br>6,300 | High storability, national price ceilings, NFA buffer stock intervention, sensitive to import tariffs (RA 11203 Rice Tariffication Law). |
| **2. Volatile Highland Vegetables** | • Onions (red)<br>• Tomatoes<br>• Cabbage | 6,787<br>7,779<br>7,543 | Perishable, lack of cold chain infrastructure, acute post-typhoon price spikes, sensitive to import licensing delays (e.g. 2022–2023 onion crisis). |
| **3. Core Animal Proteins** | • Meat (pork)<br>• Meat (chicken, whole)<br>• Eggs | 8,262<br>6,867<br>6,699 | Biological disease exposure (African Swine Fever, Avian Flu), feed import dependency (corn/soybeans), strict cold-chain requirements. |

---

## 3. Methodological Contrast: Data Mining vs. Traditional Studies

| Analytical Dimension | Traditional Studies (PIDS, UPLB, DA) | Proposed DS312 Data Mining Pipeline |
| :--- | :--- | :--- |
| **Analytical Horizon** | **Retrospective & Explanatory:** Cointegration and VECM models explain why past price movements occurred months after the fact. | **Forward-Looking & Predictive:** Formulates price spike detection as an out-of-time classification task 30–60 days in advance. |
| **Commodity Breadth** | **Single-Commodity Focus:** Over 85% of domestic literature studies only rice (paddy vs. milled), ignoring perishable crops. | **Integrated Palengke Basket:** Simultaneously evaluates durable grains, volatile highland vegetables, and animal proteins. |
| **Modeling Paradigms** | **Linear Econometrics:** Assumes linear transmission, which fails during severe supply ruptures and policy ceiling shocks. | **Non-Linear Tree Ensembles:** Deploys Random Forests and LightGBM/XGBoost to capture non-linear tipping points and threshold effects. |
| **Regional Segmentation** | **Manual Partitioning:** Manually groups data into broad island groups (Luzon/Visayas/Mindanao) or 2–3 major cities. | **Data-Driven Unsupervised Clustering:** Applies K-Means and DBSCAN across all 108 markets based on empirical price volatility signatures. |

---

## 4. Business Problem Canvas

| Dimension | Group Specification |
| :--- | :--- |
| **Context / Organization** | Department of Agriculture (DA), Department of Trade and Industry (DTI - Fair Trade Group), National Food Authority (NFA), and Provincial/City Local Price Coordinating Councils (LPCCs). |
| **Problem Statement** | Agricultural surveillance is predominantly retrospective. Authorities lack an automated early-warning framework to detect structural market vulnerabilities, quantify middleman margins, and anticipate staple food price shocks before consumer purchasing power is compromised. |
| **Stakeholders** | 1. Policy Makers (DA, DTI, NFA): Setting Suggested Retail Prices (SRP), import tariff adjustments, and emergency buffer stock releases.<br>2. Local Government Units (LGUs): Directing targeted palengke inspections and monitoring price gouging.<br>3. Farmers & Consumer Advocacy Groups: Benefiting from transparent market margin benchmarks. |
| **Business Questions** | 1. **Market Vulnerability Archetypes:** Which Philippine wet markets act as 'price leaders' (shock originators) versus 'price followers' (lagged shock absorbers)?<br>2. **Price Shock Early Warning:** Can we predict whether a staple commodity in a given province will experience a critical price shock (>20% monthly increase or >2σ volatility) 30–60 days ahead?<br>3. **Value-Chain Spread:** How do margins between Farm Gate, Wholesale, and Retail prices vary across regions and commodity classes?<br>4. **Seasonality & Shock Lag:** What seasonal cycles and lag structures systematically precede sustained commodity price inflation? |
| **Success Criteria** | • Unsupervised: Discover 3–5 statistically distinct market clusters (Silhouette Score ≥ 0.45) with intuitive geographic/logistical interpretations.<br>• Supervised: Achieve an AUC-ROC ≥ 0.80 and PR-AUC > 0.40 (substantially beating the ~10% minority class baseline) for 30-day price spike prediction.<br>• Usability: Deliver concrete policy intervention rules tied directly to model outputs. |
| **Task Types** | **Dual Data Mining Technique Families:**<br>1. *Unsupervised Learning:* Spatial-Temporal Market Clustering (K-Means / Agglomerative Clustering / DBSCAN).<br>2. *Supervised Learning:* Cost-Sensitive Binary Classification & Gradient Boosted Regression (Logistic Regression Baseline vs. Random Forest & LightGBM/XGBoost). |
| **Risks & Limitations** | • Historical reporting cadence varies across remote provincial wet markets.<br>• Exogenous geopolitical shocks (global fertilizer costs, crude oil) must be approximated via temporal proxy lags.<br>• Spanning 26 years requires nominal price deflation (CPI base adjustment) or rolling relative price ratios to prevent historical nominal distortion. |

---

## 5. Repository Structure

```text
DS312-Philippine-Food-Price-Early-Warning/
├── data/
│   ├── raw/
│   │   ├── wfp_food_prices_phl.csv   # 238,623 rows × 16 columns (31.34 MB)
│   │   └── wfp_markets_phl.csv       # 132 monitored wet markets × 7 columns (0.01 MB)
│   └── processed/                    # Cleaned, integrated matrices for Phases 2–4
├── notebooks/
│   └── DS312_Phase1_Food_Price_Early_Warning.ipynb  # Executed Phase 1 Master Notebook
├── reports/
│   ├── DS312_Phase1_Project_Proposal_Food_Security_Times_New_Roman.docx # Formal Proposal
│   └── DS312_Phase1_Project_Proposal_Food_Security.docx
├── scripts/
│   ├── download_data.py              # Automated HDX dataset downloader
│   ├── create_proposal_docx.py       # Proposal document generator
│   └── create_phase1_notebook.py     # Master notebook builder
├── .gitignore
├── README.md
└── [STUDENT] DS312_FINAL_PIT_GUIDE.pdf
```

---

## 6. Project Timeline & Milestones

| Phase | Focus & Deliverables | Dates | Deadline |
| :---: | :--- | :--- | :--- |
| **Phase 1** | **Dataset Selection & Business Problem Canvas**<br>• Initial load (`.shape`, `.head()`, `.info()`, `.describe()`)<br>• Candidate dataset evaluation matrix (Advanced Tier justification)<br>• Formal Proposal Document & Master Notebook | Oct 12 – Oct 24 | **Sun, Oct 25, 2026**<br>*(Narrative: Oct 28)* |
| **Phase 2** | **Data Preprocessing & Data Quality Report**<br>• Table joins (`market_id`), unit standardization, missing value treatment<br>• Preprocessing Log documenting every issue, action, and rationale | Oct 26 – Nov 7 | **Sun, Nov 8, 2026**<br>*(Narrative: Nov 11)* |
| **Phase 3** | **Exploratory Data Analysis (EDA)**<br>• 8+ purposeful visualizations with written interpretations<br>• 2 Statistical Hypothesis Tests (Welch's t-test, ANOVA) | Nov 9 – Nov 14 | **Sun, Nov 15, 2026**<br>*(Narrative: Nov 18)* |
| **Phase 4** | **Data Mining & Machine Learning**<br>• Family 1: Unsupervised Market Clustering (K-Means / DBSCAN)<br>• Family 2: Supervised Price Shock Forecasting (LightGBM vs Baseline) | Nov 16 – Nov 28 | **Sun, Nov 29, 2026**<br>*(Narrative: Dec 2)* |
| **Phase 5** | **Master Deliverables & Defense**<br>• Master Notebook, A1 Project Poster, 12-Slide PowerPoint Presentation | Nov 30 – Dec 5 | **Class Schedule (Dec 1–5)** |

---

## 7. Quickstart & Replication

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/Troge-dev/DS312-Philippine-Food-Price-Early-Warning.git
cd DS312-Philippine-Food-Price-Early-Warning
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn lightgbm xgboost requests python-docx nbformat nbclient
```

### 3. Verify or Download Dataset
```bash
python scripts/download_data.py
```

### 4. Run the Phase 1 Notebook
```bash
jupyter notebook notebooks/DS312_Phase1_Food_Price_Early_Warning.ipynb
```

---

## 8. Authors & Team Contributions

* **Student 1 (Data Engineering Lead):** Data ingestion, relational table joins, preprocessing log, and pipeline reproducibility.
* **Student 2 (EDA & Visualization Lead):** Statistical hypothesis testing (Welch's t-test, ANOVA), visual profiling, and geospatial mapping.
* **Student 3 (Modeling & Machine Learning Lead):** Time-series cross-validation architecture, baseline establishment, and gradient-boosted classification tuning.
* **Student 4 (Policy & Business Translation Lead):** Business problem canvas alignment, stakeholder recommendations, and formal documentation.
