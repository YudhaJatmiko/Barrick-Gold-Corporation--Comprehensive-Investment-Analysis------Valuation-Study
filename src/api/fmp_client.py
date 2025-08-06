import pandas as pd
from typing import Dict, Any, List
from .base_client import BaseAPIClient

class FMPClient(BaseAPIClient):
    """Financial Modeling Prep API client"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://financialmodelingprep.com/api", rate_limit=0.25)
        
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company profile"""
        endpoint = f"v3/profile/{symbol}"
        data = self._make_request(endpoint)
        return data[0] if data else {}
        
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Get historical price data"""
        endpoint = f"v3/historical-price-full/{symbol}"
        params = {
            'timeseries': 252 if period == "1year" else 1260
        }
        
        data = self._make_request(endpoint, params)
        
        if 'historical' not in data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data['historical'])
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df = df.sort_index()
        
        return df[['open', 'high', 'low', 'close', 'adjClose', 'volume']]
        
    def get_financial_statements(self, symbol: str, statement_type: str = "income-statement") -> List[Dict[str, Any]]:
        """Get financial statements (income-statement, balance-sheet-statement, cash-flow-statement)"""
        endpoint = f"v3/{statement_type}/{symbol}"
        params = {'limit': 5}
        return self._make_request(endpoint, params)
        
    def get_ratios(self, symbol: str) -> List[Dict[str, Any]]:
        """Get financial ratios"""
        endpoint = f"v3/ratios/{symbol}"
        params = {'limit': 5}
        return self._make_request(endpoint, params)
        
    def get_key_metrics(self, symbol: str) -> List[Dict[str, Any]]:
        """Get key metrics"""
        endpoint = f"v3/key-metrics/{symbol}"
        params = {'limit': 5}
        return self._make_request(endpoint, params)
        
    def get_dcf(self, symbol: str) -> List[Dict[str, Any]]:
        """Get DCF valuation"""
        endpoint = f"v3/discounted-cash-flow/{symbol}"
        return self._make_request(endpoint)
        
    def get_peer_list(self, symbol: str) -> List[str]:
        """Get peer companies"""
        overview = self.get_company_overview(symbol)
        if not overview or 'industry' not in overview:
            return []
            
        sector = overview.get('sector', '')
        industry = overview.get('industry', '')
        
        # Get companies in same sector/industry
        endpoint = "v3/stock-screener"
        params = {
            'sector': sector,
            'industry': industry,
            'limit': 20
        }
        
        data = self._make_request(endpoint, params)
        return [company['symbol'] for company in data if company['symbol'] != symbol]
        
    def get_enterprise_values(self, symbol: str) -> List[Dict[str, Any]]:
        """Get enterprise value data"""
        endpoint = f"v3/enterprise-values/{symbol}"
        params = {'limit': 5}
        return self._make_request(endpoint, params)
        
    def get_market_cap(self, symbol: str) -> Dict[str, Any]:
        """Get current market cap"""
        endpoint = f"v3/market-capitalization/{symbol}"
        data = self._make_request(endpoint)
        return data[0] if data else {}