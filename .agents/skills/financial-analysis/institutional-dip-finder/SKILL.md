---
name: institutional-dip-finder
description: Algorithmic checker to identify institutional 'Add on Dip' setups based on Relative Oversold RSI conditions and Moving Average Proximity Zones.
---

# Institutional Dip Finder

## Overview
Retail traders often blindly buy when the RSI drops below 30. Institutional algorithms, however, buy high-momentum stocks during "Relative Oversold" pullbacks (RSI cooling to 45-65) when the price enters a **Proximity Zone** (within 3%) of major dynamic support levels (10-EMA, 21-EMA, or 50-MA).

This skill executes a specialized script that evaluates the target ticker against these exact institutional confluence rules.

## Execution Instructions

To check if a stock is currently triggering an Institutional Dip Buy Signal, run the following command:

```bash
uv run python .agents/skills/financial-analysis/institutional-dip-finder/scripts/find_dip.py [TICKER]
```

Example:
```bash
uv run python .agents/skills/financial-analysis/institutional-dip-finder/scripts/find_dip.py AMD
```

## Workflow Integration Rules (MANDATORY)
1. **Reporting the Output:** You MUST execute this script during the Technical Analysis phase of the `/ticker-analysis` workflow.
2. **Signal Synthesis:** If the script outputs `[INSTITUTIONAL DIP BUY SIGNAL: TRIGGERED]`, you must prominently feature this in your final Synthesis Report. It changes the strategy for Current Holders from "Hold/Trim" to "Add on Dip", and it gives Non-Holders an immediate aggressive entry signal.
3. **Ignore Retail Rules:** Do NOT complain that the RSI is "not oversold enough" if the RSI is 55. If the script triggers a buy signal, trust the algorithm—the momentum is simply too strong to reach an RSI of 30.
