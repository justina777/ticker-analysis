import argparse
import yfinance as yf
import sys

def fetch_cad_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Prefer current live price or regular market price for today's close
        price = info.get('currentPrice')
        if price is None:
            price = info.get('regularMarketPrice')
        if price is None:
            price = info.get('regularMarketPreviousClose', 0)
            
        company_name = info.get('longName', info.get('shortName', 'Unknown'))
        
        print(f"\n=============================================")
        print(f"CAD PRICE FETCHER: {ticker}")
        print(f"=============================================")
        print(f"Company Name : {company_name}")
        print(f"CAD Price    : ${price:.2f}")
        print(f"=============================================")
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch live CAD price and Company Name from TSX/NEO.')
    parser.add_argument('ticker', type=str, help='The Canadian ticker symbol (e.g., IBM.TO)')
    
    args = parser.parse_args()
    fetch_cad_price(args.ticker)
