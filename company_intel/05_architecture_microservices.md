# 05 — Architecture & Microservices

## Where They Started: The Monolith

ServiceTitan launched in 2012 as a .NET monolith — a single C# application backed
by Microsoft SQL Server, deployed on Azure. This is standard for SaaS startups. The
monolith served them well through early growth but created scaling challenges as
they hit thousands of tenants and tens of millions of jobs.

Evidence of the monolith-era:
- All job postings reference "microservices architecture" as something they are *building*,
  not something fully in place — indicating active migration
- Engineering blog posts reference "microservices architecture" as an aspiration and
  ongoing project, not a completed state
- Job postings explicitly call out: "Experience with microservices and asynchronous
  messaging technologies like Kafka, Azure ServiceBus" as a *plus*, not required —
  meaning not everyone is working in microservices yet

---

## Current State: Active Migration

ServiceTitan is in a **monolith-to-microservices migration** phase. The pattern
used by companies at their scale is typically the **Strangler Fig** approach:

1. An API gateway or proxy sits in front of the monolith
2. New features are built as independent microservices
3. Old monolith functionality is progressively re-implemented in services
4. Traffic is shifted service by service until the monolith is "strangled"

Key signals about their current architecture:

- **Kubernetes (AKS)** is listed in all recent job postings — containerized workloads
- **Azure Service Bus** and **Kafka** are both referenced for async messaging — the
  two common choices for event-driven service communication
- **ML services are separate** — the Titan Intelligence ML platform runs on Azure ML
  endpoints, decoupled from the core .NET application
- **Contact Center Pro** is explicitly described as a separate product with its own
  AI backend — a clear microservice boundary
- **API-first design** — job postings reference "custom API development" and REST APIs
  as core to their architecture

---

## Event-Driven Architecture

The transition to microservices at ServiceTitan almost certainly involves event
streaming because:

1. The core domain is inherently event-driven: a phone call happens → a booking
   is created → a tech is assigned → the job is completed → an invoice is sent →
   payment is processed. Each step is an event.

2. The ML platform needs to consume events asynchronously (e.g., Second Chance
   Leads fires "within minutes of a call completing" — this is an event consumer
   pattern, not a polling pattern).

3. Azure Service Bus (confirmed in job postings) and Kafka (referenced) are the
   two messaging technologies in use.

**Likely event flow for Second Chance Leads:**
```
Call ends (telephony event)
  → published to Azure Service Bus / Kafka
  → consumed by TI ML service
  → ASR transcription (Azure Cognitive Services)
  → LLM classification (Azure OpenAI)
  → scored lead written back to SQL Server
  → push notification to CSR dashboard
  (Total latency: <5 minutes)
```

---

## ML Service Architecture

Based on the Azure case study and job postings, the ML platform likely looks like:

```
┌─────────────────────────────────────────────────┐
│               ServiceTitan Core                  │
│         (C# / .NET / SQL Server)                │
└────────────────────┬────────────────────────────┘
                     │ events / REST
          ┌──────────▼──────────┐
          │  Azure Service Bus  │
          │  / Kafka topics     │
          └──────┬──────┬───────┘
                 │      │
    ┌────────────▼┐  ┌──▼────────────────────┐
    │  TI ML      │  │  Azure ML Endpoints    │
    │  Service    │  │  (model serving)       │
    │  (Python)   │  │                        │
    └────────────┬┘  └──┬─────────────────────┘
                 │      │
          ┌──────▼──────▼──────────────┐
          │  Azure OpenAI Service      │
          │  Azure Cognitive Speech    │
          │  Azure ML Model Registry   │
          └────────────────────────────┘
```

Training pipelines run on **Azure ML pipelines** using Python, with models
registered in the **Azure ML model registry** and deployed to **Azure ML endpoints**
(managed online endpoints for real-time serving).

---

## Multi-Tenancy Considerations for ML

With ~12,000 contractor tenants, ML at ServiceTitan has a multi-tenancy problem
that most systems don't:

- **Global models vs. per-tenant models**: A single churn model must work for a
  2-tech plumbing shop and a 200-tech HVAC enterprise. Feature engineering must
  account for scale differences.
- **Data isolation**: One contractor's pricing and customer data must never influence
  another's model outputs. Privacy is a product requirement.
- **Cold start**: New customers have no historical data. The system must bootstrap
  from industry priors until enough tenant-specific data accumulates.
- **Atlas personalization**: Atlas is explicitly described as adapting to "the unique
  context of your business" — this implies per-tenant context storage and potentially
  per-tenant fine-tuning or RAG over tenant-specific data.

---

## Deployment Patterns

From job postings and engineering culture signals:

- **CI/CD is table stakes** — TeamCity-based pipelines, Git branching discipline
- **Blue/green or canary deployments** — standard for SaaS at this scale; needed
  to avoid downtime for 24/7 contractor operations
- **Feature flags** — referenced in engineering discussions; used for gradual rollout
- **Kubernetes** — all new services containerized; AKS for orchestration
- **Azure regions** — ML workloads co-located with application workloads to minimize
  latency and satisfy data residency requirements

---

## What "Staff" Means in This Context

At ServiceTitan's scale, a Staff ML Engineer is expected to:

1. Define the technical architecture for new ML products, not just implement them
2. Make the monolith-to-microservices boundary decisions for ML services
3. Own the Azure ML platform — model lifecycle, versioning, A/B test infrastructure,
   monitoring, retraining triggers
4. Collaborate with Core Platform engineers on event schema design
5. Drive LLMOps practices (prompt versioning, eval frameworks, safety guardrails)
6. Be the technical authority for multi-tenant ML isolation patterns
