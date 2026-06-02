---
name: dcf-model
description: Real DCF (Discounted Cash Flow) model creation for equity valuation. Uses the centralized generate_dcf.py script to output professional Excel models with executive summaries.
---

# DCF Model Builder

## Overview

This skill creates institutional-quality DCF models for equity valuation. 

## Tools

You MUST NOT write custom Python scripts or use `openpyxl` from scratch to build DCF models. That is highly inefficient and creates messy scratch files.

Instead, you MUST use the centralized Python script provided in this skill's directory:
`.agents/skills/financial-analysis/dcf-model/scripts/generate_dcf.py`

## Execution Instructions

To generate a DCF model, run the following command in the workspace root:

```bash
uv run python .agents/skills/financial-analysis/dcf-model/scripts/generate_dcf.py [TICKER]
```

### Optional Arguments:
- `--growth`: 5-year revenue CAGR (default: 0.15)
- `--margin`: EBIT margin (default: 0.25)
- `--terminal`: Terminal growth rate (default: 0.03)

Example:
```bash
uv run python .agents/skills/financial-analysis/dcf-model/scripts/generate_dcf.py MU --growth 0.20 --margin 0.35
```

## Deliverables
The script will automatically generate the DCF Excel model and save it to `out/[TICKER]_DCF_Model.xlsx`. 
Once the file is generated, you must read the command output (implied share price, etc.) and incorporate it into your final valuation report.