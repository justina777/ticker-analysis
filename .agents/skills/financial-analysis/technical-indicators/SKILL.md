---
name: quantitative-metrics
description: Use this skill to automatically calculate live fundamental valuation inputs (Beta, Risk-Free Rate, WACC, Historical Growth) AND technical momentum indicators (MA, RSI, MACD). Triggers on "technical analysis", "momentum", "WACC", "Growth Rates", or when executing Phase 1 and Phase 4 of the ticker-analysis workflow.
---

# Quantitative Metrics Skill

This skill calculates core mathematical metrics, blending fundamental valuation inputs (Cost of Capital, Historical CAGR) with technical momentum indicators to provide a complete quantitative profile for a ticker.

## Fundamental Metrics Computed
1. **Beta & Risk-Free Rate:** Live fetch from market indices and US Treasuries (10Y Yield).
2. **Estimated WACC (Cost of Capital):** Calculated using CAPM methodology with standard capital structure assumptions.
3. **Historical Revenue Growth:** 3-year historical CAGR based on SEC filings.

## Technical Momentum Indicators Computed
1. **Moving Averages (5MA & 10MA):** Short-term momentum tracking.
2. **Relative Strength Index (RSI):** A 14-day momentum oscillator.
3. **MACD (Moving Average Convergence Divergence):** Trend-following momentum indicator.

## Execution
To perform the quantitative analysis on a ticker, execute the bundled python script:

```bash
uv run python .agents/skills/financial-analysis/technical-indicators/scripts/compute_indicators.py [TICKER]
```

This script will output a mathematical summary containing both the Fundamental Valuation Inputs (to be used in your DCF modeling) and the Technical Momentum signals.

## Signal Rules (How to interpret the data)
After running the script and obtaining the indicator values, apply the following strict institutional rules to determine the short-term signal:

### Moving Average Rules (5MA vs 10MA)
- **BULLISH CROSS (BUY Signal):** If the 5MA crosses *above* the 10MA, near-term momentum is positive.
- **BEARISH CROSS (SELL Signal):** If the 5MA crosses *below* the 10MA, near-term momentum is negative. This is a classic short-term exit signal.

### RSI Rules (14-day)
- **OVERSOLD (BUY Signal):** If RSI is `< 30`. Indicates the asset may be undervalued or experiencing a reactionary sell-off.
- **OVERBOUGHT (SELL Signal):** If RSI is `> 70`. Indicates the asset may be overvalued and due for a pullback.
- **NEUTRAL:** RSI between `30` and `70`.

### MACD Rules
- **BULLISH:** MACD Line > Signal Line (Momentum accelerating upwards).
- **BEARISH:** MACD Line < Signal Line (Momentum accelerating downwards).

## Deliverable
Synthesize the outputs of the indicators and the applied rules into a concise Markdown section (e.g., `out/[ticker]_Technical_Setup.md`) documenting the current technical posture and the explicit momentum signal (Bullish, Bearish, or Neutral).
