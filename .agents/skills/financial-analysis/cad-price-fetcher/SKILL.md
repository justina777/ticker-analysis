---
name: cad-price-fetcher
description: Specialized skill to fetch exact CAD exchange prices for Canadian Depository Receipts (CDRs) or TSX-listed stocks using their native .TO or .NE suffixes, bypassing the need for percentage conversion math.
---

# Native CAD Price Fetcher

## Overview
Because Canadian Depository Receipts (CDRs) and TSX stocks trade natively in Canadian Dollars, doing math conversions based on US price targets can be imprecise. This skill fetches the exact End-of-Day close price directly from the exchange.

## Execution Instructions

To fetch the real CAD price of a ticker, run the following script:

```bash
uv run python .agents/skills/financial-analysis/cad-price-fetcher/scripts/fetch_cad_price.py [TICKER]
```

Example:
```bash
uv run python .agents/skills/financial-analysis/cad-price-fetcher/scripts/fetch_cad_price.py IBM.TO
```

## Validation Protocol (MANDATORY)
The script will output the **Company Name** returned directly from the exchange (e.g., `International Business Machines Corporation`). 

You **MUST** cross-reference this returned name against the name provided in the user's source list (e.g., `ticker-list-s.txt`). If the names do not reasonably match, you have encountered a ticker hallucination and must fail the extraction or prompt the user for clarification. Do not proceed with the returned data if the company name does not validate.
