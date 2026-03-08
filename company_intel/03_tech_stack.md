# 03 — Tech Stack

Primary source: ServiceTitan engineering blog (Medium), Built In interviews, job postings.

---

## Backend

| Layer | Technology |
|---|---|
| Primary language | **C# / .NET / .NET Core** |
| API framework | **ASP.NET MVC**, Web APIs |
| ML / Data Science | **Python** |
| Secondary services | **Java**, **Node.js** |
| Runtime orchestration | **Kubernetes** |
| Messaging / async | **Azure Service Bus**, **Apache Kafka** (referenced in job postings) |
| Build system | **TeamCity**, CI/CD pipelines |

The engineering team is explicitly ".NET-first." One engineering lead from Built In
described it as: "With a backend stack built on .NET, utilizing Microsoft Azure cloud
services, we emphasize high-quality code, stringent coding standards, and ongoing
refactoring."

---

## Frontend

| Layer | Technology |
|---|---|
| Modern UI | **React**, **TypeScript** |
| Legacy UI | **JavaScript** |
| Mobile | **Apache Cordova** (hybrid), being replaced by native **Field Mobile App** |

The mobile app has a notable technical requirement: **offline capability**. Field
technicians operate in dead zones, so the app supports local data persistence, action
queuing, and server synchronization with graceful rollback on sync failures.

---

## Data & Analytics

| System | Technology |
|---|---|
| Primary OLTP | **Microsoft SQL Server** |
| Analytics / Data Warehouse | **Amazon Redshift** |
| Caching | **Redis** |
| Additional warehousing | **Snowflake**, **PostgreSQL** (referenced in job postings) |
| Orchestration | **Apache Spark** (Data Engineer JDs) |

SQL Server is the system of record. Redshift and Snowflake are used for
analytical workloads and ML feature pipelines.

---

## Cloud & Infrastructure

| Category | Technology |
|---|---|
| Primary cloud | **Microsoft Azure** |
| Backup/secondary | **AWS** |
| ML platform | **Azure Machine Learning** |
| LLM APIs | **Azure OpenAI Service** |
| Prompt/agent tooling | **Azure AI Prompt Flow** |
| ASR / speech | **Azure Cognitive Services (Speech)** |
| Container orchestration | **Kubernetes (AKS)** |
| Model registry | Azure ML model registry |
| Training pipelines | Azure ML pipelines |

The Azure-first choice is strategic: running models in the same Azure region as
their services eliminates cross-region latency and simplifies data privacy/PII
compliance (data stays in-house). Per Mehmet Ezbiderli (Principal Architect):
"Azure AI also had the major advantage of serving the model from within the Azure
region where our services are located."

---

## ML-Specific Tooling (from job postings and case studies)

| Category | Tools |
|---|---|
| Deep learning | PyTorch, TensorFlow |
| NLP / Speech | Hugging Face Transformers, DeepSpeech, Kaldi/ESPnet |
| Agentic / LLM orchestration | LangChain, LangGraph |
| RAG | Azure AI Prompt Flow + Azure OpenAI |
| Feature store / training | Azure ML datasets, pipelines, endpoints |
| Experiment tracking | Azure ML (model registry + runs) |
| MLOps | AzureML, AIOps, LLMOps practices |
| Version control | Git |
| Project tracking | JIRA |
| Code review / CI | HackerRank (interviews), TeamCity (internal CI) |

---

## Key Architectural Characteristics

- **Multi-tenant SaaS**: One platform serves ~12,000 contractors; tenant isolation
  is critical for data privacy (a contractor's pricing/customer data must not leak)
- **High-volume transactional**: Millions of jobs, calls, and invoices processed daily
- **Offline-first mobile**: The tech app must function without connectivity
- **Monolith migrating to microservices**: The core platform originated as a monolith
  and is actively being decomposed; new services use event-driven patterns
- **Real-time requirements**: Dispatch optimization, call analysis (Second Chance
  Leads fires within minutes of call end), and AI voice agents require low latency

---

## Engineering Culture Signals

- "High-quality code, stringent coding standards, ongoing refactoring" (Built In)
- CI/CD discipline is expected; TeamCity is the internal CI system
- Globally distributed teams (US + Poland engineering hub opened 2024)
- Staff engineers are expected to mentor, define technical roadmaps, and communicate
  across engineering/infrastructure/data science/product
