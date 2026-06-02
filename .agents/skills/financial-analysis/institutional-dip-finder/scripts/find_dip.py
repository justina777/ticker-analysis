import argparse
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import sys

def check_institutional_dip(ticker):
    print(f"Analyzing {ticker} for Institutional Dip Setups...")
    
    # Download 1 year of data to ensure MAs can be calculated properly
    try:
        df = yf.download(ticker, period="1y")
        if df.empty:
            print(f"Error: No data found for {ticker}")
            sys.exit(1)
            
        # Handle multi-index columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Calculate technical indicators
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=10, append=True)
        df.ta.ema(length=21, append=True)
        df.ta.sma(length=50, append=True)
        
        df = df.dropna()
        if len(df) < 50:
            print("Not enough data to calculate indicators.")
            sys.exit(1)
            
        latest = df.iloc[-1]
        current_price = latest['Close']
        current_rsi = latest['RSI_14']
        ema_10 = latest['EMA_10']
        ema_21 = latest['EMA_21']
        sma_50 = latest['SMA_50']
        
        # Look back 30 days to see if RSI was > 75 (Recent Overbought Peak)
        recent_30 = df.tail(30)
        had_recent_peak = (recent_30['RSI_14'] > 75).any()
        
        # 1. TREND CHECK: Is the secular trend bullish?
        # A simple check: Price is > 50MA, or 50MA is trending upward.
        # We will check if current price > 50MA * 0.95 (allowing deep pullbacks but not crashing through secular support)
        is_bullish_trend = current_price > (sma_50 * 0.95)
        
        # 2. RSI COOLDOWN CHECK: Is the RSI between 30 and 65? (Cooling off, but not necessarily textbook oversold)
        rsi_cooldown = 30 <= current_rsi <= 65
        
        # 3. PROXIMITY ZONE CHECK: Is the price within 3% of the 10-EMA, 21-EMA, or 50-MA?
        dist_10 = abs(current_price - ema_10) / current_price * 100
        dist_21 = abs(current_price - ema_21) / current_price * 100
        dist_50 = abs(current_price - sma_50) / current_price * 100
        
        in_proximity_zone = (dist_10 <= 3.0) or (dist_21 <= 3.0) or (dist_50 <= 3.0)
        
        # Final Signal Logic
        # We need a bullish structural trend, a cooling RSI, the stock to be in a proximity zone, 
        # and historically it should have had a recent momentum peak (though not strictly required if it's just grinding up).
        triggered = is_bullish_trend and rsi_cooldown and in_proximity_zone
        
        print("\n" + "="*50)
        print(f"INSTITUTIONAL DIP FINDER: {ticker}")
        print("="*50)
        print(f"Current Price    : ${current_price:.2f}")
        print(f"Current RSI(14)  : {current_rsi:.2f}")
        print(f"Recent RSI Peak? : {'Yes (RSI > 75 in last 30d)' if had_recent_peak else 'No'}")
        print("\n--- PROXIMITY ZONES ---")
        print(f"10-Day EMA       : ${ema_10:.2f} (Dist: {dist_10:.2f}%)")
        print(f"21-Day EMA       : ${ema_21:.2f} (Dist: {dist_21:.2f}%)")
        print(f"50-Day MA        : ${sma_50:.2f} (Dist: {dist_50:.2f}%)")
        
        print("\n--- ALGORITHMIC CHECKS ---")
        print(f"1. Bullish Secular Trend (Price > 0.95*50MA) : {'[PASS]' if is_bullish_trend else '[FAIL]'}")
        print(f"2. RSI Cooldown (30 <= RSI <= 65)            : {'[PASS]' if rsi_cooldown else '[FAIL]'}")
        print(f"3. Proximity Zone (Within 3% of MA/EMA)      : {'[PASS]' if in_proximity_zone else '[FAIL]'}")
        
        print("\n" + "="*50)
        if triggered:
            print(">>> [INSTITUTIONAL DIP BUY SIGNAL: TRIGGERED] <<<")
            print("Action: The stock has cooled off from momentum highs and entered a high-probability institutional buy zone near dynamic support.")
        else:
            print(">>> [INSTITUTIONAL DIP BUY SIGNAL: NOT TRIGGERED] <<<")
            print("Action: Conditions not met. The stock is either still too overbought, crashing through support, or in no man's land.")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify institutional dip buying setups based on RSI cooldown and Proximity Zones.')
    parser.add_argument('ticker', type=str, help='The stock ticker symbol')
    
    args = parser.parse_args()
    check_institutional_dip(args.ticker)
