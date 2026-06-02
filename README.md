# Stock Analyzer

A research-first stock analysis toolkit built around three institutional-grade `.agents` workflows.

This repo combines workflow orchestration, analyst-style financial modeling, and structured output generation to support single-ticker initiation research, portfolio reviews, and secular trend analysis.

## Core workflows in `.agents/workflows`

### 1. `ticker-analysis`
Responsible for deep, multi-skill initiation research on a single ticker.

What it does:
- Gathers fundamentals, momentum, and risk metrics.
- Runs DCF and comps valuation scripts.
- Generates a technical setup and earnings/catalyst assessment.
- Produces an institutional-quality `out/[TICKER]_Initiation_Report.md`.

When to use:
- You need a full research note for one ticker.
- You want definitive actionable guidance for buyers and current holders.

### 2. `short-term-portfolio-review`
Designed to review a portfolio of tickers and create a tactical short-term action report.

What it does:
- Reads the portfolio list from `ticker-list-s.txt`.
- Validates CAD holdings and native CAD prices.
- Runs `ticker-analysis` for each position in parallel.
- Synthesizes a portfolio-level report in `out_master/[YYYY-MM-DD]/Short_Term_Portfolio_Review.md`.

When to use:
- You need a 1–3 month tactical review of a real portfolio.
- You want buy/trim/exit guidance across multiple positions.

### 3. `secular-analysis`
Built for long-term, macro-driven secular trend investing.

What it does:
- Analyzes sector tailwinds and the company’s value chain position.
- Screens for moat strength, capital intensity, and structural risk.
- Builds a falsifiable thesis with kill criteria and DCF support.
- Produces `out_secular/[TICKER]_Secular_Datapack.md` and `out_secular/[TICKER]_Secular_Playbook.md`.

When to use:
- You are evaluating a stock as a long-term core holding.
- You need a precise, time-bound secular thesis and portfolio strategy.

## Repository structure

- `.agents/workflows/` — workflow definitions for each agent pipeline.
- `.agents/skills/` — reusable skill modules powering the workflows.
- `out/` — single-ticker outputs and reports.
- `out_master/` — portfolio review deliverables.
- `out_secular/` — long-term secular analysis deliverables.
- `ticker-list-s.txt` — sample portfolio input for short-term review.


## How to use

1. Run the appropriate workflow with your agent tooling.
2. Review generated reports in `out/`, `out_master/`, or `out_secular/`.
