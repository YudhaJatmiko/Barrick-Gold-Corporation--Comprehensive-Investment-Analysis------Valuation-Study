import requests
import time
from typing import Dict, Any, Optional
import pandas as pd
from abc import ABC, abstractmethod

class BaseAPIClient(ABC):
    """Base class for all financial API clients"""
    
    def __init__(self, api_key: str, base_url: str, rate_limit: float = 1.0):
        self.api_key = api_key
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.last_request_time = 0
        
    def _rate_limit_check(self):
        """Enforce rate limiting between API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        self.last_request_time = time.time()
        
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting"""
        self._rate_limit_check()
        
        url = f"{self.base_url}/{endpoint}"
        if params is None:
            params = {}
            
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}
            
    @abstractmethod
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company fundamental data"""
        pass
        
    @abstractmethod
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Get historical price data"""
        pass