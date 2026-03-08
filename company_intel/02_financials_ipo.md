# 02 — Financials & IPO

## IPO Summary

- **IPO date**: December 12, 2024
- **Exchange**: Nasdaq
- **Ticker**: TTAN
- **IPO price**: $71/share (upsized from $52–57 initial range)
- **Opening trade**: $101/share (42% first-day pop)
- **Shares offered**: 8.8M
- **Capital raised**: ~$625M
- **Implied valuation at open**: ~$18–20B

---

## Key Financial Metrics (as of most recent filings)

| Metric | Value | Notes |
|---|---|---|
| Revenue (FY2025) | $772M | +26% YoY |
| Revenue (FY2024) | $614M | +31% YoY |
| Implied ARR (Jul 2024) | $772M | Per S-1 |
| Gross Transaction Volume | $68.5B | FY2025 |
| Gross Dollar Retention | >95% | 10-quarter streak |
| Net Dollar Retention | >110% | Existing customers expand |
| Non-GAAP Platform Gross Margin | 77% | Platform-only (excl. FinTech) |
| Non-GAAP Operating Margin | ~2–5% | Improving rapidly |
| Net Loss (FY2024) | $(183M) | Still GAAP-negative |

Revenue run rate (TTM through Oct 2025) was approximately $916M — the company
is on track toward $1B ARR.

---

## Revenue Mix

| Stream | Share | Type |
|---|---|---|
| Subscription (Core + Pro) | ~71% | Recurring |
| Usage (FinTech / payments) | ~25% | Usage-based |
| Professional Services | ~4% | One-time |

The usage-based FinTech component is important — it ties ServiceTitan's revenue
directly to the volume of work their customers complete. When a tech closes a job
and processes a payment, ServiceTitan earns a ~0.25% take rate on that transaction.

---

## Unit Economics

- **Average Revenue Per Customer**: ~$78K/year
- **Minimum customer threshold**: $10K annualized billing to be counted "active"
- **Enterprise tier**: Accounts >$100K ARR represent >50% of total billings
- **Top customers**: Accounts >$250K ARR growing meaningfully

---

## Why This Matters for ML Interview

The financial structure creates specific ML priorities:

1. **Churn has massive LTV impact** — losing a $78K/year customer costs more than a
   consumer SaaS churn; prediction must be precise, not just recall-maximizing
2. **FinTech revenue grows with job volume** — demand forecasting and dispatch
   optimization directly improve the bottom line, not just customer happiness
3. **Net dollar retention >110% means upsell/expansion matters** — recommendation
   and propensity models have clear revenue attribution
4. **Pro Products are the growth vector** — "Pro users see 67% higher job growth" is
   a cited metric; ML inside Pro Products is the monetization engine

---

## Investor Base

Thoma Bravo, Bessemer Venture Partners, ICONIQ Capital, Sequoia Capital Global
Equities, Tiger Global Management, Battery Ventures.

The Series H (Nov 2022) had a compounding IPO ratchet that pressured the company
to IPO before $84.57/share threshold, adding urgency to the December 2024 timeline.
