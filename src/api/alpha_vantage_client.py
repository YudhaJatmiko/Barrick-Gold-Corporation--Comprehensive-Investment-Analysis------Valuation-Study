import pandas as pd
from typing import Dict, Any
from .base_client import BaseAPIClient

class AlphaVantageClient(BaseAPIClient):
    """Alpha Vantage API client for stock data and fundamentals"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://www.alphavantage.co/query", rate_limit=12.0)
        
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview and fundamental data"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        return self._make_request('', params)
        
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Get daily price data"""
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'outputsize': 'full'
        }
        
        data = self._make_request('', params)
        
        if 'Time Series (Daily)' not in data:
            return pd.DataFrame()
            
        time_series = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index')
        
        # Clean column names and convert to numeric
        df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend', 'split']
        df = df.apply(pd.to_numeric)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        return df
        
    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get annual income statement"""
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol
        }
        return self._make_request('', params)
        
    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get annual balance sheet"""
        params = {
            'function': 'BALANCE_SHEET', 
            'symbol': symbol
        }
        return self._make_request('', params)
        
    def get_cash_flow(self, symbol: str) -> Dict[str, Any]:
        """Get annual cash flow statement"""
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol
        }
        return self._make_request('', params)
        
    def get_earnings(self, symbol: str) -> Dict[str, Any]:
        """Get earnings data"""
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }
        return self._make_request('', params)