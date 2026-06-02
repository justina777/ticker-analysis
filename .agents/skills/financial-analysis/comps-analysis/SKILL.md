---
name: comps-analysis
description: Comparable Company Analysis (Comps) model creation for equity valuation. Uses the centralized generate_comps.py script to output professional Excel models comparing EV/EBITDA, EV/Rev, and P/E multiples against industry peers.
---

# Comps Analysis Builder

## Overview

This skill creates institutional-quality Comparable Company Analysis (Comps) models for equity valuation.

## Tools

You MUST NOT write custom Python scripts or use `openpyxl` from scratch to build Comps models. That is highly inefficient and creates messy scratch files.

Instead, you MUST use the centralized Python script provided in this skill's directory:
`.agents/skills/financial-analysis/comps-analysis/scripts/generate_comps.py`

## Execution Instructions

To generate a Comps model, run the following command in the workspace root:

```bash
uv run python .agents/skills/financial-analysis/comps-analysis/scripts/generate_comps.py [TICKER] --peers [PEER1,PEER2,PEER3]
```

### Required Arguments:
- `ticker`: The target company ticker (e.g., `AMD`)
- `--peers`: A comma-separated list of peer tickers (e.g., `INTC,NVDA,QCOM`)

Example:
```bash
uv run python .agents/skills/financial-analysis/comps-analysis/scripts/generate_comps.py AMD --peers INTC,NVDA,QCOM
```

## Deliverables
The script will automatically generate the Comps Excel model and save it to `out/[TICKER]_Comps.xlsx`. 
Once the file is generated, you must read the command output (peer average EV/EBITDA, implied share price) and incorporate it into your final valuation report.
