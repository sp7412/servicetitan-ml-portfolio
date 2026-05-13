# ML/DS Notebooks 22–26: Targeted Additions for ServiceTitan Reqs

Five new notebooks for the `servicetitan-ml-portfolio` repo, each one mapped to
a specific named requirement in a currently-open ServiceTitan ML/DS req as of
May 2026. All five executed end-to-end via `nbconvert` before delivery.

## Files in this delivery

| Notebook | Maps to req | Topic |
|----------|-------------|-------|
| `22_llm_eval_guardrails.ipynb` | Senior DS (Onboarding) — names RAGAS/DeepEval | LLM evaluation harness, RAGAS-style metrics from scratch, DeepEval-style assertions, prompt-injection guards, PII redaction, schema validation, LLM-as-judge cost cascade |
| `23_financial_forecasting.ipynb` | Lead DS (Operations/Finance) — names forecasting + optimization | Hierarchical forecasting with reconciliation, quantile (P10/P50/P90) GBMs, rolling z-score + Isolation Forest anomaly detection, SLSQP budget optimization, Monte Carlo margin simulation |
| `24_mcp_server_servicetitan.ipynb` | Senior DS + Lead DS — both name MCP | MCP protocol primer, minimal server from scratch (JSON-RPC 2.0), four ST tools (jobs/techs/customers/revenue), tenant isolation, audit log, LangGraph agent wiring, production checklist |
| `25_causal_inference.ipynb` | Every senior+ req | Power & sample sizing, peeking + multiple comparisons demos, CUPED variance reduction, switchback experiments, difference-in-differences, propensity score matching |
| `26_onboarding_acceleration.ipynb` | Senior DS (Onboarding) — direct topical match | Kaplan-Meier survival from scratch, GBM milestone propensity scoring (AUC ~0.85), funnel bottleneck detection, GenAI personalized interventions, 3-tier cost-aware routing, A/B evaluation of intervention type |

## Design choices

- **No hard SDK dependencies on RAGAS / DeepEval / MCP Python SDK / lifelines.**
  Implementations are from-first-principles so the underlying math is visible. Every
  notebook calls out the production SDK that would replace the hand-rolled version
  and points to the docs/install command.
- **All data synthetic.** Each notebook seeds its RNG and runs in under 30 seconds.
- **All code runs offline.** No API keys needed; LLM calls are deterministic stubs.
- **Production-shaped, not toy.** Type hints, docstrings, dataclasses, audit logs,
  schema validation, multi-tenant auth, observability checklists. Reads like
  something you'd ship.

## How they slot into the existing portfolio

```
Existing notebook → New notebook that extends it
─────────────────────────────────────────────────
11 (LangGraph)    → 22 (eval guardrails for the agent), 24 (MCP for the agent)
13 (RAG)          → 22 (RAGAS metrics on the retriever)
07 (forecasting)  → 23 (production-grade FP&A forecasting)
02 (dispatch opt) → 23 (linear vs nonlinear optimization), 25 (switchback experiment design for it)
20 (LLM selection) → 22 (eval/judge cascade for cost-aware model routing)
04 (call NLP)     → 26 (onboarding intervention generation reuses the prompt patterns)
```

## Suggested README integration

Add to the portfolio README's notebook table:

```markdown
| [22](22_llm_eval_guardrails.ipynb)         | **LLM Evaluation & Guardrails**     | RAGAS, DeepEval, injection/PII guards, judge cascade |
| [23](23_financial_forecasting.ipynb)       | **Financial Forecasting & Optimization** | Hierarchical + quantile forecasting, budget allocation, MC simulation |
| [24](24_mcp_server_servicetitan.ipynb)     | **MCP Server for ServiceTitan**     | Protocol from scratch, tenant isolation, agent wiring |
| [25](25_causal_inference.ipynb)            | **Causal Inference & Experiments**  | Power, CUPED, switchback, DiD, PSM |
| [26](26_onboarding_acceleration.ipynb)     | **Customer Onboarding Acceleration** | Survival, propensity, GenAI routing, A/B eval |
```

## Total deliverables across this conversation

- **8 new notebooks** (22-29) — 5 ML/DS + 3 coding interview prep
- **150 verified test cases** across the coding notebooks
- **All notebooks executed** end-to-end before delivery; outputs match
- **Mapped to specific JD bullet points** in currently-open ST reqs

## Interview talking points by notebook

For each, here's the sentence to lead with if it comes up:

- **22**: "I treat LLM evaluation like a CI test suite — RAGAS-style metrics on a
  versioned golden set, plus injection/PII guards as separate gates. Here's the
  cost cascade that keeps judge bills sane in production."
- **23**: "FP&A forecasting needs probabilistic outputs, not point estimates.
  Quantile GBMs give you P10/P50/P90, then MC for margin distribution, then
  optimization on the median allocation."
- **24**: "MCP is just JSON-RPC 2.0 with a tool registry. I'd run ST's MCP
  server as a Python sidecar (or a C# port) with OAuth tied to the existing app
  keys, audit log to the SIEM, and read-only by default."
- **25**: "Most A/B tests at SaaS scale fail one of three ways — peeking,
  multiple comparisons, or non-randomizable units. CUPED for noise, switchback
  for dispatch-style changes, DiD for staged rollouts, PSM as last resort."
- **26**: "Time-to-first-job is the right onboarding KPI. Build a propensity
  model for early-warning, segment by intervention cost-effectiveness, eval
  with an A/B on intervention type."
