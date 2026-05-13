import sys
import yfinance as yf
import pandas as pd
import pandas_ta as ta

def compute_metrics(ticker):
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    
    # 1. FETCH FUNDAMENTAL METRICS
    info = stock.info
    beta = info.get('beta', 1.0)
    
    # Fetch 10-Year Treasury Yield for Risk-Free Rate
    tnx = yf.Ticker('^TNX')
    tnx_hist = tnx.history(period="5d")
    if not tnx_hist.empty:
        risk_free_rate = tnx_hist['Close'].iloc[-1] / 100.0
    else:
        risk_free_rate = 0.045 # fallback 4.5%
        
    equity_risk_premium = 0.055 # standard market assumption
    cost_of_equity = risk_free_rate + (beta * equity_risk_premium)
    
    # Estimate WACC (assuming 85% equity / 15% debt standard structure, 5.5% cost of debt, 15% tax)
    # For a more robust script, this could pull exact debt/equity, but this is a solid proxy.
    cost_of_debt = 0.055
    tax_rate = 0.15
    equity_weight = 0.85
    debt_weight = 0.15
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
    
    # Historical Revenue Growth
    financials = stock.financials
    growth_rate_3y = 0.10 # fallback
    if not financials.empty and 'Total Revenue' in financials.index:
        revs = financials.loc['Total Revenue'].dropna()
        if len(revs) >= 4:
            # CAGR formula: (Ending Value / Beginning Value) ** (1 / n) - 1
            # Note: financials columns are usually ordered newest to oldest
            end_val = revs.iloc[0]
            start_val = revs.iloc[3]
            if start_val > 0:
                growth_rate_3y = (end_val / start_val) ** (1/3) - 1
                
    # 2. FETCH TECHNICAL METRICS
    df = stock.history(period="6mo")
    
    if df.empty:
        print(f"Error: Could not retrieve price data for {ticker}.")
        sys.exit(1)
        
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df['5MA'] = ta.sma(df['Close'], length=5)
    df['10MA'] = ta.sma(df['Close'], length=10)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    if macd is not None and not macd.empty:
        macd_col = macd.columns[0]
        signal_col = macd.columns[2]
        df['MACD'] = macd[macd_col]
        df['MACD_Signal'] = macd[signal_col]
    else:
        df['MACD'] = 0
        df['MACD_Signal'] = 0
        
    latest = df.iloc[-1]
    
    print("\n" + "="*45)
    print(f"QUANTITATIVE METRICS FOR {ticker}")
    print("="*45)
    print("--- FUNDAMENTAL VALUATION INPUTS ---")
    print(f"Beta               : {beta:.2f}")
    print(f"Risk-Free Rate     : {risk_free_rate*100:.2f}%")
    print(f"Cost of Equity     : {cost_of_equity*100:.2f}%")
    print(f"Estimated WACC     : {wacc*100:.2f}%")
    print(f"3-Yr Revenue CAGR  : {growth_rate_3y*100:.2f}%")
    
    print("\n--- TECHNICAL MOMENTUM INDICATORS ---")
    print(f"Latest Close Price : ${float(latest['Close']):.2f}")
    print(f"5-Day MA           : ${float(latest['5MA']):.2f}")
    print(f"10-Day MA          : ${float(latest['10MA']):.2f}")
    print(f"14-Day RSI         : {float(latest['RSI']):.2f}")
    print(f"MACD Line          : {float(latest['MACD']):.4f}")
    print(f"MACD Signal Line   : {float(latest['MACD_Signal']):.4f}")
    
    ma_status = "BULLISH (5MA > 10MA)" if latest['5MA'] > latest['10MA'] else "BEARISH (5MA < 10MA)"
    rsi_status = "OVERBOUGHT" if latest['RSI'] > 70 else ("OVERSOLD" if latest['RSI'] < 30 else "NEUTRAL")
    macd_status = "BULLISH (MACD > Signal)" if latest['MACD'] > latest['MACD_Signal'] else "BEARISH (MACD < Signal)"
    
    print("\n--- MOMENTUM SUMMARY ---")
    print(f"MA Trend  : {ma_status}")
    print(f"RSI State : {rsi_status}")
    print(f"MACD Trend: {macd_status}")
    print("=============================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_indicators.py [TICKER]")
        sys.exit(1)
        
    ticker = sys.argv[1]
    compute_metrics(ticker)
