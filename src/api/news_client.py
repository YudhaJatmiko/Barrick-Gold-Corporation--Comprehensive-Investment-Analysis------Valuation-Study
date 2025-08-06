import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_client import BaseAPIClient

class NewsClient(BaseAPIClient):
    """News API client for market sentiment analysis"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://newsapi.org/v2", rate_limit=0.1)
        
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Not applicable for News API"""
        return {}
        
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Not applicable for News API"""
        return pd.DataFrame()
        
    def get_company_news(self, company_name: str, symbol: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get news articles about the company"""
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        endpoint = "everything"
        params = {
            'q': f'"{company_name}" OR "{symbol}"',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 100
        }
        
        data = self._make_request(endpoint, params)
        return data.get('articles', [])
        
    def get_sector_news(self, sector: str = "mining", days_back: int = 7) -> List[Dict[str, Any]]:
        """Get news about the sector"""
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        endpoint = "everything"
        params = {
            'q': f'{sector} OR "precious metals" OR gold',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 50
        }
        
        data = self._make_request(endpoint, params)
        return data.get('articles', [])
        
    def get_market_news(self, days_back: int = 3) -> List[Dict[str, Any]]:
        """Get general market news"""
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        endpoint = "everything"
        params = {
            'q': 'stock market OR economy OR Federal Reserve',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 30
        }
        
        data = self._make_request(endpoint, params)
        return data.get('articles', [])