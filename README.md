# ServiceTitan ML Portfolio

15 end-to-end Jupyter notebooks covering ML problem domains relevant to ServiceTitan's
home services SaaS platform, plus company intelligence and interview prep.

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
| [11](11_langchain_langgraph_agents.ipynb) | **LangGraph Agents** | StateGraph, tool-calling, confirm-before-execute, routing |
| [12](12_reinforcement_learning.ipynb) | **RL & Online Optimization** | Epsilon-greedy, UCB1, LinUCB, Q-learning, regret bounds |
| [13](13_rag_architecture.ipynb) | **RAG Architecture** | Sparse + dense retrieval, RRF fusion, re-ranking, Hit@K / MRR |
| [14](14_realtime_ml_serving.ipynb) | **Real-Time ML Serving** | ONNX, quantization, batching, latency benchmarks, serving patterns |
| [15](15_multitenant_ml.ipynb) | **Multi-Tenant ML** | Global vs per-tenant models, cold start, DP, Atlas personalization |

---

## Company Intelligence & Interview Prep

See the [`company_intel/`](company_intel/) folder:

| File | Contents |
|---|---|
| [01_company_overview.md](company_intel/01_company_overview.md) | Business model, founders, markets, key people |
| [02_financials_ipo.md](company_intel/02_financials_ipo.md) | IPO, ARR, revenue breakdown, unit economics |
| [03_tech_stack.md](company_intel/03_tech_stack.md) | .NET, Azure, SQL Server, Kafka, Azure ML, PyTorch |
| [04_ml_platform_titan_intelligence.md](company_intel/04_ml_platform_titan_intelligence.md) | Titan Intelligence suite, Atlas, all ML use cases |
| [05_architecture_microservices.md](company_intel/05_architecture_microservices.md) | Monolith migration, event-driven architecture, deployment |
| [06_staff_ml_role.md](company_intel/06_staff_ml_role.md) | Job descriptions, salary, interview process |
| [07_references.md](company_intel/07_references.md) | All sources with URLs |
| [08_hackerrank_coding.md](company_intel/08_hackerrank_coding.md) | MultiMap, LRU cache, async patterns with O(n) analysis |
| [09_ml_system_design.md](company_intel/09_ml_system_design.md) | 6 system design problems with Azure ML-specific approaches |

---

## Setup

### 1. Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and install

```bash
git clone https://github.com/sp7412/servicetitan-ml-portfolio
cd servicetitan-ml-portfolio

uv venv
uv pip install -r requirements.txt
```

### 3. Register Jupyter kernel

```bash
uv pip install ipykernel
uv run python -m ipykernel install --user --name=servicetitan-ml --display-name "Python (servicetitan-ml)"
```

### 4. Launch

```bash
uv run jupyter notebook
```

Open any notebook and select **Kernel → Change kernel → Python (servicetitan-ml)**.

---

## Notebook 01: Real Dataset

Notebook 01 auto-detects the IBM Telco Churn CSV if present, otherwise generates a
faithful reproduction. To use the real data:

```bash
# Kaggle CLI
uv run kaggle datasets download -d blastchar/telco-customer-churn --unzip
# or download manually: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
# Save as WA_Fn-UseC_-Telco-Customer-Churn.csv in the repo root
```

---

## Themes Across All Notebooks

- **Time-based train/test splits** — never random-split time series or account data
- **Calibrated probabilities** — raw model scores aren't probabilities; always calibrate
- **SHAP for explainability** — models need to be explainable to be operationally useful
- **Feedback loop design** — every deployed model changes the data it's trained on
- **Humans in the loop** — consequential actions (dispatch, pricing) require human confirmation
