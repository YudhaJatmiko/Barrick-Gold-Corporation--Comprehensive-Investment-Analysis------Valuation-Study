import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
from .base_client import BaseAPIClient

class FREDClient(BaseAPIClient):
    """Federal Reserve Economic Data API client"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://api.stlouisfed.org/fred", rate_limit=0.1)
        
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Not applicable for FRED - returns empty dict"""
        return {}
        
    def get_price_data(self, symbol: str, period: str = "1year") -> pd.DataFrame:
        """Not applicable for FRED - returns empty DataFrame"""
        return pd.DataFrame()
        
    def get_economic_indicator(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get economic indicator data"""
        endpoint = "series/observations"
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1825)).strftime("%Y-%m-%d")  # 5 years
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            'series_id': series_id,
            'observation_start': start_date,
            'observation_end': end_date,
            'file_type': 'json',
            'frequency': 'm'  # monthly
        }
        
        data = self._make_request(endpoint, params)
        
        if 'observations' not in data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df.set_index('date', inplace=True)
        
        return df[['value']]
        
    def get_gold_price(self) -> pd.DataFrame:
        """Get gold prices (London PM fix)"""
        return self.get_economic_indicator('GOLDPMGBD228NLBM')
        
    def get_inflation_rate(self) -> pd.DataFrame:
        """Get CPI inflation rate"""
        return self.get_economic_indicator('CPIAUCSL')
        
    def get_interest_rates(self) -> pd.DataFrame:
        """Get 10-year Treasury rates"""
        return self.get_economic_indicator('GS10')
        
    def get_gdp_growth(self) -> pd.DataFrame:
        """Get GDP growth rate"""
        return self.get_economic_indicator('GDPC1')
        
    def get_unemployment_rate(self) -> pd.DataFrame:
        """Get unemployment rate"""
        return self.get_economic_indicator('UNRATE')
        
    def get_dollar_index(self) -> pd.DataFrame:
        """Get US Dollar Index"""
        return self.get_economic_indicator('DEXUSEU')  # USD/EUR
        
    def get_mining_production_index(self) -> pd.DataFrame:
        """Get mining production index"""
        return self.get_economic_indicator('IPG212S')