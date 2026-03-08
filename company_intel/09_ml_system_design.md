# 09 — ML System Design Problems

Design problems tailored to ServiceTitan's infrastructure: Azure ML, .NET/C# core platform,
SQL Server, Kafka/Azure Service Bus, Kubernetes, multi-tenant SaaS.

---

## Problem 1: Second Chance Leads (The Flagship)

**Prompt**: Design a system that analyzes call recordings within minutes of a call ending and flags missed booking opportunities for CSR follow-up.

### Requirements
- Latency: < 5 minutes end-to-end from call end to CSR notification
- Scale: ~100K calls/day across all tenants
- Accuracy: High recall (missing a real opportunity is worse than a false alarm)
- Multi-tenant: Data must be fully isolated per contractor

### Recommended Approach

```
Phone call ends
    |
    v
[Telephony webhook] --> Azure Service Bus (call_completed event)
    |
    v
[Transcription Service]  -- Azure Cognitive Services Speech API
    |  (async, ~30-60s)
    v
[Feature Extraction]     -- Extract: call_duration, words_spoken, 
    |                         price_mentioned, schedule_requested,
    |                         competitor_mentioned, urgency_keywords
    v
[ML Classifier]          -- GBM / fine-tuned DistilBERT
    |  (< 100ms)          -- threshold tuned for high recall (F0.5 metric)
    v
[Score Store]            -- Azure SQL (tenant-scoped, RLS policy)
    |
    v
[CSR Dashboard Push]     -- SignalR (real-time notification)
    + ranked by: P(missed_booking) * estimated_job_value
```

**Data Pipeline for Training:**
```
Call logs (outcome: booked / not booked)
    JOIN
Phone records (call_id -> transcript)
    JOIN  
Job creation events (was a job created within 24h of call?)
    -->
Label: missed_booking = 1 if call ended without booking AND
                              job created within 48h after follow-up
```

**Key Design Decisions:**
| Decision | Choice | Rationale |
|---|---|---|
| Labeling | Join call logs to job creation timestamps | Auto-labels; no manual annotation |
| Metric | Recall@P90 precision | CSRs can handle false positives; missing leads hurts revenue |
| Model | DistilBERT fine-tuned on transcript features | Handles semantic patterns (hesitation language) |
| Fallback | Keyword heuristic if ML unavailable | 99.9% SLA requires graceful degradation |
| Tenant isolation | Azure SQL Row-Level Security + tenant_id column | No cross-tenant data exposure |
| Retraining | Weekly, triggered by label drift | Weekly label accumulation + concept drift monitor |

---

## Problem 2: Atlas -- Agentic AI for Contractors

**Prompt**: Design the Atlas AI assistant that can answer questions, run reports, and take actions (dispatch, campaigns) through natural language.

### Requirements
- <2s P99 for read operations (reports, queries)
- Confirm-before-execute for all write operations
- Multi-tenant: each contractor sees only their own data
- Actions must be auditable and reversible where possible
- 12,000 tenants × ~50 DAU each = 600K queries/day

### Recommended Approach

```
User message
    |
    v
[Intent Router]      -- LLM with function_calling schema
    |                   Route: read_query | write_action | chitchat
    |
    +---> READ PATH:
    |       [RAG + SQL query generation]
    |       Tenant-scoped vector store (pgvector or Azure AI Search)
    |       Text2SQL for structured data (job history, revenue, techs)
    |       [Response synthesis] --> streaming to user
    |
    +---> WRITE PATH:
            [Action planner]
            Preview: "This will assign James K. to Job J001. Confirm?"
            [Human confirms]
            [Action executor] --> ServiceTitan REST API
            [Audit log] --> append-only event store
```

**Multi-Tenant Isolation for LLM Context:**
```
System prompt injection (per request):
  "You are Atlas for {tenant_name}. 
   You have access to their data only.
   Today is {date}. Their team has {n_techs} technicians."

RAG vector store:
  - Index key: (tenant_id, doc_id)  
  - All queries filtered by tenant_id before retrieval
  - No cross-tenant documents in the same retrieval call

SQL generation:
  - All generated queries automatically appended with WHERE tenant_id = ?
  - Parameterized -- no SQL injection risk
  - Generated SQL reviewed by rule-based validator before execution
```

**Scaling to 600K queries/day:**
- Horizontal scaling: stateless LLM service pods on Kubernetes (AKS)
- Caching: Redis cache for read queries (TTL=5min); identical queries from same tenant served from cache
- Rate limiting: per-tenant token bucket (prevent runaway agent loops)
- Cost control: route simple queries to smaller model (GPT-3.5); complex to GPT-4

---

## Problem 3: Dispatch Optimization

**Prompt**: Build a system that recommends (or automatically makes) technician assignments for incoming jobs, optimizing for revenue and customer satisfaction.

### Requirements
- Day-ahead planning: schedule tomorrow's jobs each night
- Real-time: react to emergency jobs, no-shows, and tech delays
- ~50 techs per contractor, ~200 jobs/day for large contractors
- Human dispatcher must be able to override any recommendation

### Recommended Approach

**Two-tier architecture:**

**Tier 1: ML models (learned features for the optimizer)**
```
Job duration predictor:     P(duration | job_type, equipment_age, tech_id, time_of_day)
                            Quantile regression (P90 for buffer)
                            Training data: completed job actual duration vs estimated

Job value predictor:        E[revenue | job_type, customer_history, tech_skill_match]
                            GBM regression

Tech-job skill match:       cosine_similarity(tech_skill_embedding, job_requirement_embedding)
                            Learned from historical completion rate per tech-job-type pair

Geo time estimator:         travel_time(tech_loc, job_loc) from Google Maps API
                            Cache results by zone pair
```

**Tier 2: Combinatorial optimizer (uses ML outputs)**
```
Day-ahead:  MILP via OR-Tools CP-SAT
            Constraints: skill match, travel time, tech availability windows
            Objective:   maximize sum(job_value * P(on_time)) - travel_cost

Real-time:  Greedy insertion heuristic
            For emergency job: score each available tech, insert at lowest cost position
            Re-optimize full schedule every 30min via background CP-SAT run
```

**Why not end-to-end RL?**
- MILP gives optimality guarantees; RL does not
- MILP is explainable to dispatchers; RL is a black box
- MILP handles hard constraints cleanly; RL often violates them
- RL is appropriate for the *policy* layer (which jobs to accept), not the assignment layer

---

## Problem 4: ML Feature Platform

**Prompt**: Design a feature store for ServiceTitan that serves features to multiple ML models in real-time with low latency and strong tenant isolation.

### Requirements
- Features needed: per-job, per-tech, per-customer, per-tenant-aggregate
- Online serving: <10ms P99
- Batch training: generate features for full historical dataset
- Consistency: training and serving must see the same feature values (no training-serving skew)
- Multi-tenant: no feature leakage between tenants

### Recommended Approach

```
┌──────────────────────────────────────────────────────────────────┐
│                    Feature Platform                               │
│                                                                   │
│  OFFLINE (training)              ONLINE (serving)                │
│  ─────────────────               ─────────────────               │
│  Azure ML Datasets               Redis (hot features)            │
│  Redshift / Snowflake            Azure SQL (warm features)       │
│  Spark feature pipelines         Feature server (FastAPI/gRPC)  │
│                                                                   │
│  Feature Registry (Azure ML)                                     │
│  - feature name, type, version                                   │
│  - computation logic (SQL / Python)                              │
│  - TTL (how stale is acceptable?)                                │
│  - owner, SLA                                                    │
│                                                                   │
│  Key: f"{tenant_id}:{entity_type}:{entity_id}:{feature_name}"   │
└──────────────────────────────────────────────────────────────────┘
```

**Feature Categories and Serving Strategy:**

| Feature Type | Example | Freshness | Storage |
|---|---|---|---|
| Real-time entity | Tech current location | <1s | Redis (TTL=30s) |
| Job-level | Job duration estimate | Computed at booking | Azure SQL |
| Customer rolling | 90-day spend, churn risk | Hourly batch | Redis (TTL=1h) |
| Tenant aggregate | Fleet utilization, close rate | Daily batch | Azure SQL |
| Embedding | Tech skill vector | Weekly retrain | Azure ML / SQL |

**Avoiding Training-Serving Skew:**
- Feature computation logic defined once in `feature_registry.py`
- Same function called by both Spark batch pipeline and online feature server
- Point-in-time correct features: training always joins on `event_time < label_time`

---

## Problem 5: Demand Forecasting at Scale

**Prompt**: Build a system to forecast job demand per service category and region for the next 2 weeks, to help contractors with staffing and parts ordering.

### Requirements
- Forecast 7 service categories × 50 regions = 350 time series per tenant
- Granularity: daily, 14-day horizon
- Retrain frequency: weekly
- Must be explainable: "Demand up 20% this week due to heat wave forecast"

### Recommended Approach

```
Data:
  - Historical job volume (per category, region, day)
  - Weather forecast (temperature, humidity -- from external API)
  - Calendar features (holidays, school calendars, local events)
  - Seasonality (HVAC: peaks in summer/winter; plumbing: spring thaw)
  - Lag features: job_vol_{t-7}, job_vol_{t-14}, job_vol_{t-28}
  - Trend: 4-week rolling average, YoY growth rate

Models (test all, pick per vertical):
  1. Prophet (Facebook): captures seasonality + holidays, explainable, fast to train
  2. LightGBM with lag features: handles non-linear weather interactions
  3. N-BEATS: neural architecture, best for accuracy on sufficient data
  4. Ensemble: weighted blend of 1+2

Serving:
  - Weekly batch job on Azure ML pipeline
  - Outputs stored in Redshift, surfaced in contractor dashboard
  - Confidence intervals shown (P10/P50/P90)
  - "Demand driver" column: top contributing feature for human interpretability

Evaluation:
  - MAPE (mean absolute percentage error) by category
  - Pinball loss for interval calibration
  - Business metric: forecast error translates to under/over-staffing cost
```

---

## Problem 6: Real-Time Anomaly Detection (Atlas Monitoring)

**Prompt**: Detect anomalies in contractor KPIs in real time and alert Atlas when something needs attention (e.g., sudden drop in booking rate, technician no-shows).

### Recommended Approach

**3-tier detection hierarchy:**

```
Tier 1: Statistical (rule-based, fast)
  - Z-score on rolling 30-day window: alert if |z| > 3
  - Week-over-week change: alert if delta > 2 sigma
  - Hard thresholds: 0 jobs scheduled on Monday = alert
  Latency: <1ms, covers ~80% of real anomalies

Tier 2: ML-based (Isolation Forest per metric)
  - Trained weekly on tenant's own history
  - Catches multivariate anomalies (e.g., revenue normal but close rate dropped)
  - Per-tenant model (isolation forest is lightweight enough)
  Latency: <10ms, runs on Kafka consumer

Tier 3: LLM contextual (high-value alerts only)
  - "Revenue dropped 30% this week. Check: tech James K. went on leave,
     HVAC slow season started, 3 negative reviews this week."
  - Runs only on Tier 1/2 alerts (not every data point)
  - Calls Atlas with context + anomaly summary
  Latency: 2-5s, runs async after alert is triggered
```

---

## Design Interview Scoring Rubric

When ServiceTitan evaluates a system design, they likely care about:

| Area | What They Want to See |
|---|---|
| Problem scoping | Ask clarifying questions; identify the right ML formulation |
| Data pipeline | How labels are created; training-serving consistency |
| Model selection | Justify choice; acknowledge alternatives; know tradeoffs |
| Serving architecture | Latency budget; batch vs real-time; fallback logic |
| Multi-tenancy | Data isolation; cold start; per-tenant vs global |
| Monitoring | Data drift, model drift, business metric tracking |
| Failure modes | What happens when the model is wrong? |
| Azure ML specifics | Reference their actual stack (endpoints, pipelines, registry) |
| Business impact | Always tie back to revenue, CSM efficiency, contractor outcomes |
