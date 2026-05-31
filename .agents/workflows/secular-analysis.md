---
description: Perform in-depth, institutional-grade secular trend analysis on a requested ticker. Use this workflow when the user wants to evaluate a stock for a long-term hold (at least 1 year), not for a short-term trade.
---

# Institutional Secular Analysis Workflow

When the user asks you to analyze a ticker for a long-term hold (e.g., `/secular-analysis AAPL`), you must act as the **Lead Portfolio Manager** for a "Core Book" initiation.

This workflow serves as a **guide** for you (the AI). You must manually execute these phases sequentially. Because secular analysis involves evaluating vast amounts of fundamental and macro data over a multi-year horizon, **you must output intermediate deliverables** at key phases to maintain your context window.

## Phase 1: Sector Tailwind & Thematic Check
- **Goal:** Determine if the secular tailwind driving the ticker is expanding.
- **Skill Alignment:** Leverage `.agents/skills/equity-research/sector-overview/SKILL.md`.
- **Action:** 
  1. Search the web for downstream demand and upstream supply for this sector.
  2. Map the **Value Chain**. Is the ticker a primary driver (e.g., NVDA) or a second/third-derivative beneficiary?
  3. **Deliverable:** Write the extracted thematic data to a structured `out_secular/[ticker]_Secular_Datapack.md`.

## Phase 2: The Gatekeeper (Competitive Moat & Capital Intensity)
- **Goal:** Abort the workflow if the ticker is structurally flawed.
- **Skill Alignment:** Apply `.agents/skills/financial-analysis/competitive-analysis/SKILL.md`.
- **Action:** Evaluate the company's competitive moat, market share trajectory, and capital intensity. 
- **CRITICAL FAIL-SAFE:** If the company is losing market share, has horrific capital intensity with low ROI, or faces imminent terminal disruption, **ABORT THE HOLD STRATEGY.** You must immediately generate `out_secular/[ticker]_Secular_Playbook.md` with a **"SECULAR AVOID / SHORT"** rating, explaining the structural flaws, and terminate the workflow. Do not proceed to Phase 3.

## Phase 3: Falsifiable Thesis & DCF Valuation
- **Goal:** Build an institutional thesis and ensure margin of safety.
- **Action:** 
  1. Define a 1-2 sentence core thesis and explicitly list **Kill Criteria** (events that would force an exit, such as moat destruction or severe valuation bubbles).
  2. Apply `.agents/skills/financial-analysis/dcf-model/SKILL.md` (or write a quick python DCF) focusing heavily on the **Terminal Growth Rate**. Secular winners are best when they don't require massive ongoing capital to grow.
  3. **Deliverable:** Append the Thesis, Kill Criteria, and DCF output to your `out_secular/[ticker]_Secular_Datapack.md`.

## Phase 4: Technical Macro Support (200-Day MA)
- **Goal:** Identify the structural floor of the asset.
- **Action:** Run the `uv run python .agents/skills/financial-analysis/technical-indicators/scripts/compute_indicators.py [TICKER] --period 2y` script.
- **Rules:** 
  - Focus strictly on the **200MA** and the **52-Week High/Low**.
  - Ignore the 8EMA/21EMA noise for the "Core Book".
  - The Golden Rule: *Never sell a core position on a drawdown as long as it holds the 200MA and the Fundamental Kill Criteria are not met.*

## Phase 5: The "Secular Strategy Playbook" & Concrete Prediction
- **Goal:** Synthesize all findings into the final, actionable institutional report.
- **Action:** Generate and save `out_secular/[ticker]_Secular_Playbook.md`.
- **Formatting Rules:**
  - **Title:** Secular Strategy Playbook: [Company Name] ([Ticker])
  - **Sections:**
    1.  **Value Chain Position:** Where does it sit in the secular trend?
    2.  **The Falsifiable Thesis & Kill Criteria:** Outline the thesis and exactly what would trigger a full exit.
    3.  **Valuation & Capital Intensity:** DCF implied price and moat assessment.
    4.  **Portfolio Strategy (Core vs. Tactical):**
        -   *Core Book (60-80%):* Hold until Kill Criteria met or 200MA breaks on macro panic.
        -   *Tactical Book (20-40%):* Explicit instructions on when to trim (e.g., RSI > 75, 50% above 200MA) and when to add (tests of the 50MA).
  - **CRITICAL MANDATE - CONCRETE ACTIONABLE PREDICTION:** The report **MUST** conclude with a highly specific, actionable prediction and timeline. You must state explicit holding durations (e.g., "This ticker is a high-conviction hold for the next 2.5 years") and time-bound price targets based on the secular drivers (e.g., "We project the stock will reach $1500+ by mid-2027 as HBM supply constraints persist"). Avoid vague "long-term" generalities.