# Stock Analyzer: Agentic Workflow Orchestration

A research-first stock analysis toolkit designed for AI agents, built around three institutional-grade `.agents` workflows.

This repository combines workflow orchestration, analyst-style financial modeling (DCF and Comps), and structured markdown generation to support single-ticker initiation research, portfolio reviews, and secular trend analysis.

## Agentic Execution & Core Workflows

Agents can trigger these primary workflows via their corresponding slash commands. All heavy lifting is handled by centralized Python scripts located in `.agents/skills/`.

### 1. `/ticker-analysis`
Responsible for deep, multi-skill initiation research on a single ticker.

* **What it does:**
  - Gathers fundamental, momentum, and risk metrics using `compute_indicators.py`.
  - Runs DCF and relative valuation (Comps) via Python automation.
  - Checks for "Relative Oversold" institutional dip setups using `find_dip.py`.
  - Produces an institutional-quality `out/[TICKER]_Initiation_Report.md`.
* **When to use:**
  - You need a full research note for one specific stock.
  - You want definitive actionable guidance for new buyers vs. current holders.

### 2. `/short-term-portfolio-review`
Designed to batch-review a portfolio of tickers and create a tactical short-term action report (1-3 month horizon).

* **What it does:**
  - Reads the portfolio list from `ticker-list-s.txt`.
  - Extracts the exact CAD exchange pricing using `fetch_cad_price.py` to prevent currency hallucination.
  - Uses `invoke_subagent` to run `/ticker-analysis` for each position in parallel.
  - Synthesizes a portfolio-level strategy report in `out_master/[YYYY-MM-DD]/Short_Term_Portfolio_Review.md` based on absolute position sizing and technical confluence.
* **When to use:**
  - You need a tactical review of a live portfolio to determine precise Add on Dip, Hold, or Trim targets.

### 3. `/secular-analysis`
Built for long-term, macro-driven secular trend investing.

* **What it does:**
  - Analyzes sector tailwinds and the company’s value chain position.
  - Screens for moat strength, capital intensity, and structural risk.
  - Builds a falsifiable thesis with kill criteria and DCF support.
  - Produces `out_secular/[TICKER]_Secular_Datapack.md` and `out_secular/[TICKER]_Secular_Playbook.md`.
* **When to use:**
  - You are evaluating a stock as a long-term core holding (1+ year timeframe).

## Repository Structure & Stack

- **`.agents/workflows/`** — Workflow definitions (YAML/Markdown) for each agent pipeline.
- **`.agents/skills/`** — Reusable skill modules (Python scripts) powering the workflows.
  - *Tech Stack:* `Python`, `uv`, `yfinance`, `pandas`, `pandas_ta`
- **`out/`** — Single-ticker outputs and intermediate deliverables (Excel & Markdown).
- **`out_master/`** — Master portfolio review strategy documents.
- **`out_secular/`** — Long-term secular analysis deliverables.

## Inputs & Configuration
- **`ticker-list-s.txt`**: The core input file for the `/short-term-portfolio-review` workflow. It must follow a structured CSV format so agents can parse it accurately:
  `Ticker, Name, Avg(CAD), Shares` *(e.g., `IBM.TO, International Business Machines Corporation, 40.9, 26`)*
