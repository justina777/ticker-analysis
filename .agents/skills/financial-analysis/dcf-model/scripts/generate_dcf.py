import argparse
import pandas as pd
import yfinance as yf
import os
import sys

def generate_dcf(ticker, revenue_growth, ebit_margin, terminal_growth):
    print(f"Fetching financial data for {ticker}...")
    stock = yf.Ticker(ticker)
    
    # Create the out directory if it doesn't exist
    os.makedirs('out', exist_ok=True)
    
    try:
        info = stock.info
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        
        # Get baseline metrics
        if not income_stmt.empty and 'Total Revenue' in income_stmt.index:
            current_revenue = income_stmt.loc['Total Revenue'].iloc[0] / 1e9 # in Billions
        else:
            current_revenue = info.get('totalRevenue', 10e9) / 1e9
            
        beta = info.get('beta', 1.0)
        shares_outstanding = info.get('sharesOutstanding', 1e9) / 1e9
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 100))
        
        total_debt = info.get('totalDebt', 0) / 1e9
        total_cash = info.get('totalCash', 0) / 1e9
        net_debt = total_debt - total_cash
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}. Using fallback defaults.")
        current_revenue = 10.0
        beta = 1.2
        shares_outstanding = 1.0
        current_price = 100.0
        net_debt = 1.0
        
    # Standard WACC Assumptions
    risk_free_rate = 0.045
    equity_risk_premium = 0.055
    cost_of_equity = risk_free_rate + (beta * equity_risk_premium)
    cost_of_debt = 0.055
    tax_rate = 0.15
    
    equity_weight = 0.85
    debt_weight = 0.15
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
    
    # Margins
    d_and_a_margin = 0.05
    capex_margin = 0.08
    nwc_margin = 0.02
    
    # 5-Year Projections
    years = ['FY1', 'FY2', 'FY3', 'FY4', 'FY5']
    revenues = []
    r = current_revenue
    
    for _ in range(5):
        r *= (1 + revenue_growth)
        revenues.append(r)
        
    ebit = [r * ebit_margin for r in revenues]
    nopat = [e * (1 - tax_rate) for e in ebit]
    d_and_a = [r * d_and_a_margin for r in revenues]
    capex = [r * capex_margin for r in revenues]
    nwc_change = [r * nwc_margin for r in revenues]
    
    fcf = [nopat[i] + d_and_a[i] - capex[i] - nwc_change[i] for i in range(5)]
    
    # Valuation
    discount_factors = [(1 + wacc) ** (i + 1) for i in range(5)]
    pv_fcf = [fcf[i] / discount_factors[i] for i in range(5)]
    
    terminal_value = (fcf[-1] * (1 + terminal_growth)) / (wacc - terminal_growth) if wacc > terminal_growth else 0
    pv_terminal_value = terminal_value / discount_factors[-1] if discount_factors[-1] > 0 else 0
    
    enterprise_value = sum(pv_fcf) + pv_terminal_value
    equity_value = enterprise_value - net_debt
    
    if shares_outstanding > 0:
        implied_share_price = equity_value / shares_outstanding
    else:
        implied_share_price = 0
        
    # Output to Excel
    data = {
        'Metric': ['Revenue ($B)', 'EBIT ($B)', 'NOPAT ($B)', 'D&A ($B)', 'CapEx ($B)', 'Change in NWC ($B)', 'Unlevered FCF ($B)', 'PV of FCF ($B)'],
        'FY1': [revenues[0], ebit[0], nopat[0], d_and_a[0], capex[0], nwc_change[0], fcf[0], pv_fcf[0]],
        'FY2': [revenues[1], ebit[1], nopat[1], d_and_a[1], capex[1], nwc_change[1], fcf[1], pv_fcf[1]],
        'FY3': [revenues[2], ebit[2], nopat[2], d_and_a[2], capex[2], nwc_change[2], fcf[2], pv_fcf[2]],
        'FY4': [revenues[3], ebit[3], nopat[3], d_and_a[3], capex[3], nwc_change[3], fcf[3], pv_fcf[3]],
        'FY5': [revenues[4], ebit[4], nopat[4], d_and_a[4], capex[4], nwc_change[4], fcf[4], pv_fcf[4]]
    }
    df_dcf = pd.DataFrame(data)
    
    val_data = {
        'Metric': ['Beta', 'WACC', 'Terminal Growth Rate', 'Terminal Value ($B)', 'PV of Terminal Value ($B)', 'Sum of PV FCF ($B)', 'Enterprise Value ($B)', 'Less: Net Debt ($B)', 'Implied Equity Value ($B)', 'Shares Outstanding (B)', 'Implied Share Price', 'Current Market Price'],
        'Value': [beta, wacc, terminal_growth, terminal_value, pv_terminal_value, sum(pv_fcf), enterprise_value, net_debt, equity_value, shares_outstanding, implied_share_price, current_price]
    }
    df_val = pd.DataFrame(val_data)
    
    filename = f"out/{ticker}_DCF_Model.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df_dcf.to_excel(writer, sheet_name='DCF Projections', index=False)
        df_val.to_excel(writer, sheet_name='Valuation Output', index=False)
        
        workbook = writer.book
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        pct_format = workbook.add_format({'num_format': '0.00%'})
        
        ws1 = writer.sheets['DCF Projections']
        ws1.set_column('A:A', 25)
        ws1.set_column('B:F', 15, money_format)
        
        ws2 = writer.sheets['Valuation Output']
        ws2.set_column('A:A', 30)
        ws2.set_column('B:B', 20)
        
    print(f"\n=============================================")
    print(f"DCF MODEL GENERATED FOR {ticker}")
    print(f"=============================================")
    print(f"Implied Share Price : ${implied_share_price:.2f}")
    print(f"Current Market Price: ${current_price:.2f}")
    if current_price > 0:
        upside = (implied_share_price / current_price) - 1
        print(f"Implied Upside      : {upside*100:.2f}%")
    print(f"File Saved To       : {filename}")
    print(f"=============================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a baseline DCF Excel Model for a ticker.')
    parser.add_argument('ticker', type=str, help='The stock ticker symbol')
    parser.add_argument('--growth', type=float, default=0.15, help='Baseline 5-year revenue CAGR (e.g. 0.15 for 15%%)')
    parser.add_argument('--margin', type=float, default=0.25, help='Baseline EBIT margin (e.g. 0.25 for 25%%)')
    parser.add_argument('--terminal', type=float, default=0.03, help='Terminal growth rate (e.g. 0.03 for 3%%)')
    
    args = parser.parse_args()
    generate_dcf(args.ticker, args.growth, args.margin, args.terminal)
