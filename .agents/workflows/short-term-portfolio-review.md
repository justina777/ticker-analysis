---
description: Automatically process a list of tickers, run the short-term ticker-analysis on each concurrently, and synthesize a final portfolio-level action report focusing on dip-buying and trim/exit strategies.
---

# Institutional Short-Term Portfolio Review Workflow

When the user invokes this workflow (e.g., `/short-term-portfolio-review`), you must act as the **Lead Portfolio Manager**, orchestrating multiple `/ticker-analysis` executions and consolidating the outputs into a master strategy document.

This workflow is highly tactical, focusing on a 1-to-3 month horizon.

## Phase 1: Parse Portfolio Holdings & Validation
- **Goal:** Prepare the input data, align tickers, and validate company names.
- **Action:** Read the `ticker-list-s.txt` file in the workspace root.
- **Rules & Logic:**
  - **Ticker Parsing:** The list contains Canadian exchange tickers with their full Company Names (e.g., `IBM.TO`, `International Business Machines Corporation`). You must strip the `.TO` (or `.NE`) suffix to identify the primary **US Ticker** (e.g., `IBM`, `NOW`).
  - **Why?** Technical analysis *must* be run on the highly liquid US ticker.
  - **Record Keeping:** Capture the user's Average Cost (`Avg(CAD)`) and Share count from the text file for context in Phase 3.
  - **Native CAD Fetching & Validation (CRITICAL):** Do NOT use math conversions. Apply `.agents/skills/financial-analysis/cad-price-fetcher/SKILL.md`. Run the script `uv run python .agents/skills/financial-analysis/cad-price-fetcher/scripts/fetch_cad_price.py [CANADIAN_TICKER]` (e.g., `IBM.TO`). 
  - You MUST cross-check the "Company Name" outputted by the script against the name in the user's text file. If they match, record the exact CAD price. If they don't, abort and alert the user.

## Phase 2: Parallel Batch Execution
- **Goal:** Generate the underlying initiation reports rapidly.
- **Action:** For each parsed base US ticker, you must execute the `/ticker-analysis` workflow.
- **Agentic Execution Rule:** To save time, do **NOT** run these sequentially yourself. You **MUST** use the `invoke_subagent` tool to spawn a parallel researcher agent for each ticker. Give each sub-agent the specific prompt: "Run the `/ticker-analysis` workflow on [TICKER]".
- Wait until all sub-agents have completed their tasks and generated their respective `out/[ticker]_Initiation_Report.md` files.

## Phase 3: Short-Term Strategy Synthesis & Historical Comparison
- **Goal:** Consolidate the findings into an actionable portfolio mandate.
- **Action:** Read the generated `out/[ticker]_Initiation_Report.md` files.
- **Historical Delta Check:** 
  - Check the `out_master/` directory for the most recent previous `Short_Term_Portfolio_Review.md` file.
  - **The Staleness Limit:** If the previous report is older than 14 days, flag it as **"Stale"**. Do not run the delta comparison, as short-term momentum (like 8EMA/21EMA) resets frequently. Treat the current review as a baseline.
  - If the previous report is within 14 days, compare the old 50MA/RSI targets to the current ones to identify strengthening or breaking trends.
- **Deliverable:** Generate the master portfolio document at: `out_master/[YYYY-MM-DD]/Short_Term_Portfolio_Review.md`.
- **Formatting Rules for the Deliverable:**
  - **The "Add at Dip" Matrix:** A table listing each ticker, its current US Price, the **Native CAD Price** fetched in Phase 1, and its exact 50MA support level.
  - **The "Trim/Exit" Matrix:** A table listing each ticker, its current RSI, the 8EMA/21EMA status, and the explicit US and CAD price targets to take profits or cut losses.
  - **Portfolio Action & Position Sizing (CRITICAL):** Calculate the absolute dollar value of the position (`Shares * Current CAD Price`). If the user holds a very small allocation (e.g., < $2000 CAD) of a highly bullish stock, you MUST recommend an **"Add on Dip"** strategy to build out the core position, using the CAD 50MA as the exact dip entry target. Do not blindly suggest "Trim" just because they have a high percentage gain if the absolute position is tiny.
