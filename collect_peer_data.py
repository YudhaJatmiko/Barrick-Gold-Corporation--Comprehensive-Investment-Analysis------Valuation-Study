import yfinance as yf
import pandas as pd
import json

# Gold mining peer companies
peers = {
    'ABX.TO': 'Barrick Gold Corporation',
    'NEM': 'Newmont Corporation', 
    'AEM': 'Agnico Eagle Mines Limited',
    'AEM.TO': 'Agnico Eagle Mines Limited (TSX)',
    'KGC': 'Kinross Gold Corporation',
    'K.TO': 'Kinross Gold Corporation (TSX)',
    'AU': 'AngloGold Ashanti Limited',
    'EGO': 'Eldorado Gold Corporation',
    'FNV': 'Franco-Nevada Corporation',
    'FNV.TO': 'Franco-Nevada Corporation (TSX)',
    'WPM': 'Wheaton Precious Metals Corp',
    'WPM.TO': 'Wheaton Precious Metals Corp (TSX)'
}

peer_data = {}
print("Collecting peer group data for gold mining companies...")

for symbol, company_name in peers.items():
    try:
        print(f"Collecting data for {symbol} - {company_name}")
        ticker = yf.Ticker(symbol)
        
        # Get company info
        info = ticker.info
        
        # Get price data (2 years)
        hist = ticker.history(period='2y')
        
        if hist.empty:
            print(f"  No price data for {symbol}")
            continue
            
        # Calculate key metrics
        current_price = hist['Close'].iloc[-1]
        year_high = hist['High'].max()
        year_low = hist['Low'].min()
        
        # Calculate returns
        returns_1m = (hist['Close'].iloc[-1] / hist['Close'].iloc[-22] - 1) * 100 if len(hist) > 22 else 0
        returns_3m = (hist['Close'].iloc[-1] / hist['Close'].iloc[-66] - 1) * 100 if len(hist) > 66 else 0
        returns_1y = (hist['Close'].iloc[-1] / hist['Close'].iloc[-252] - 1) * 100 if len(hist) > 252 else 0
        
        # Calculate volatility (annualized)
        daily_returns = hist['Close'].pct_change().dropna()
        volatility = daily_returns.std() * (252**0.5) * 100
        
        peer_data[symbol] = {
            'company_name': company_name,
            'current_price': round(current_price, 2),
            'market_cap': info.get('marketCap', 0),
            'enterprise_value': info.get('enterpriseValue', 0),
            'pe_ratio': info.get('forwardPE', info.get('trailingPE', 0)),
            'pb_ratio': info.get('priceToBook', 0),
            'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'roe': info.get('returnOnEquity', 0),
            'profit_margin': info.get('profitMargins', 0),
            'operating_margin': info.get('operatingMargins', 0),
            'revenue_growth': info.get('revenueGrowth', 0),
            'earnings_growth': info.get('earningsGrowth', 0),
            'year_high': round(year_high, 2),
            'year_low': round(year_low, 2),
            'returns_1m': round(returns_1m, 2),
            'returns_3m': round(returns_3m, 2),
            'returns_1y': round(returns_1y, 2),
            'volatility_annualized': round(volatility, 2),
            'avg_volume': info.get('averageVolume', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'beta': info.get('beta', 0),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'country': info.get('country', ''),
            'full_time_employees': info.get('fullTimeEmployees', 0)
        }
        
        print(f"  Successfully collected data - Market Cap: ${peer_data[symbol]['market_cap']:,}")
        
    except Exception as e:
        print(f"  Error collecting {symbol}: {e}")
        continue

# Save peer data
def json_serializer(obj):
    if pd.isna(obj):
        return None
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return str(obj)

with open('data/raw/peer_comparison_data.json', 'w') as f:
    json.dump(peer_data, f, indent=2, default=json_serializer)

print(f"\nPeer data collection completed! Collected data for {len(peer_data)} companies.")
print("Data saved to data/raw/peer_comparison_data.json")

# Quick summary
print("\n=== PEER GROUP SUMMARY ===")
for symbol, data in peer_data.items():
    print(f"{symbol}: {data['company_name']}")
    print(f"  Market Cap: ${data['market_cap']:,}")
    print(f"  P/E Ratio: {data['pe_ratio']}")
    print(f"  1Y Return: {data['returns_1y']}%")
    print()