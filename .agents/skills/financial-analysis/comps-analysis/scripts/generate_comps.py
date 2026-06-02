import argparse
import pandas as pd
import yfinance as yf
import os

def generate_comps(ticker, peers):
    print(f"Generating Comparable Company Analysis for {ticker}...")
    
    os.makedirs('out', exist_ok=True)
    all_tickers = [ticker] + peers
    
    data_list = []
    
    for t in all_tickers:
        print(f"Fetching data for {t}...")
        try:
            stock = yf.Ticker(t)
            info = stock.info
            
            price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            market_cap = info.get('marketCap', 0) / 1e9
            
            total_debt = info.get('totalDebt', 0) / 1e9
            total_cash = info.get('totalCash', 0) / 1e9
            net_debt = total_debt - total_cash
            ev = market_cap + net_debt
            
            revenue = info.get('totalRevenue', 0) / 1e9
            ebitda = info.get('ebitda', 0) / 1e9
            
            pe = info.get('trailingPE', info.get('forwardPE', 0))
            
            ev_rev = ev / revenue if revenue > 0 else 0
            ev_ebitda = ev / ebitda if ebitda > 0 else 0
            
            data_list.append({
                'Ticker': t,
                'Share Price': price,
                'Market Cap ($B)': market_cap,
                'Net Debt ($B)': net_debt,
                'Enterprise Value ($B)': ev,
                'LTM Revenue ($B)': revenue,
                'LTM EBITDA ($B)': ebitda,
                'EV / Revenue': ev_rev,
                'EV / EBITDA': ev_ebitda,
                'P/E Ratio': pe
            })
            
        except Exception as e:
            print(f"Error fetching data for {t}: {e}")
            data_list.append({
                'Ticker': t, 'Share Price': 0, 'Market Cap ($B)': 0, 'Net Debt ($B)': 0,
                'Enterprise Value ($B)': 0, 'LTM Revenue ($B)': 0, 'LTM EBITDA ($B)': 0,
                'EV / Revenue': 0, 'EV / EBITDA': 0, 'P/E Ratio': 0
            })
            
    df = pd.DataFrame(data_list)
    
    # Calculate Averages (excluding the target ticker for the peer average)
    peer_df = df[df['Ticker'] != ticker]
    avg_ev_rev = peer_df['EV / Revenue'].mean() if not peer_df.empty else 0
    avg_ev_ebitda = peer_df['EV / EBITDA'].mean() if not peer_df.empty else 0
    avg_pe = peer_df['P/E Ratio'].mean() if not peer_df.empty else 0
    
    # Calculate Implied Value based on Peer Average EV/EBITDA
    target_ebitda = df[df['Ticker'] == ticker]['LTM EBITDA ($B)'].iloc[0]
    target_net_debt = df[df['Ticker'] == ticker]['Net Debt ($B)'].iloc[0]
    
    try:
        target_shares = yf.Ticker(ticker).info.get('sharesOutstanding', 1e9) / 1e9
    except:
        target_shares = 1.0
        
    implied_ev = target_ebitda * avg_ev_ebitda
    implied_equity = implied_ev - target_net_debt
    implied_share_price = implied_equity / target_shares if target_shares > 0 else 0
    
    filename = f"out/{ticker}_Comps.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Comps', index=False)
        
        # Write Summary
        summary_data = {
            'Metric': ['Peer Avg EV/Rev', 'Peer Avg EV/EBITDA', 'Peer Avg P/E', 'Target Implied EV', 'Target Implied Equity', 'Target Implied Price'],
            'Value': [avg_ev_rev, avg_ev_ebitda, avg_pe, implied_ev, implied_equity, implied_share_price]
        }
        df_sum = pd.DataFrame(summary_data)
        df_sum.to_excel(writer, sheet_name='Valuation Summary', index=False)
        
        # Formatting
        workbook = writer.book
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        mult_format = workbook.add_format({'num_format': '0.0x'})
        
        ws1 = writer.sheets['Comps']
        ws1.set_column('A:A', 10)
        ws1.set_column('B:G', 15, money_format)
        ws1.set_column('H:J', 15, mult_format)
        
        ws2 = writer.sheets['Valuation Summary']
        ws2.set_column('A:A', 25)
        ws2.set_column('B:B', 15)

    print(f"\n=============================================")
    print(f"COMPS GENERATED FOR {ticker}")
    print(f"=============================================")
    print(f"Peer Avg EV/EBITDA  : {avg_ev_ebitda:.1f}x")
    print(f"Implied Share Price : ${implied_share_price:.2f}")
    print(f"File Saved To       : {filename}")
    print(f"=============================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an Excel Comps Analysis.')
    parser.add_argument('ticker', type=str, help='The target stock ticker symbol')
    parser.add_argument('--peers', type=str, required=True, help='Comma separated list of peer tickers (e.g. AMD,INTC,NVDA)')
    
    args = parser.parse_args()
    peer_list = [p.strip() for p in args.peers.split(',')]
    generate_comps(args.ticker, peer_list)
