import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
from .base_client import BaseAPIClient

class PolygonClient(BaseAPIClient):
    """Polygon.io API client for market data"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://api.polygon.io", rate_limit=0.2)
        
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company details from Polygon"""
        endpoint = f"v3/reference/tickers/{symbol}"
        return self._make_request(endpoint)
        
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Get aggregated price data"""
        end_date = datetime.now()
        
        if period == "1year":
            start_date = end_date - timedelta(days=365)
        elif period == "5year":
            start_date = end_date - timedelta(days=1825)
        else:
            start_date = end_date - timedelta(days=365)
            
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        endpoint = f"v2/aggs/ticker/{symbol}/range/1/day/{start_str}/{end_str}"
        params = {
            'adjusted': 'true',
            'sort': 'asc',
            'limit': 5000
        }
        
        data = self._make_request(endpoint, params)
        
        if 'results' not in data:
            return pd.DataFrame()
            
        results = data['results']
        df = pd.DataFrame(results)
        
        if df.empty:
            return df
            
        # Convert timestamp and rename columns
        df['date'] = pd.to_datetime(df['t'], unit='ms')
        df = df.rename(columns={
            'o': 'open',
            'h': 'high', 
            'l': 'low',
            'c': 'close',
            'v': 'volume',
            'vw': 'vwap',
            'n': 'transactions'
        })
        
        df.set_index('date', inplace=True)
        return df[['open', 'high', 'low', 'close', 'volume', 'vwap', 'transactions']]
        
    def get_financials(self, symbol: str) -> Dict[str, Any]:
        """Get company financials"""
        endpoint = f"vX/reference/financials"
        params = {
            'ticker': symbol,
            'limit': 10
        }
        return self._make_request(endpoint, params)
        
    def get_news(self, symbol: str, limit: int = 50) -> Dict[str, Any]:
        """Get recent news for the company"""
        endpoint = "v2/reference/news"
        params = {
            'ticker': symbol,
            'limit': limit,
            'sort': 'published_utc',
            'order': 'desc'
        }
        return self._make_request(endpoint, params)