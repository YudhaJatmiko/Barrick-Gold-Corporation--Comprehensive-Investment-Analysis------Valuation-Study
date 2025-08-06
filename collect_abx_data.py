import yfinance as yf
import pandas as pd
import json
import os

# Collect Barrick Gold data with correct symbol
ticker = yf.Ticker('ABX.TO')

print("Collecting Barrick Gold (ABX) data...")

# Historical prices
hist_5y = ticker.history(period='5y')
print(f"Price data range: {hist_5y.index[0]} to {hist_5y.index[-1]}")
print(f"Latest price: ${hist_5y['Close'].iloc[-1]:.2f}")

# Company info
info = ticker.info

# Financial statements
try:
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    cashflow = ticker.cashflow
    print("Financial statements collected successfully")
except Exception as e:
    print(f"Error collecting financials: {e}")

# Save data
hist_5y.to_csv('data/raw/abx_daily_prices.csv')

# Save company info with proper JSON handling
def json_serializer(obj):
    if pd.isna(obj):
        return None
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return str(obj)

with open('data/raw/abx_company_info.json', 'w') as f:
    json.dump(info, f, indent=2, default=json_serializer)

print("Data collection completed!")
print(f"Company: {info.get('longName', 'N/A')}")
print(f"Sector: {info.get('sector', 'N/A')}")
print(f"Industry: {info.get('industry', 'N/A')}")
print(f"Market Cap: ${info.get('marketCap', 0):,}")