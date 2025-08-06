import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

class YFinanceCollector:
    """Backup data collector using Yahoo Finance"""
    
    def __init__(self, symbol="GOLD"):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        
    def collect_comprehensive_data(self):
        """Collect all available data from Yahoo Finance"""
        print(f"Collecting comprehensive data for {self.symbol} from Yahoo Finance...")
        
        # Basic info
        info = self.ticker.info
        self._save_json(info, "data/raw/yf_company_info.json")
        
        # Historical prices (5 years)
        hist_5y = self.ticker.history(period="5y", interval="1d")
        hist_5y.to_csv("data/raw/yf_daily_prices_5y.csv")
        
        # Historical prices (1 year, hourly for detailed analysis)
        hist_1y = self.ticker.history(period="1y", interval="1h")
        hist_1y.to_csv("data/raw/yf_hourly_prices_1y.csv")
        
        # Financial statements
        try:
            # Income Statement
            income_stmt = self.ticker.financials
            income_stmt.to_csv("data/raw/yf_income_statement.csv")
            
            # Balance Sheet
            balance_sheet = self.ticker.balance_sheet
            balance_sheet.to_csv("data/raw/yf_balance_sheet.csv")
            
            # Cash Flow
            cashflow = self.ticker.cashflow
            cashflow.to_csv("data/raw/yf_cashflow.csv")
            
            # Quarterly data
            quarterly_income = self.ticker.quarterly_financials
            quarterly_income.to_csv("data/raw/yf_quarterly_income.csv")
            
            quarterly_balance = self.ticker.quarterly_balance_sheet
            quarterly_balance.to_csv("data/raw/yf_quarterly_balance.csv")
            
            quarterly_cashflow = self.ticker.quarterly_cashflow
            quarterly_cashflow.to_csv("data/raw/yf_quarterly_cashflow.csv")
            
        except Exception as e:
            print(f"Error collecting financial statements: {e}")
            
        # Analyst recommendations
        try:
            recommendations = self.ticker.recommendations
            if recommendations is not None:
                recommendations.to_csv("data/raw/yf_recommendations.csv")
        except:
            pass
            
        # Earnings data
        try:
            earnings = self.ticker.earnings
            if earnings is not None:
                earnings.to_csv("data/raw/yf_earnings.csv")
                
            earnings_quarterly = self.ticker.quarterly_earnings
            if earnings_quarterly is not None:
                earnings_quarterly.to_csv("data/raw/yf_quarterly_earnings.csv")
        except:
            pass
            
        # Dividends and splits
        dividends = self.ticker.dividends
        if not dividends.empty:
            dividends.to_csv("data/raw/yf_dividends.csv")
            
        splits = self.ticker.splits
        if not splits.empty:
            splits.to_csv("data/raw/yf_splits.csv")
            
        # Major holders
        try:
            major_holders = self.ticker.major_holders
            if major_holders is not None:
                major_holders.to_csv("data/raw/yf_major_holders.csv")
                
            institutional_holders = self.ticker.institutional_holders
            if institutional_holders is not None:
                institutional_holders.to_csv("data/raw/yf_institutional_holders.csv")
        except:
            pass
            
        print("Yahoo Finance data collection completed!")
        
    def collect_peer_data(self, peers=None):
        """Collect peer comparison data"""
        if peers is None:
            peers = ['NEM', 'AEM', 'KGC', 'AU', 'EGO', 'GG', 'FNV']  # Major gold miners
            
        peer_data = {}
        
        for peer_symbol in peers:
            try:
                print(f"Collecting data for peer: {peer_symbol}")
                peer_ticker = yf.Ticker(peer_symbol)
                
                # Basic info
                peer_info = peer_ticker.info
                
                # Price data (1 year)
                peer_prices = peer_ticker.history(period="1y")
                
                # Key financial metrics from info
                peer_data[peer_symbol] = {
                    'info': peer_info,
                    'prices': peer_prices.to_dict(),
                    'market_cap': peer_info.get('marketCap', 0),
                    'pe_ratio': peer_info.get('forwardPE', 0),
                    'pb_ratio': peer_info.get('priceToBook', 0),
                    'profit_margin': peer_info.get('profitMargins', 0),
                    'revenue_growth': peer_info.get('revenueGrowth', 0),
                    'debt_to_equity': peer_info.get('debtToEquity', 0)
                }
                
            except Exception as e:
                print(f"Error collecting data for {peer_symbol}: {e}")
                continue
                
        self._save_json(peer_data, "data/raw/yf_peer_analysis.json")
        
    def _save_json(self, data, filepath):
        """Save data as JSON with proper handling"""
        import json
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        def json_serializer(obj):
            """JSON serializer for objects not serializable by default"""
            if pd.isna(obj):
                return None
            elif hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                return str(obj)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=json_serializer)

if __name__ == "__main__":
    collector = YFinanceCollector("GOLD")
    collector.collect_comprehensive_data()
    collector.collect_peer_data()