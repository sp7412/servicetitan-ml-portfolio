# ServiceTitan ML Portfolio

37 end-to-end Jupyter notebooks covering ML problem domains relevant to ServiceTitan's
home services SaaS platform, plus company intelligence and interview prep.

The first 29 notebooks were built for the Staff AI Engineer (Voice Agents) role.
Notebooks 30-37 are targeted at the Agent OS Platform Engineering role (JR114907)
and cover the core platform primitives: agent runtime, typed tool contracts,
evaluation infrastructure, and production observability.

---

## Notebooks

### Core ML/DS Problems (1-21)

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
| [16](16_advanced_dict_structures.ipynb) | **Advanced Data Structures** | MultiMap, LRU cache, trie, segment tree, O(n) complexity analysis |
| [17](17_vision_transformers_vit.ipynb) | **Vision Transformers (ViT)** | Patch embedding, multi-head attention, fine-tuning, use-case mapping |
| [18](18_dataclasses_containers.ipynb) | **Dataclasses & Type-Safe Containers** | `@dataclass`, `Protocol`, generics, validated domain objects |
| [19](19_ml_design_patterns.ipynb) | **ML Design Patterns** | Strategy, Factory/Registry, Observer/Callback, Template Method, Adapter |
| [20](20_agentic_ai_llm_selection.ipynb) | **Agentic AI & LLM Selection** | ReAct agents, model routing, Atlas architecture, multi-tenant guardrails, cost modeling |
| [21](21_agentic_router_poc.ipynb) | **Agentic Router POC** | TF-IDF+LR router, LoRA LLM path, entity extraction, loop-back dispatch, confidence gating |

### Advanced Topics (22-29)

| # | Topic | Key Techniques |
|---|---|---|
| [22](22_llm_eval_guardrails.ipynb) | **LLM Evaluation & Guardrails** | RAGAS metrics, DeepEval assertions, injection/PII guards, LLM-as-judge cascade |
| [23](23_financial_forecasting.ipynb) | **Financial Forecasting & Optimization** | Hierarchical forecasting, quantile GBMs, anomaly detection, SLSQP budget allocation, Monte Carlo |
| [24](24_mcp_server_servicetitan.ipynb) | **MCP Server for ServiceTitan** | JSON-RPC 2.0 protocol, tenant isolation, audit logs, LangGraph agent wiring |
| [25](25_causal_inference.ipynb) | **Causal Inference & Experiments** | Power analysis, CUPED variance reduction, switchback experiments, DiD, PSM |
| [26](26_onboarding_acceleration.ipynb) | **Customer Onboarding Acceleration** | Kaplan-Meier survival, GBM propensity scoring, GenAI intervention routing, A/B evaluation |
| [27](27_coding_servicetitan_top5.ipynb) | **Coding: ServiceTitan Top 5** | VersionedMultiMap, LRU (linked-list), async fetch, priority scheduler, rate limiter |
| [28](28_coding_leetcode_top5.ipynb) | **Coding: Classic LeetCode Top 5** | Two Sum, Valid Parens, Merge Intervals, LRU (OrderedDict), Course Schedule |
| [29](29_coding_ml_engineer_top5.ipynb) | **Coding: ML Engineer Top 5** | Softmax + CE (stable), K-means, Top-K heap, Rolling stats, Scaled dot-product attention |

### Agent OS Platform Engineering (30-37)

Targeted at ServiceTitan's Agent OS Platform role (JR114907). These notebooks
cover the core engineering primitives the JD describes: agent runtime, typed
tool contracts, evaluation infrastructure, and production observability.

| # | Topic | Key Techniques | Agent OS Pillar |
|---|---|---|---|
| [30](30_agent_runtime_durable_execution.ipynb) | **Agent Runtime: Durable Execution** | SqliteSaver checkpointing, pause/resume, idempotency tokens, tenant-scoped thread IDs, failure recovery | Agent runtime and workflow execution |
| [31](31_typed_tool_contracts_safety.ipynb) | **Typed Tool Contracts & Action Safety** | Pydantic v2 frozen models, precondition validators, scoped permission model, immutable audit log, rollback/compensating transactions | Typed tools and action contracts |
| [32](32_agent_eval_harness.ipynb) | **Agent Evaluation Harness** | Offline scenario library, trajectory scoring (exact/prefix/edit-distance), LLM-as-judge with rubric, regression detection, autonomy promotion gates | Evaluation and observability |
| [33](33_autonomous_research_agent.ipynb) | **Autonomous Research Agent** | LangGraph ReAct loop, SQLite checkpoint, multi-agent pipeline, autonomous scheduler, dry-run mode | Agent runtime and workflow execution |
| [34](34_agentic_anomaly_detection.ipynb) | **Agentic Anomaly Detection over Structured Streams** | Tool-calling agent over DuckDB, five typed tools, ground-truth F1 validation, Ollama local LLM, auditable reasoning trace | Typed tools and action contracts |
| [35](35_meta_prompt_generator.ipynb) | **Meta-Prompt Generator with LLM-as-Judge** | LangChain LCEL, variant generation, LLM-as-judge scoring, CoT rationale, bias taxonomy, regression tracking | Evaluation and observability |
| [36](36_local_rag_pipeline.ipynb) | **Local RAG Pipeline: FAISS, Hybrid Retrieval & Memory** | FAISS IndexFlatIP, BM25 sparse retrieval, RRF fusion, conversational memory, provenance tracking | Context and memory systems |
| [37](37_langfuse_context_optimization.ipynb) | **Context Optimization with Langfuse Tracing** | Self-hosted Langfuse tracing, chunking strategy comparison, top-k experiments, context budget management, freshness TTL | Context and memory systems |

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
| [10_transformers_vit_use_cases.md](company_intel/10_transformers_vit_use_cases.md) | ViT use cases, attention maps, fine-tuning strategies for ST domains |

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
- **Agentic safety** — multi-step agents require trace logging, guardrails, and human confirmation gates on write actions
- **Cost-aware model selection** — cascade routing and model tiering are engineering requirements at ST scale
- **Typed contracts over untyped dicts** — Pydantic v2 frozen models as the boundary between LLM reasoning and system writes
- **Idempotency by default** — every tool that writes to a system of record must be safe to retry
- **Observability first** — Langfuse tracing, W&B, and structured audit logs are not optional in production
