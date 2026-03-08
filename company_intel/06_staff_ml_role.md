# 06 — Staff ML Role: What They're Looking For

## Two Distinct Tracks (From Job Postings)

ServiceTitan has two Staff-level ML job profiles — both are relevant:

### Track A: Staff Machine Learning Applications Engineer
*Focus: Feature engineering, MLOps, integrating models into the product*
- Salary: $150K–$216K
- Build user-facing ML features end-to-end (data → model → product)
- Work with data scientists and engineering to prototype and ship
- Azure ML, MLOps practices, microservices, Kafka/Service Bus

### Track B: Staff AI Engineer (Voice/Conversational AI)
*Focus: AI Voice Agents, ASR/TTS, real-time NLP systems*
- Salary: $202K–$270K
- Lead AI Voice Agent technical roadmap
- Deep expertise in conversational AI, ASR/TTS, LLMs, LangChain/LangGraph
- PyTorch, Hugging Face, DeepSpeech, Kaldi/ESPnet
- Reinforcement learning + continuous/online optimization systems

---

## Required Skills (Composite from All Postings)

### Must Have
- Python (expert level for ML work)
- Azure ML: pipelines, endpoints, model registry, dataset management
- Azure OpenAI Service / prompt engineering / RAG
- SQL (SQL Server specifically; also Redshift, Snowflake, PostgreSQL)
- ML fundamentals: classification, regression, time series, anomaly detection
- Deep learning frameworks: PyTorch and/or TensorFlow
- NLP/Speech: Hugging Face Transformers; ideally ASR experience
- Production ML: low-latency inference serving, fault-tolerant systems
- MLOps: model versioning, monitoring, A/B testing, retraining pipelines
- System design: distributed systems, microservices, event-driven architecture
- Git, unit testing, debugging, profiling, JIRA
- Communication: must translate technical work to PMs, execs, customers

### Strong Pluses
- LangChain / LangGraph for agentic systems
- Reinforcement learning (online optimization)
- Azure Cognitive Services (Speech/Bot Service)
- Kafka / Azure Service Bus (async messaging in ML pipelines)
- Kubernetes / containerized ML deployment
- C# / .NET familiarity (to collaborate with core platform engineers)

---

## Interview Process (from Glassdoor, Feb 2026)

**Stage 1: Recruiter Screen (~1 hour)**
- Background, motivation, general fit
- Standard format; no surprises

**Stage 2: HackerRank Coding Assessment**
- Implement a custom data structure to a given interface (not LeetCode algorithms)
- Example seen: MultiMap (dictionary mapping keys to lists of values)
  - Part 1: basic implementation (straightforward)
  - Part 2: advanced features (more complex)
- Tip: they test interfaces and data structures, not DP/graph puzzles

**Stage 3: Technical Interviews (3 rounds, ~1.5 hours each via HackerRank)**
- Each round involves implementing an interface
- Topics seen: data structures, async/await and parallel programming
- Process is long (~5 weeks total), with 3–4 day waits between rounds
- Interviewers are described as nice and provide hints

**Stage 4: System Design + Behavioral (inferred from role level)**
- For Staff level: expect ML system design (design a feature end-to-end)
- For data engineers: SQL + data pipeline questions confirmed
- Behavioral: expect questions about leading technically, cross-functional work,
  handling ambiguity, defining roadmaps

---

## What to Emphasize in Interview

Based on the job descriptions and company context, weight your prep toward:

### 1. Azure ML Platform Depth
Know the full Azure ML workflow: dataset creation, pipeline authoring, model
registration, online endpoint deployment, monitoring. Be able to walk through
how you'd build a training + serving pipeline for Second Chance Leads.

### 2. LLM/RAG Architecture
Design an end-to-end RAG system. Know Azure AI Prompt Flow. Understand context
window management, retrieval strategies (dense vs. sparse), re-ranking, and
how to evaluate a RAG pipeline.

### 3. Agentic AI / LangGraph
Atlas is the company's flagship product. Know how to design a tool-using agent
with state machines (LangGraph), function calling, confirm-before-execute patterns
for write operations, and streaming output.

### 4. Real-Time ML Serving
Second Chance Leads fires within minutes. AI Voice Agents operate in real-time.
Know latency budgets, model optimization (quantization, ONNX, TensorRT), and
online inference architecture.

### 5. Multi-Tenant ML
Be ready to discuss: global vs. per-tenant models, cold start problem, data
isolation, personalization strategies (fine-tuning vs. RAG vs. in-context learning).

### 6. MLOps at Scale
Training pipelines, experiment tracking, model registry, A/B testing, shadow
deployment, data drift detection, retraining triggers.

### 7. Staff-Level Behaviors
- "I owned the ML platform decision for X" — scope and ownership language
- "I defined the technical roadmap for Y" — strategy language
- "I mentored Z engineers through W problem" — leadership language
- Communicate the business impact, not just the model metrics

---

## Compensation Benchmarks

| Role | US Range |
|---|---|
| Staff ML Applications Engineer | $150K–$216K base |
| Staff AI Engineer (Voice/Conversational) | $202K–$270K base |

Both include annual bonus + equity (RSUs) + comprehensive benefits.
Poland engineering hub roles are listed at 30,133–45,200 PLN/month gross.

---

## Key Question to Be Ready For

*"Tell me about the AI/ML work you've done that had the most business impact."*

At Staff level, the answer needs to include: what you built, how it was deployed,
how it performed in production, how you measured success, and what happened to the
business as a result. Avoid describing research or prototype work as if it shipped.
