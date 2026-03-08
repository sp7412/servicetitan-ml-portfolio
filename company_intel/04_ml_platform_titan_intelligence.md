# 04 — ML Platform & Titan Intelligence

## What Is Titan Intelligence (TI)?

Titan Intelligence is ServiceTitan's branded AI/ML product suite, described as
"purpose-built AI for the trades." It is not a single model — it is a portfolio
of ML and generative AI features embedded across the Pro Products platform, all
built on Azure ML and Azure OpenAI.

The internal division is called **"Data, Titan Intelligence, and AI"** and is
separate from core product engineering. This is where a Staff ML Engineer would
likely sit.

---

## The ML Infrastructure (Azure ML)

Per the Microsoft Azure case study, ServiceTitan uses the following Azure services:

- **Azure Machine Learning** — training pipelines, model registry, dataset management,
  endpoints for serving
- **Azure OpenAI Service** — GPT-4 class models for generative AI features
- **Azure AI Prompt Flow** — building and deploying RAG pipelines and chat/voice bots
- **Azure Cognitive Services (Speech)** — ASR for call transcription

Key engineering quote from Lilit Zargaryan (Staff ML Engineer, ML Platform within TI):
"Building an AI platform can be a major, challenging process... most traditional AI
applications required you to solve every problem yourself."

Key quote from Mehmet Ezbiderli (Principal Architect, Data & ML):
"Azure AI also had the major advantage of serving the model from within the Azure
region where our services are located" — avoiding latency and keeping PII in-house.

---

## Current Titan Intelligence Feature Inventory

### Call & Lead Intelligence
| Feature | How It Works | ML Type |
|---|---|---|
| **Second Chance Leads** | Analyzes call transcripts of unbooked/dismissed calls; flags high-likelihood-to-rebook ones; fires within minutes of call end | ASR + LLM classification + scoring |
| **AI Voice Agents** | 24/7 inbound call handling; books jobs, reschedules, answers questions; integrates with live ST data | ASR + NLU + dialogue management + TTS |
| **SMS Booking Agent** | Same as voice agents but over text | NLU + state machine |
| **Contact Center Pro** | Multichannel AI contact center with queue routing, sentiment analysis | NLP + routing ML |

**Key stat**: Second Chance Leads — over 50% of outbound follow-up calls result in
a booked job. Users recapture ~37% of unconverted calls. One customer (Bonfe) added
$40K in one month.

### Dispatch & Scheduling
| Feature | How It Works | ML Type |
|---|---|---|
| **Dispatch Pro** | Assigns best-fit technician per job based on skills, proximity, recent sales performance, job value prediction | Multi-objective optimization + regression |
| **Dispatch Assist** | Recommends assignments; dispatcher accepts/rejects | Same as above with human-in-loop |
| **Job Value Predictor** | Predicts revenue potential of a job at time of booking | Regression |
| **Demand-Based Capacity** | Adjusts scheduling capacity based on demand forecasts | Time series forecasting |

**Key stat**: 2x increase in capacity per dispatcher with Dispatch Pro.

### Sales & Field Intelligence
| Feature | How It Works | ML Type |
|---|---|---|
| **Field Pro / Sales Pro** | Pre-job AI briefing, AI-guided diagnostics, post-job coaching, close rate tracking | NLP + scoring + recommendation |
| **AI Coaching (Boost Sales)** | Surfaces missed upsell opportunities, coaches on call behavior | NLP classification |
| **Financing Plan Optimizer** | Recommends conservative/balanced/aggressive financing plan based on historical conversion | Policy optimization |

### Pricing & Market Intelligence
| Feature | How It Works | ML Type |
|---|---|---|
| **Price Insights (Pricebook Pro)** | Shows how a contractor's price compares to regional averages | Regression + market data aggregation |
| **Ads Optimizer** | Feeds revenue + customer data back into Google Ads; trains Google to optimize for closed jobs, not just calls | Conversion attribution + audience ML |
| **Quarterly Benchmark Report** | Compares your KPIs to similar businesses | Clustering + statistical benchmarking |

### Agentic AI (2025+)
| Feature | How It Works |
|---|---|
| **Atlas** | Natural-language AI sidekick; runs reports, dispatches techs, surfaces insights, takes actions. Described as "the ultimate power user of ServiceTitan." Announced Sept 2025 at Pantheon. Connects to Pro Product automations to create fully automated AI workflows. |
| **Atlas Campaign Recommendations** | Monitors schedule; if light, recommends/triggers marketing campaigns. If full, throttles spend. |

---

## Atlas: The Current Flagship

Atlas (announced Pantheon 2025) represents the strategic evolution from
feature-level AI to an **agentic, multi-step AI** that:

- Understands natural language queries in the context of the contractor's business
- Has access to the full ServiceTitan data graph (jobs, customers, techs, inventory)
- Can take direct action (not just recommend) — e.g., trigger a campaign, reroute a tech
- Learns over time from interactions within a specific contractor's context
- Is embedded in mobile (technician-facing) and office UI simultaneously

This is explicitly an **agentic AI** play — tool use, action-taking, long-horizon
planning from a domain-specific LLM grounded in real-time operational data.

For a Staff ML Engineer, this is the most technically interesting and scope-expansive
area to discuss in an interview.

---

## ML Problem Taxonomy (Internally Relevant)

Mapping the product surface area to ML problem types:

| Business Problem | ML Formulation |
|---|---|
| Will this customer churn? | Binary classification on account-level features |
| Which technician should get this job? | Multi-objective combinatorial optimization with learned utility |
| Was this call a missed booking? | Binary classification on ASR transcript |
| What will job demand look like next week? | Time series forecasting (multivariate) |
| What price should I charge? | Causal inference + revenue optimization |
| Will this estimate close? | Binary classification (lead scoring) |
| Which customers are ready for an upsell? | Multi-label propensity scoring |
| What ad budget should I allocate? | Bid optimization + attribution modeling |
| Is this driving behavior risky? | Anomaly detection / classification on telematics |

---

## Data Assets (The Moat)

ServiceTitan processes $68.5B in annual GTV. This means they have:

- Millions of call recordings with matched booking outcomes
- Full job lifecycle data (booked → dispatched → completed → invoiced → paid)
- Technician-level performance data over years
- Price book data across tens of thousands of contractors and millions of SKUs
- Customer equipment history with age, service records, and replacement patterns
- Regional demand patterns tied to weather, seasons, and economic conditions

This proprietary data, combined with tight vertical focus, is what makes their AI
defensible. A generic LLM does not know that a 14-year-old heat exchanger in Phoenix
in October means a specific replacement probability.
