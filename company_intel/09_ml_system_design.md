# 09 — ML System Design Problems

## Overview: What to Expect

**Format:** 45-60 minute system design discussion with ML Engineer or Staff ML Engineer
**Structure:** Open-ended problem → Requirements gathering → Architecture design → Deep dives

**Common Themes Based on ServiceTitan's Products:**
- Real-time ML systems (< 5 min latency)
- Multi-tenant SaaS architecture (12,000+ contractors)
- Azure ML infrastructure (their actual stack)
- Business impact focus (revenue, efficiency, contractor outcomes)

**What Makes ServiceTitan ML Design Unique:**
1. **Multi-tenancy is non-negotiable** - Every design must isolate tenant data
2. **Azure ML ecosystem** - Use their actual tools (not AWS SageMaker)
3. **Business metrics matter** - Always connect to revenue/efficiency
4. **Hybrid ML + rules** - Pure ML rarely works; need fallbacks
5. **Explainability required** - Contractors need to understand recommendations

---

## Background: ServiceTitan's ML Platform

### Tech Stack (Reference for Your Designs)

**Infrastructure:**
- **Cloud:** Azure (not AWS)
- **ML Platform:** Azure ML (model registry, endpoints, pipelines)
- **Compute:** Kubernetes (AKS) for serving, Azure ML Compute for training
- **Storage:** Azure SQL Server, Cosmos DB, Azure Blob Storage
- **Streaming:** Azure Service Bus, Kafka
- **Caching:** Redis
- **Monitoring:** Application Insights, Prometheus + Grafana

**ML Tools:**
- **Training:** Python (scikit-learn, XGBoost, PyTorch, Transformers)
- **Serving:** FastAPI/gRPC microservices on Kubernetes
- **Feature Store:** Custom-built on Azure SQL + Redis
- **LLMs:** Azure OpenAI (GPT-4, GPT-3.5-turbo)
- **Vector DB:** Azure AI Search (formerly Cognitive Search)

**Core Platform:**
- **Backend:** .NET/C# (not Python)
- **Frontend:** React
- **Database:** SQL Server (not PostgreSQL)
- **API:** REST + GraphQL

### Key Constraints to Remember

1. **Multi-tenant SaaS:** 12,000+ contractors, each with isolated data
2. **Scale:** 100K+ calls/day, millions of jobs/year
3. **Latency:** Real-time features need <100ms, batch is overnight
4. **Cost:** Azure costs matter; optimize for efficiency
5. **Compliance:** Data privacy, audit logs, GDPR

---

## Problem 1: Second Chance Leads (The Flagship)

### Background: Why This Matters

**Business Context:**
- ServiceTitan contractors receive 100-1000 calls/day
- ~30% of calls end without booking (customer says "let me think about it")
- Of those, ~15% actually book with a competitor or call back later
- **Revenue opportunity:** If CSRs follow up within 5 minutes, conversion rate jumps from 15% → 40%

**The Problem:**
CSRs are too busy to manually review every call. They need an AI system to flag the high-value missed opportunities.

**Success Metrics:**
- **Primary:** Incremental revenue from recovered leads
- **Secondary:** CSR time saved (only review flagged calls)
- **Constraint:** <5% false positive rate (CSRs get annoyed)

### Prompt

Design a system that analyzes call recordings within minutes of a call ending and flags missed booking opportunities for CSR follow-up.

### Requirements
- **Latency:** < 5 minutes end-to-end from call end to CSR notification
- **Scale:** ~100K calls/day across all tenants
- **Accuracy:** High recall (missing a real opportunity is worse than a false alarm)
- **Multi-tenant:** Data must be fully isolated per contractor

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Second Chance Leads System                    │
└─────────────────────────────────────────────────────────────────┘

Phone call ends
    │
    ├──> [Telephony System] (Twilio/RingCentral)
    │         │
    │         v
    │    [Webhook] POST /api/call-completed
    │         │
    │         v
    │    [Azure Service Bus] (call_completed event)
    │         │  Topic: call-events
    │         │  Partition key: tenant_id (for ordering)
    │         │
    │         v
    │    [Transcription Service]
    │         │  Azure Cognitive Services Speech-to-Text
    │         │  Async processing (~30-60s for 5min call)
    │         │  Output: transcript + speaker diarization
    │         │
    │         v
    │    [Feature Extraction Service]
    │         │  Extract structured features from transcript:
    │         │  - call_duration (seconds)
    │         │  - words_spoken (count)
    │         │  - price_mentioned (bool, regex: $\d+)
    │         │  - schedule_requested (bool, "when can you come")
    │         │  - competitor_mentioned (bool, "other company")
    │         │  - urgency_keywords (count: "emergency", "urgent", "asap")
    │         │  - hesitation_language ("let me think", "I'll call back")
    │         │  - positive_sentiment (0-1, from sentiment model)
    │         │
    │         v
    │    [ML Classifier Service]
    │         │  Model: Fine-tuned DistilBERT (128M params)
    │         │  Input: transcript + structured features
    │         │  Output: P(missed_booking) ∈ [0, 1]
    │         │  Latency: <100ms (GPU inference)
    │         │  Threshold: 0.35 (tuned for Recall@P90 precision)
    │         │
    │         v
    │    [Score Store] (Azure SQL)
    │         │  Table: call_scores
    │         │  Columns: call_id, tenant_id, score, features_json, created_at
    │         │  Index: (tenant_id, score DESC, created_at DESC)
    │         │  Row-Level Security: WHERE tenant_id = @current_tenant_id
    │         │
    │         v
    │    [Notification Service]
    │         │  Filter: score > 0.35 AND call_duration > 60s
    │         │  Rank by: score * estimated_job_value
    │         │  Push to CSR dashboard via SignalR (WebSocket)
    │         │
    │         v
    │    [CSR Dashboard]
              Display: "5 missed opportunities in last hour"
              For each: transcript snippet, score, recommended action
```

### Data Pipeline for Training

**Label Generation (Critical for Interview):**

```python
# Pseudo-SQL for label generation
SELECT 
    c.call_id,
    c.tenant_id,
    c.transcript,
    c.duration,
    c.outcome AS immediate_outcome,  -- 'booked' or 'not_booked'
    
    -- Label: Did they book within 48h after follow-up?
    CASE 
        WHEN c.outcome = 'booked' THEN 0  -- Already booked, not a miss
        WHEN EXISTS (
            SELECT 1 FROM jobs j 
            WHERE j.customer_id = c.customer_id 
            AND j.created_at BETWEEN c.ended_at AND c.ended_at + INTERVAL '48 hours'
        ) THEN 1  -- Missed opportunity (they called back or CSR followed up)
        ELSE 0  -- True negative (customer never booked)
    END AS missed_booking_label
    
FROM calls c
WHERE c.ended_at > NOW() - INTERVAL '90 days'  -- Training window
AND c.duration > 60  -- Filter out wrong numbers
```

**Why This Labeling Strategy:**
- **Automatic:** No manual annotation needed
- **Realistic:** Captures actual business outcome
- **Noisy but useful:** Some false negatives (booked with competitor), but signal is strong

**Training Pipeline:**
```
1. Daily batch job (Azure ML Pipeline)
   - Query last 90 days of calls + labels
   - Extract features (same code as serving)
   - Train/val split: 80/20 by time (not random!)
   
2. Model training (Azure ML Compute)
   - Fine-tune DistilBERT on transcript + features
   - Optimize for Recall@P90 precision (F0.5 metric)
   - Early stopping on validation PR-AUC
   
3. Model evaluation
   - Test on last 7 days (held-out)
   - Metrics: PR-AUC, Recall@P90, Precision@K (K=100)
   - Business metric: estimated revenue from flagged calls
   
4. Model deployment
   - Register in Azure ML Model Registry
   - Deploy to AKS endpoint (GPU nodes)
   - Canary: 10% traffic → 100% over 24h
   - Rollback if PR-AUC drops >5%
```

### Key Design Decisions (Explain These in Interview)

| Decision | Choice | Rationale | Alternative Considered |
|----------|--------|-----------|----------------------|
| **Labeling strategy** | Join calls to job creation timestamps | Auto-labels; no manual work | Manual annotation: too expensive |
| **Evaluation metric** | Recall@P90 precision | CSRs can handle false positives; missing leads hurts revenue | F1: treats FP/FN equally (wrong for this use case) |
| **Model architecture** | DistilBERT fine-tuned | Handles semantic patterns ("let me think about it") | Keyword rules: too brittle; GPT-4: too slow/expensive |
| **Threshold** | 0.35 (not 0.5) | Tuned for high recall | 0.5: misses too many opportunities |
| **Fallback logic** | Keyword heuristic if ML fails | 99.9% SLA requires graceful degradation | No fallback: system goes dark on ML failure |
| **Tenant isolation** | Azure SQL Row-Level Security | Automatic enforcement at DB level | App-level filtering: bug-prone |
| **Retraining frequency** | Weekly | Balance freshness vs. compute cost | Daily: too expensive; monthly: concept drift |
| **Serving latency** | <5 min end-to-end | Business requirement (CSR needs to call back quickly) | Real-time (<1s): transcription is bottleneck |

### Interview Deep Dive Questions & Answers

**Q: "How do you handle cold start for new tenants with no historical data?"**

A: Three-tier approach:
1. **Tier 1 (Day 1-30):** Use global model trained on all tenants' data
2. **Tier 2 (Day 31-90):** Blend global model (70%) + tenant-specific model (30%)
3. **Tier 3 (Day 90+):** Fully tenant-specific model

Threshold: Require ≥500 labeled calls before training tenant-specific model.

**Q: "What if the transcription service goes down?"**

A: Fallback hierarchy:
1. **Primary:** Azure Cognitive Services Speech-to-Text
2. **Fallback 1:** Keyword-based heuristic (no transcript needed)
   - Flag if: duration >3min AND customer said "let me think" (from audio keywords)
3. **Fallback 2:** Flag all calls >5min that didn't book (high recall, low precision)
4. **Alert:** Page on-call if transcription down >15min

**Q: "How do you prevent data leakage between tenants?"**

A: Defense in depth:
1. **Database:** Row-Level Security (RLS) policy on Azure SQL
   ```sql
   CREATE SECURITY POLICY tenant_isolation
   ADD FILTER PREDICATE dbo.fn_tenant_filter(tenant_id)
   ON dbo.call_scores;
   ```
2. **Application:** Every query includes `WHERE tenant_id = @current_tenant`
3. **Model serving:** Tenant ID in request header, validated against auth token
4. **Monitoring:** Alert if any query returns data for wrong tenant_id

**Q: "How do you monitor model performance in production?"**

A: Three-layer monitoring:
1. **System metrics:** Latency (P50/P95/P99), error rate, throughput
2. **ML metrics:** 
   - Prediction distribution drift (KL divergence vs. training)
   - Feature drift (mean/std of each feature vs. training)
   - Label drift (actual conversion rate of flagged calls)
3. **Business metrics:**
   - Incremental revenue from recovered leads
   - CSR satisfaction (survey: "Are flagged calls useful?")
   - False positive rate (CSRs mark "not a real opportunity")

Alert if:
- Prediction distribution shifts >20% (concept drift)
- Conversion rate of flagged calls drops >30% (model degradation)
- CSR satisfaction <3.5/5 (too many false positives)

---

## Problem 2: Atlas — Agentic AI for Contractors

### Background: Why This Matters

**Business Context:**
- ServiceTitan contractors are busy (running a business, not tech experts)
- Current UI has 100+ screens, 1000+ features
- Contractors want: "Just tell me what to do" or "Do it for me"
- **Atlas vision:** Natural language interface to entire platform

**Example Queries:**
- "How many jobs did we complete last week?" (read)
- "Show me revenue by technician this month" (read + visualization)
- "Assign the HVAC emergency to James" (write action)
- "Send a follow-up campaign to customers who haven't booked in 90 days" (complex action)

**Success Metrics:**
- **Primary:** % of queries successfully answered (<2s latency)
- **Secondary:** Actions taken per user per day
- **Safety:** 0 unauthorized cross-tenant data access

### Prompt

Design the Atlas AI assistant that can answer questions, run reports, and take actions (dispatch, campaigns) through natural language.

### Requirements
- **Latency:** <2s P99 for read operations (reports, queries)
- **Safety:** Confirm-before-execute for all write operations
- **Multi-tenant:** Each contractor sees only their own data
- **Auditability:** All actions must be logged and reversible where possible
- **Scale:** 12,000 tenants × ~50 DAU each = 600K queries/day

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Atlas AI System                           │
└─────────────────────────────────────────────────────────────────┘

User message: "How many jobs did we complete last week?"
    │
    v
[API Gateway]
    │  Authentication: JWT token → tenant_id
    │  Rate limiting: 100 req/min per tenant
    │
    v
[Intent Router] (GPT-4 with function calling)
    │  System prompt: "You are Atlas for {tenant_name}. Today is {date}."
    │  Function schema: [read_query, write_action, chitchat]
    │  Output: intent + parameters
    │
    ├──> READ PATH (80% of queries)
    │    │
    │    v
    │    [Query Planner]
    │    │  Determine data source: structured (SQL) vs unstructured (docs)
    │    │
    │    ├──> STRUCTURED DATA
    │    │    │
    │    │    v
    │    │    [Text2SQL Generator] (GPT-4 + few-shot examples)
    │    │    │  Input: "jobs completed last week"
    │    │    │  Output: SELECT COUNT(*) FROM jobs 
    │    │    │          WHERE tenant_id = ? 
    │    │    │          AND status = 'completed'
    │    │    │          AND completed_at >= DATEADD(week, -1, GETDATE())
    │    │    │
    │    │    v
    │    │    [SQL Validator]
    │    │    │  Check: tenant_id filter present, no DROP/DELETE, read-only
    │    │    │
    │    │    v
    │    │    [SQL Executor] (Azure SQL, read replica)
    │    │    │  Execute with timeout=5s
    │    │    │  Return: result set
    │    │    │
    │    │    v
    │    │    [Response Synthesizer] (GPT-3.5-turbo)
    │    │         "You completed 47 jobs last week."
    │    │
    │    └──> UNSTRUCTURED DATA (RAG)
    │         │
    │         v
    │         [Vector Store Query] (Azure AI Search)
    │         │  Query: "jobs completed last week"
    │         │  Filter: tenant_id = ? AND doc_type = 'help_article'
    │         │  Top-K: 5 documents
    │         │
    │         v
    │         [Response Synthesizer] (GPT-4)
    │              Context: retrieved docs + user query
    │              Output: "Based on your data, you completed 47 jobs..."
    │
    └──> WRITE PATH (20% of queries)
         │
         v
         [Action Planner] (GPT-4)
         │  Parse: "Assign HVAC emergency to James"
         │  Extract: job_id=?, tech_name="James", action="assign"
         │
         v
         [Entity Resolution]
         │  Lookup: "James" → tech_id=12345 (for this tenant)
         │  Lookup: "HVAC emergency" → job_id=67890 (most recent)
         │
         v
         [Action Preview]
         │  Generate: "This will assign Job #67890 (HVAC repair at 123 Main St) 
         │             to James K. (ID: 12345). Confirm?"
         │  Show to user: [Confirm] [Cancel]
         │
         v
         [User confirms]
         │
         v
         [Action Executor]
         │  Call ServiceTitan REST API: POST /api/jobs/67890/assign
         │  Body: {"tech_id": 12345, "assigned_by": "atlas"}
         │
         v
         [Audit Log] (append-only event store)
              Event: {
                "timestamp": "2026-03-07T21:00:00Z",
                "tenant_id": "tenant_123",
                "user_id": "user_456",
                "action": "job_assign",
                "job_id": 67890,
                "tech_id": 12345,
                "status": "success"
              }
```

### Multi-Tenant Isolation (Critical for Interview)

**1. System Prompt Injection (per request):**
```python
system_prompt = f"""You are Atlas, the AI assistant for {tenant_name}.

CRITICAL RULES:
- You have access ONLY to {tenant_name}'s data
- Today is {current_date}
- Their team has {n_techs} technicians and {n_customers} customers
- Never mention other contractors or tenants
- If asked about data you don't have access to, say "I don't have that information"

CONTEXT:
- Tenant ID: {tenant_id} (for your reference only, don't mention to user)
- User role: {user_role} (admin/dispatcher/tech)
"""
```

**2. RAG Vector Store Isolation:**
```python
# Azure AI Search query with tenant filter
search_query = {
    "search": user_query,
    "filter": f"tenant_id eq '{tenant_id}'",  # Mandatory filter
    "top": 5,
    "select": "content,metadata"
}

# NEVER allow cross-tenant retrieval
# Index structure: (tenant_id, doc_id) as composite key
```

**3. SQL Generation Safety:**
```python
def validate_generated_sql(sql: str, tenant_id: str) -> bool:
    """Validate SQL before execution."""
    
    # Rule 1: Must include tenant_id filter
    if f"tenant_id = '{tenant_id}'" not in sql.lower():
        raise SecurityError("Missing tenant_id filter")
    
    # Rule 2: Read-only (no writes)
    forbidden = ['insert', 'update', 'delete', 'drop', 'alter', 'create']
    if any(kw in sql.lower() for kw in forbidden):
        raise SecurityError("Write operations not allowed")
    
    # Rule 3: No subqueries that could leak data
    if 'union' in sql.lower() or 'join' in sql.lower():
        # Verify all tables have tenant_id filter
        pass  # Complex validation logic
    
    return True
```

**4. Action Execution Safety:**
```python
def execute_action(action: dict, tenant_id: str, user_id: str):
    """Execute action with safety checks."""
    
    # Verify user has permission
    if not has_permission(user_id, action['type']):
        raise PermissionError("User not authorized")
    
    # Verify entities belong to tenant
    if action['type'] == 'job_assign':
        job = get_job(action['job_id'])
        tech = get_tech(action['tech_id'])
        
        if job.tenant_id != tenant_id:
            raise SecurityError("Job belongs to different tenant")
        if tech.tenant_id != tenant_id:
            raise SecurityError("Tech belongs to different tenant")
    
    # Execute via API (not direct DB write)
    response = api_client.post(
        f"/api/jobs/{action['job_id']}/assign",
        headers={"X-Tenant-ID": tenant_id},
        json={"tech_id": action['tech_id']}
    )
    
    # Audit log
    log_action(tenant_id, user_id, action, response.status_code)
    
    return response
```

### Scaling to 600K Queries/Day

**1. Horizontal Scaling:**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: atlas-api
spec:
  replicas: 20  # Auto-scale 10-50 based on CPU
  template:
    spec:
      containers:
      - name: atlas
        image: atlas-api:v1.2.3
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
```

**2. Caching Strategy:**
```python
# Redis cache for read queries
cache_key = f"{tenant_id}:{query_hash}"
cached = redis.get(cache_key)

if cached:
    return cached  # Cache hit
else:
    result = execute_query(query)
    redis.setex(cache_key, ttl=300, value=result)  # 5min TTL
    return result

# Cache invalidation: on data write, clear tenant's cache
def on_data_write(tenant_id: str):
    redis.delete_pattern(f"{tenant_id}:*")
```

**3. Cost Optimization:**
```python
def route_to_model(query: str, complexity: int) -> str:
    """Route to appropriate model based on complexity."""
    
    if complexity < 3:  # Simple queries
        return "gpt-3.5-turbo"  # $0.002/1K tokens
    else:  # Complex queries
        return "gpt-4"  # $0.03/1K tokens
    
# Complexity scoring:
# - Simple: "How many jobs?" → GPT-3.5
# - Complex: "Analyze revenue trends and recommend pricing" → GPT-4
```

**4. Rate Limiting:**
```python
# Per-tenant token bucket
def check_rate_limit(tenant_id: str) -> bool:
    key = f"rate_limit:{tenant_id}"
    current = redis.get(key) or 0
    
    if current >= 100:  # 100 req/min
        return False
    
    redis.incr(key)
    redis.expire(key, 60)  # Reset every minute
    return True
```

### Interview Deep Dive Questions & Answers

**Q: "How do you prevent prompt injection attacks?"**

A: Multi-layer defense:
1. **Input sanitization:** Strip markdown, code blocks, system-like instructions
2. **Prompt structure:** User input in separate section, not mixed with system prompt
3. **Output validation:** Check if response mentions other tenants (red flag)
4. **Monitoring:** Alert if query contains "ignore previous instructions"

Example:
```python
def sanitize_input(user_input: str) -> str:
    # Remove potential injection attempts
    forbidden = [
        "ignore previous instructions",
        "you are now",
        "system:",
        "assistant:",
    ]
    for phrase in forbidden:
        if phrase in user_input.lower():
            raise SecurityError("Potential prompt injection detected")
    
    return user_input
```

**Q: "What if the LLM generates incorrect SQL that returns wrong data?"**

A: Validation + human-in-the-loop:
1. **SQL validator:** Check syntax, tenant_id filter, read-only
2. **Dry run:** Execute with LIMIT 1 first, show preview to user
3. **User confirmation:** "I found 47 jobs. Does this look right? [Yes] [No]"
4. **Feedback loop:** If user says "No", log as incorrect and retrain

**Q: "How do you handle 'write' actions that can't be undone?"**

A: Tiered approach:
1. **Reversible actions:** Execute immediately after confirmation
   - Example: Assign job (can reassign)
2. **Irreversible actions:** Require additional confirmation + delay
   - Example: Delete customer (show "This will permanently delete...")
   - Add 30-second undo window
3. **High-risk actions:** Require admin approval
   - Example: Bulk delete, pricing changes

---

## Problem 3: Dispatch Optimization

### Background: Why This Matters

**Business Context:**
- Dispatch is the #1 pain point for contractors
- Manual dispatch takes 2-4 hours/day for large contractors
- Poor dispatch = late arrivals, unhappy customers, lost revenue
- **Opportunity:** 10-15% revenue increase from better dispatch

**Constraints:**
- Technicians have different skills (HVAC, plumbing, electrical)
- Jobs have time windows ("between 2-4pm")
- Travel time varies by traffic, distance
- Emergency jobs arrive throughout the day
- Dispatchers need to override AI recommendations

### Prompt

Build a system that recommends (or automatically makes) technician assignments for incoming jobs, optimizing for revenue and customer satisfaction.

### Requirements
- **Day-ahead planning:** Schedule tomorrow's jobs each night
- **Real-time:** React to emergency jobs, no-shows, and tech delays
- **Scale:** ~50 techs per contractor, ~200 jobs/day for large contractors
- **Human-in-the-loop:** Dispatcher must be able to override any recommendation

### Recommended Approach: Two-Tier Architecture

**Why Two Tiers?**
- **Tier 1 (ML):** Learn patterns from data (job duration, skill match, etc.)
- **Tier 2 (Optimizer):** Solve combinatorial problem with learned inputs

This is better than end-to-end RL because:
- MILP gives optimality guarantees; RL doesn't
- MILP is explainable; RL is a black box
- MILP handles hard constraints cleanly; RL often violates them

**Tier 1: ML Models (Learned Features)**

```python
# 1. Job Duration Predictor
# Predicts: How long will this job take?
# Why: Need accurate durations for scheduling

from sklearn.ensemble import GradientBoostingRegressor

duration_model = GradientBoostingRegressor(
    loss='quantile',  # Predict P90 (add buffer)
    alpha=0.90,
    n_estimators=200
)

features = [
    'job_type',           # HVAC repair, plumbing install, etc.
    'equipment_age',      # Older equipment = longer jobs
    'tech_experience',    # Years of experience
    'time_of_day',        # Morning jobs faster (fresh tech)
    'customer_history',   # Repeat customer = faster (knows location)
]

# Training data: completed jobs with actual_duration
# Label: actual_duration (in minutes)
# Metric: MAPE (mean absolute percentage error)

# 2. Job Value Predictor
# Predicts: Expected revenue from this job
# Why: Prioritize high-value jobs

value_model = GradientBoostingRegressor()

features = [
    'job_type',
    'customer_lifetime_value',
    'service_tier',       # Premium vs. standard
    'upsell_opportunity', # Likelihood of add-ons
]

# Training data: completed jobs with actual_revenue
# Label: actual_revenue
# Metric: RMSE

# 3. Tech-Job Skill Match
# Predicts: How well does this tech match this job?
# Why: Better match = faster completion, higher quality

from sklearn.metrics.pairwise import cosine_similarity

# Learn embeddings for techs and jobs
tech_embedding = learn_embedding(tech_history)  # 32-dim vector
job_embedding  = learn_embedding(job_requirements)  # 32-dim vector

skill_match_score = cosine_similarity(tech_embedding, job_embedding)

# Training signal: completion rate, customer satisfaction
# High match = job completed on time + high rating

# 4. Travel Time Estimator
# Predicts: How long to drive from A to B?
# Why: Minimize drive time = more jobs per day

# Option 1: Google Maps API (real-time traffic)
travel_time = google_maps.distance_matrix(
    origins=[tech_location],
    destinations=[job_location],
    departure_time='now'
)

# Option 2: Learned model (cheaper, but less accurate)
# Cache results by (zone_A, zone_B, time_of_day)
```

**Tier 2: Combinatorial Optimizer (Uses ML Outputs)**

```python
from ortools.sat.python import cp_model

# Day-ahead scheduling (runs nightly)
def optimize_schedule(jobs, techs, predictions):
    """
    Solve: Assign jobs to techs to maximize revenue - travel_cost
    Subject to: skill constraints, time windows, tech availability
    """
    
    model = cp_model.CpModel()
    
    # Decision variables
    # x[j, t] = 1 if job j assigned to tech t, else 0
    x = {}
    for j in jobs:
        for t in techs:
            x[j, t] = model.NewBoolVar(f'x_{j}_{t}')
    
    # Constraint 1: Each job assigned to exactly one tech
    for j in jobs:
        model.Add(sum(x[j, t] for t in techs) == 1)
    
    # Constraint 2: Tech has required skill for job
    for j in jobs:
        for t in techs:
            if not has_skill(t, j.required_skill):
                model.Add(x[j, t] == 0)
    
    # Constraint 3: Tech capacity (max 8 jobs/day)
    for t in techs:
        model.Add(sum(x[j, t] for j in jobs) <= 8)
    
    # Constraint 4: Time windows (job must fit in tech's schedule)
    # This is complex - need to track cumulative time
    for t in techs:
        # Start time variables for each job
        start_time = {}
        for j in jobs:
            start_time[j] = model.NewIntVar(0, 1440, f'start_{j}_{t}')  # 1440 min/day
        
        # If job j assigned to tech t, must fit in time window
        for j in jobs:
            model.Add(start_time[j] >= j.earliest_start).OnlyEnforceIf(x[j, t])
            model.Add(start_time[j] + predictions['duration'][j] <= j.latest_end).OnlyEnforceIf(x[j, t])
    
    # Objective: Maximize (revenue - travel_cost)
    revenue_terms = []
    travel_cost_terms = []
    
    for j in jobs:
        for t in techs:
            # Revenue from completing job
            revenue = predictions['job_value'][j] * predictions['skill_match'][j, t]
            revenue_terms.append(x[j, t] * int(revenue))
            
            # Travel cost (time = money)
            travel_time = predictions['travel_time'][t.location, j.location]
            travel_cost = travel_time * 0.5  # $0.50/min
            travel_cost_terms.append(x[j, t] * int(travel_cost))
    
    model.Maximize(sum(revenue_terms) - sum(travel_cost_terms))
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60  # 1min timeout
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Extract solution
        assignments = []
        for j in jobs:
            for t in techs:
                if solver.Value(x[j, t]) == 1:
                    assignments.append({
                        'job_id': j.id,
                        'tech_id': t.id,
                        'start_time': solver.Value(start_time[j]),
                        'expected_revenue': predictions['job_value'][j],
                        'confidence': predictions['skill_match'][j, t]
                    })
        return assignments
    else:
        # Infeasible - fall back to greedy heuristic
        return greedy_assign(jobs, techs, predictions)


# Real-time scheduling (runs on emergency job arrival)
def realtime_insert(new_job, current_schedule, techs, predictions):
    """
    Greedy insertion: find best tech to insert new job into.
    Fast (<100ms) but suboptimal.
    """
    
    best_tech = None
    best_cost = float('inf')
    
    for t in techs:
        if not has_skill(t, new_job.required_skill):
            continue
        
        # Calculate insertion cost
        cost = (
            predictions['travel_time'][t.current_location, new_job.location]
            - predictions['job_value'][new_job] * predictions['skill_match'][new_job, t]
        )
        
        if cost < best_cost:
            best_cost = cost
            best_tech = t
    
    return best_tech


# Background re-optimization (runs every 30min)
def background_reoptimize(current_schedule, remaining_jobs, techs):
    """
    Re-run full optimization on remaining jobs.
    Allows recovery from suboptimal greedy decisions.
    """
    return optimize_schedule(remaining_jobs, techs, predictions)
```

### Why Not End-to-End Reinforcement Learning?

**RL Challenges:**
1. **No optimality guarantee:** RL finds local optima, MILP finds global
2. **Black box:** Can't explain why tech A assigned to job B
3. **Constraint violations:** RL often violates hard constraints (skill requirements)
4. **Sample inefficiency:** Needs millions of episodes to train
5. **Deployment risk:** Hard to debug when it fails

**When RL IS appropriate:**
- **Policy layer:** Which jobs to accept/reject (long-term strategy)
- **Pricing:** Dynamic pricing based on demand
- **Routing:** Multi-day routing with uncertainty

**For dispatch:** MILP + ML is the right architecture.

### Interview Deep Dive Questions & Answers

**Q: "How do you handle emergency jobs that arrive mid-day?"**

A: Three-tier response:
1. **Immediate (<1min):** Greedy insertion (find closest available tech with