# ServiceTitan ML Portfolio

10 end-to-end Jupyter notebooks covering the ML problem domains most relevant to ServiceTitan's home services SaaS platform. Each notebook includes synthetic (or real open-source) data, a full modeling pipeline, evaluation, and interview-ready takeaways.

---

## Notebooks

| # | Topic | Key Techniques |
|---|---|---|
| [01](01_churn_prediction.ipynb) | **Customer Churn Prediction** | XGBoost, SHAP, PR-AUC, Precision@K, calibration |
| [02](02_dispatch_optimization.ipynb) | **Technician Dispatch Optimization** | Quantile regression, GBM, greedy scheduler simulation |
| [03](03_upsell_recommendation.ipynb) | **Upsell / Cross-Sell Recommendation** | Multi-label classification, Platt scaling, utility ranking |
| [04](04_call_transcript_nlp.ipynb) | **Call Transcript NLP** | TF-IDF, logistic regression, LLM prompt design |
| [05](05_pricing_recommendation.ipynb) | **Pricing Recommendation & Elasticity** | Causal confounding, logistic elasticity, scipy revenue optimization |
| [06](06_lead_to_close_funnel.ipynb) | **Lead-to-Close Funnel Conversion** | XGBoost, SHAP coaching tips, multi-stage funnel model |
| [07](07_demand_forecasting.ipynb) | **Demand Forecasting** | Lag features, GBM time series, quantile forecasting |
| [08](08_anomaly_detection.ipynb) | **Anomaly Detection** | Rolling Z-score, week-over-week change, Isolation Forest |
| [09](09_segmentation_clv.ipynb) | **Customer Segmentation & CLV** | K-Means, RFM, silhouette scoring, CLV regression |
| [10](10_rag_estimating_assistant.ipynb) | **RAG Estimating Assistant** | TF-IDF retrieval, LLM prompt design, Hit@K evaluation |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/sp7412/servicetitan-ml-portfolio
cd servicetitan-ml-portfolio
```

### 2. Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> You should see `(.venv)` at the start of your terminal prompt once activated.

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Register the venv as a Jupyter kernel

This makes the venv available as a kernel inside Jupyter so the notebooks use the right packages:

```bash
pip install ipykernel
python -m ipykernel install --user --name=servicetitan-ml --display-name "Python (servicetitan-ml)"
```

### 5. Launch Jupyter

```bash
jupyter notebook
```

Open any notebook and select **Kernel → Change kernel → Python (servicetitan-ml)**.

---

## Notebook 01: Real Dataset

Notebook 01 uses the **IBM Telco Customer Churn** dataset — the standard churn benchmark. The notebook runs without it (generates a faithful reproduction automatically), but to use the real data:

```bash
# Option 1: Kaggle CLI
pip install kaggle
kaggle datasets download -d blastchar/telco-customer-churn --unzip

# Option 2: Manual download
# https://www.kaggle.com/datasets/blastchar/telco-customer-churn
# Save as WA_Fn-UseC_-Telco-Customer-Churn.csv in the repo root
```

All other notebooks use synthetic data generated inline — no downloads needed.

---

## Deactivating the venv

When you're done:

```bash
deactivate
```

To remove it entirely:

```bash
rm -rf .venv
```

---

## Themes Across All Notebooks

- **Time-based train/test splits** — never random-split time series or account data
- **Calibrated probabilities** — raw model scores aren't probabilities; always calibrate
- **SHAP for explainability** — models need to be explainable to be operationally useful
- **Feedback loop design** — every deployed model changes the data it's trained on
- **Humans in the loop** — consequential actions (dispatch, pricing) require human confirmation
