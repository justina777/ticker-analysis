---
description: Perform in-depth, multi-skill institutional financial analysis on a requested ticker
---

# Institutional Ticker Analysis Workflow

When the user asks you to analyze or check a specific ticker (e.g., `/ticker-analysis AAPL`), you must act as the **Lead Orchestrator** for an in-depth "Initiating Coverage" pipeline. 

This workflow serves as a **guide** for you (the AI). You must manually execute these phases sequentially, leveraging your specialized skills from `.agents/skills`. Because this process is heavy, you should output intermediate deliverables (Data packs, Excel models, Markdown reports) at each phase.

## Phase 1: Data Structuring & Pre-computation
**Goal:** Gather comprehensive fundamental, quantitative, and technical data.
1. **Skill Alignment:** Apply `.agents/skills/financial-analysis/technical-indicators/SKILL.md` (now upgraded to Quantitative Metrics).
2. **Action:** Run the `uv run python .agents/skills/financial-analysis/technical-indicators/scripts/compute_indicators.py [TICKER] --period 6mo` script to dynamically fetch the live Beta, Risk-Free Rate, WACC, Historical Revenue CAGR, and Technical Momentum indicators.
3. Use your `search_web` tool to extract the target company's latest consensus estimates and company profile. **CRITICAL:** Identify the company's Fiscal Year-End (e.g., December, June, etc.) to prevent calendar year hallucinations.
4. **Deliverable:** Write the extracted data to a structured `out/[ticker]_datapack.md` to maintain context. You MUST include the newly generated WACC and Growth Rates in this datapack.

## Phase 2: Core Financial Modeling
**Goal:** Build intrinsic valuation models without writing custom python scratch code.
1. Read the data pack generated in Phase 1.
2. **Skill Alignment:** Read and apply `.agents/skills/financial-analysis/dcf-model/SKILL.md`.
3. **Action:** Execute the centralized script `uv run python .agents/skills/financial-analysis/dcf-model/scripts/generate_dcf.py [TICKER]` to generate the baseline DCF model. **CRITICAL:** Pass the calculated Growth Rate and Margin from Phase 1 into the script using the `--growth` and `--margin` arguments.
4. **Deliverable:** The script will automatically output `out/[ticker]_DCF_Model.xlsx`. Read the script output (Implied Share Price) for synthesis.

## Phase 3: Peer Benchmarking & Landscape
**Goal:** Evaluate relative valuation against competitors without writing custom python scratch code.
1. Identify 3-4 direct competitors for the target ticker.
2. **Skill Alignment:** Apply `.agents/skills/financial-analysis/comps-analysis/SKILL.md`.
3. **Action:** Execute the centralized script `uv run python .agents/skills/financial-analysis/comps-analysis/scripts/generate_comps.py [TICKER] --peers [PEER1,PEER2...]` to generate the baseline Comps model.
4. **Deliverable:** The script will automatically output `out/[ticker]_Comps.xlsx`. Read the script output (Peer Avg EV/EBITDA, Implied Share Price) for synthesis.

## Phase 4: Technical Analysis & Momentum
**Goal:** Evaluate short-term price momentum and identify optimal entry/exit signals.
1. **Action:** Review the **8EMA / 21EMA crossover**, **50MA trend**, MACD, and RSI metrics generated in Phase 1.
2. **8EMA / 21EMA Crossover:** If 8EMA > 21EMA, short-term momentum is BULLISH. If 8EMA < 21EMA, momentum is BEARISH. EMAs are more responsive than simple MAs — treat crossovers as high-conviction signals.
3. **50MA as Dynamic Support/Resistance:** If the price is above the 50MA, the medium-term trend is intact. Use the 50MA price level as a concrete support target for pullback entry strategies in the Position Building section.
4. **Institutional Dip Finder:** Apply `.agents/skills/financial-analysis/institutional-dip-finder/SKILL.md`. Run the centralized script `uv run python .agents/skills/financial-analysis/institutional-dip-finder/scripts/find_dip.py [TICKER]` to algorithmically check for a "Proximity Zone" dip-buying setup.
5. **Deliverable:** Write a concise technical setup summary to `out/[ticker]_Technical_Setup.md` detailing the explicit Bullish/Bearish momentum signals, the 50MA level, realistic support/resistance levels, and whether the Institutional Dip Buy Signal was triggered.

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
5. Ensure the report includes a definitive Price Target, BUY/HOLD/SELL recommendation, and a dual-pronged **Actionable Strategy Section** that addresses two specific use cases:
    - **1) Non-Holders (Position Building):** Provide realistic entry points. If the `find_dip.py` script triggered a Buy Signal, aggressively recommend entering the stock now. If not, define the exact 50MA price level as the pullback target and wait for the 8EMA/21EMA crossover.
    - **2) Current Holders (Trimming/Exit OR Adding/Averaging Up):** If the position is overextended, define technical triggers for trimming. If the broader trend is bullish AND the `find_dip.py` script triggered a Buy Signal, strongly recommend an "Add on Dip" / Averaging Up strategy to increase allocation based on the Proximity Zone metrics.