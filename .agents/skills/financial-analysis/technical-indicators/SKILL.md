---
name: quantitative-metrics
description: Use this skill to automatically calculate live fundamental valuation inputs (Beta, Risk-Free Rate, WACC, Historical Growth) AND technical momentum indicators (EMA, RSI, MACD). Triggers on "technical analysis", "momentum", "WACC", "Growth Rates", or when executing Phase 1 and Phase 4 of the ticker-analysis workflow.
---

# Quantitative Metrics Skill

This skill calculates core mathematical metrics, blending fundamental valuation inputs (Cost of Capital, Historical CAGR) with technical momentum indicators to provide a complete quantitative profile for a ticker.

## Fundamental Metrics Computed
1. **Beta & Risk-Free Rate:** Live fetch from market indices and US Treasuries (10Y Yield).
2. **Estimated WACC (Cost of Capital):** Calculated using CAPM methodology with standard capital structure assumptions.
3. **Historical Revenue Growth:** 3-year historical CAGR based on SEC filings.

## Technical Momentum Indicators Computed
1. **Exponential Moving Averages (8EMA & 21EMA):** Fast-reacting short-term momentum crossover system. EMAs weight recent prices more heavily than simple MAs, providing earlier entry/exit signals.
2. **50-Day Moving Average (50MA):** Medium-term trend anchor. Price above the 50MA confirms an uptrend; price below confirms a downtrend. Serves as a key dynamic support/resistance level for position building.
3. **Relative Strength Index (RSI):** A 14-day momentum oscillator.
4. **MACD (Moving Average Convergence Divergence):** Trend-following momentum indicator.

## Execution
To perform the quantitative analysis on a ticker, execute the bundled python script:

```bash
uv run python .agents/skills/financial-analysis/technical-indicators/scripts/compute_indicators.py [TICKER] --period [PERIOD]
```

### The `--period` Argument
The script accepts an optional `--period` argument that strictly aligns with `yfinance` history periods (e.g., `6mo`, `1y`, `2y`, `5y`).
*   **Default (`--period 6mo`):** Perfect for short-to-medium term swing trading. Outputs the fast-reacting 8EMA, 21EMA, 50MA, RSI, and MACD.
*   **Long-Term (`--period 2y` or greater):** Perfect for secular holding. Automatically calculates the **200-Day Moving Average (200MA)** as the macro structural floor, and calculates the **52-Week High / 52-Week Low** for cycle context.

This script will output a mathematical summary containing both the Fundamental Valuation Inputs (to be used in your DCF modeling) and the Technical Momentum signals.

## Signal Rules (How to interpret the data)
After running the script and obtaining the indicator values, apply the following strict institutional rules to determine the short-term signal:

### EMA Crossover Rules (8EMA vs 21EMA)
- **BULLISH CROSS (BUY Signal):** If the 8EMA crosses *above* the 21EMA, near-term momentum is accelerating.
- **BEARISH CROSS (SELL Signal):** If the 8EMA crosses *below* the 21EMA, near-term momentum is fading. This is a classic short-term exit signal.
- EMAs react faster than simple MAs, so treat these crossovers as high-conviction short-term signals.

### 50MA Trend Rules
- **ABOVE 50MA (Uptrend):** Price trading above the 50MA confirms the medium-term trend is bullish. Use the 50MA as a dynamic support level for pullback entries.
- **BELOW 50MA (Downtrend):** Price trading below the 50MA confirms the medium-term trend is bearish. A break below the 50MA is a significant distribution signal.

### RSI Rules (14-day)
- **OVERSOLD (BUY Signal):** If RSI is `< 30`. Indicates the asset may be undervalued or experiencing a reactionary sell-off.
- **OVERBOUGHT (SELL Signal):** If RSI is `> 70`. Indicates the asset may be overvalued and due for a pullback.
- **NEUTRAL:** RSI between `30` and `70`.

### MACD Rules
- **BULLISH:** MACD Line > Signal Line (Momentum accelerating upwards).
- **BEARISH:** MACD Line < Signal Line (Momentum accelerating downwards).

## Deliverable
Synthesize the outputs of the indicators and the applied rules into a concise Markdown section (e.g., `out/[ticker]_Technical_Setup.md`) documenting the current technical posture and the explicit momentum signal (Bullish, Bearish, or Neutral).
