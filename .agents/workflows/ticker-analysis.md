---
description: Perform in-depth, multi-skill institutional financial analysis on a requested ticker
---

# Institutional Ticker Analysis Workflow

When the user asks you to analyze or check a specific ticker (e.g., `/ticker-analysis AAPL`), you must act as the **Lead Orchestrator** for an in-depth "Initiating Coverage" pipeline. 

This workflow serves as a **guide** for you (the AI). You must manually execute these phases sequentially, leveraging your specialized skills from `.agents/skills`. Because this process is heavy, you should output intermediate deliverables (Data packs, Excel models, Markdown reports) at each phase.

## Phase 1: Data Structuring & Pre-computation
**Goal:** Gather comprehensive fundamental, quantitative, and technical data.
1. **Skill Alignment:** Apply `.agents/skills/financial-analysis/technical-indicators/SKILL.md` (now upgraded to Quantitative Metrics).
2. **Action:** Run the `compute_indicators.py` script for the ticker to dynamically fetch the live Beta, Risk-Free Rate, WACC, Historical Revenue CAGR, and Technical Momentum indicators.
3. Use your `search_web` tool to extract the target company's latest consensus estimates and company profile. **CRITICAL:** Identify the company's Fiscal Year-End (e.g., December, June, etc.) to prevent calendar year hallucinations.
4. **Deliverable:** Write the extracted data to a structured `out/[ticker]_datapack.md` to maintain context. You MUST include the newly generated WACC and Growth Rates in this datapack.

## Phase 2: Core Financial Modeling
**Goal:** Build intrinsic valuation models.
1. Read the data pack generated in Phase 1.
2. **Skill Alignment:** Read and apply `.agents/skills/financial-analysis/dcf-model/SKILL.md`.
3. Build a 3-statement projection and a Discounted Cash Flow (DCF) model. **CRITICAL:** You must dynamically use the calculated WACC and Growth Rates outputted by the script in Phase 1. Do NOT use hardcoded assumptions.
4. **Deliverable:** You **MUST** export the mathematical model to an Excel file using the rules in `.agents/skills/earnings-reviewer/xlsx-author/SKILL.md` (e.g., `out/[ticker]_DCF_Model.xlsx`).

## Phase 3: Peer Benchmarking & Landscape
**Goal:** Evaluate relative valuation against competitors.
1. Identify 3-4 direct competitors for the target ticker.
2. **Skill Alignment:** Apply `.agents/skills/financial-analysis/comps-analysis/SKILL.md`.
3. Extract multiples (EV/EBITDA, EV/Revenue, P/E) for the peer group and calculate the Peer Median/Mean.
4. **Deliverable:** You **MUST** append this Comps analysis to the Excel file or output a separate `out/[ticker]_Comps.xlsx`.

## Phase 4: Technical Analysis & Momentum
**Goal:** Evaluate short-term price momentum and identify optimal entry/exit signals.
1. **Action:** Review the MACD, RSI, and MA crossover metrics generated in Phase 1.
2. **CRITICAL Technical Rule:** Do NOT blindly apply textbook 30/70 RSI rules. You must assess the *historical* RSI floor for high-momentum stocks. If a stock never drops below 40 RSI, then 40 is the dynamic "oversold" threshold.
3. **Deliverable:** Write a concise technical setup summary to `out/[ticker]_Technical_Setup.md` detailing the explicit Bullish/Bearish momentum signals and realistic support/resistance levels.

## Phase 5: Catalyst & Earnings Context
**Goal:** Assess management tone and near-term catalysts.
1. Search for the most recent earnings call transcript or press release. 
2. **CRITICAL Date Rule:** Whenever referencing an earnings quarter, you MUST specify the calendar end date (e.g., "Fiscal Q3 2026 (Ended March 31, 2026)") to prevent temporal hallucinations.
3. **Skill Alignment:** Apply `.agents/skills/earnings-reviewer/earnings-analysis/SKILL.md`.
4. Extract thesis-relevant changes, management guidance, and margin trajectory.

## Phase 6: Synthesis & Reporting (Initiating Coverage)
**Goal:** Produce the final institutional research report with actionable conclusions.
1. Synthesize the intrinsic value (DCF), relative value (Comps), catalyst context (Earnings), and Technical Momentum.
2. **CRITICAL Synthesis Rule:** Do not automatically issue a "SELL" rating just because a high Beta/WACC crushes the DCF value. If the DCF is low but the Comps and Momentum are incredibly strong, acknowledge that the market is pricing the stock on multiples, and provide a nuanced recommendation (e.g., HOLD).
3. **Skill Alignment:** Apply `.agents/skills/equity-research/initiating-coverage/SKILL.md` (Tasks 4 & 5).
4. **Deliverable:** You **MUST** author an institutional-quality 5-8 page markdown report. Save this report using the filesystem tool as `out/[ticker]_Initiation_Report.md`.
5. Ensure the report includes a definitive Price Target, BUY/HOLD/SELL recommendation, and an **Actionable Position Building Strategy** that provides realistic entry points (based on the dynamic RSI thresholds from Phase 4, not textbook 30 RSI).