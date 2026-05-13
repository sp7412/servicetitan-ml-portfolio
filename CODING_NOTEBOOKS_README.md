# Coding Interview Prep — Notebooks 27, 28, 29

Three new notebooks for the ServiceTitan portfolio. Each covers 5 problems with
problem statement, naive vs. optimal approaches with complexity, full solution,
and **10 progressive test cases per problem** (basic → edge → stress → adversarial).

**Total: 15 problems, 150 verified test cases.** All asserts pass end-to-end
(notebooks were executed via `nbconvert` before delivery).

## Notebooks

| File | Audience | Problems |
|---|---|---|
| `27_coding_servicetitan_top5.ipynb` | **ServiceTitan HackerRank screen** | VersionedMultiMap, LRUCache (linked-list), async fetch_all w/ concurrency limit, JobScheduler (heap + lazy delete), SlidingWindowRateLimiter |
| `28_coding_leetcode_top5.ipynb` | **Generic FAANG screens** (Shield AI, Vantor, Helsing, Striveworks, etc) | Two Sum, Valid Parentheses, Merge Intervals, LRUCache (OrderedDict), Course Schedule (topo sort / cycle detection) |
| `29_coding_ml_engineer_top5.ipynb` | **Staff ML engineer screens** | Numerically stable softmax + cross-entropy, K-means from scratch, Top-K streaming with min-heap, Rolling window statistics (Welford + monotonic deques), Scaled dot-product attention from scratch |

## Why three notebooks instead of one

The screening formats differ enough that one notebook would either be 50%
irrelevant for any given interview or so shallow it doesn't help. Splitting by
audience lets you drill the right set the day before each interview:

- **ServiceTitan callback?** → drill 27. The Glassdoor reports are clear that
  their HackerRank is custom-data-structure-heavy, not graph mediums.
- **Generic SWE-style screen?** → drill 28. Portable across the rest of the
  target list.
- **Staff ML role with a "code an ML primitive" round?** → drill 29.
  The attention problem in particular is a credibility marker — it shows you
  understand what's actually happening inside a transformer rather than just
  using one.

LRU intentionally appears in both 27 and 28 with different implementations
(hand-rolled linked-list vs. `OrderedDict`). A real interviewer will sometimes
ask both — "now do it idiomatically" — and knowing only one way trips candidates.

## Suggested README integration

Append to the main portfolio README's notebook table:

```markdown
| [27](27_coding_servicetitan_top5.ipynb)   | **Coding: ServiceTitan Top 5**  | VersionedMultiMap, LRU (linked-list), async fetch, priority scheduler, rate limiter |
| [28](28_coding_leetcode_top5.ipynb)       | **Coding: Classic LeetCode Top 5** | Two Sum, Valid Parens, Merge Intervals, LRU (OrderedDict), Course Schedule |
| [29](29_coding_ml_engineer_top5.ipynb)    | **Coding: ML Engineer Top 5**   | Softmax + CE (stable), K-means, Top-K heap, Rolling stats, Scaled dot-product attention |
```

## Verifying the notebooks

Each notebook has a "Final Sanity Check" cell at the end that prints all 5
problems as PASS once you've run every cell top to bottom. If anything fails,
the failure will surface at the per-problem test cell, not the final summary.

The async notebook (27, problem 3) needs `nest_asyncio` in Jupyter; it's
imported at the top of that test cell with a try/except so it gracefully
degrades when run as plain Python.

## What's next (open questions for Seth)

The earlier conversation flagged five additional ML/portfolio notebooks worth
building based on current ServiceTitan reqs:

- **22 — LLM Evaluation & Guardrails** (RAGAS, DeepEval; explicitly named in the
  Senior DS req)
- **23 — Financial Forecasting & Budget Optimization** (Lead DS req focus)
- **24 — MCP Server for ServiceTitan Tools** (preferred in both Senior/Lead DS reqs)
- **25 — Causal Inference & Experimental Design** (every senior+ req mentions it)
- **26 — Customer Onboarding Acceleration** (direct match to open Senior DS req)

If you want any of these built next, the LLM evaluation one is the highest-
leverage since it's named in the JD and all the prerequisites already exist in
notebooks 10/11/13/20/21.
