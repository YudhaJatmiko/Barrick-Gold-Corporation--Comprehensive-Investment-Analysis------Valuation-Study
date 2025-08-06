import os
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
from api import AlphaVantageClient, PolygonClient, FMPClient, FREDClient, NewsClient

# Load environment variables
load_dotenv()

class BarrickDataCollector:
    """Main data collection orchestrator for Barrick Gold analysis"""
    
    def __init__(self):
        self.symbol = "GOLD"  # Barrick Gold Corporation
        self.company_name = "Barrick Gold Corporation"
        
        # Initialize API clients
        self.alpha_vantage = AlphaVantageClient(os.getenv('ALPHAVANTAGE_API_KEY'))
        self.polygon = PolygonClient(os.getenv('POLYGON_API_KEY'))
        self.fmp = FMPClient(os.getenv('FMP_API_KEY'))
        self.fred = FREDClient(os.getenv('FRED_API_KEY'))
        self.news = NewsClient(os.getenv('NEWS_API_KEY'))
        
        # Storage paths
        self.raw_data_path = "data/raw"
        self.processed_data_path = "data/processed"
        
    def collect_all_data(self):
        """Collect all data sources for comprehensive analysis"""
        print(f"Starting comprehensive data collection for {self.company_name} ({self.symbol})")
        
        # Company fundamentals
        self._collect_company_data()
        
        # Price and market data
        self._collect_market_data()
        
        # Financial statements and ratios
        self._collect_financial_data()
        
        # Economic indicators
        self._collect_economic_data()
        
        # News and sentiment
        self._collect_news_data()
        
        print("Data collection completed successfully!")
        
    def _collect_company_data(self):
        """Collect company overview and profile data"""
        print("Collecting company overview data...")
        
        # Alpha Vantage company overview
        av_overview = self.alpha_vantage.get_company_overview(self.symbol)
        self._save_json(av_overview, f"{self.raw_data_path}/av_company_overview.json")
        
        # FMP company profile
        fmp_profile = self.fmp.get_company_overview(self.symbol)
        self._save_json(fmp_profile, f"{self.raw_data_path}/fmp_company_profile.json")
        
        # Polygon company details
        polygon_details = self.polygon.get_company_overview(self.symbol)
        self._save_json(polygon_details, f"{self.raw_data_path}/polygon_company_details.json")
        
    def _collect_market_data(self):
        """Collect price and market data"""
        print("Collecting market and price data...")
        
        # Alpha Vantage daily prices (5 years)
        av_prices = self.alpha_vantage.get_price_data(self.symbol, "5year")
        av_prices.to_csv(f"{self.raw_data_path}/av_daily_prices.csv")
        
        # Polygon daily prices (5 years)
        polygon_prices = self.polygon.get_price_data(self.symbol, "5year")
        polygon_prices.to_csv(f"{self.raw_data_path}/polygon_daily_prices.csv")
        
        # FMP historical prices (5 years)
        fmp_prices = self.fmp.get_price_data(self.symbol, "5year")
        fmp_prices.to_csv(f"{self.raw_data_path}/fmp_daily_prices.csv")
        
    def _collect_financial_data(self):
        """Collect financial statements and key metrics"""
        print("Collecting financial statements and metrics...")
        
        # Alpha Vantage financial statements
        av_income = self.alpha_vantage.get_income_statement(self.symbol)
        self._save_json(av_income, f"{self.raw_data_path}/av_income_statement.json")
        
        av_balance = self.alpha_vantage.get_balance_sheet(self.symbol)
        self._save_json(av_balance, f"{self.raw_data_path}/av_balance_sheet.json")
        
        av_cashflow = self.alpha_vantage.get_cash_flow(self.symbol)
        self._save_json(av_cashflow, f"{self.raw_data_path}/av_cash_flow.json")
        
        av_earnings = self.alpha_vantage.get_earnings(self.symbol)
        self._save_json(av_earnings, f"{self.raw_data_path}/av_earnings.json")
        
        # FMP financial data
        fmp_income = self.fmp.get_financial_statements(self.symbol, "income-statement")
        self._save_json(fmp_income, f"{self.raw_data_path}/fmp_income_statement.json")
        
        fmp_balance = self.fmp.get_financial_statements(self.symbol, "balance-sheet-statement")
        self._save_json(fmp_balance, f"{self.raw_data_path}/fmp_balance_sheet.json")
        
        fmp_cashflow = self.fmp.get_financial_statements(self.symbol, "cash-flow-statement")
        self._save_json(fmp_cashflow, f"{self.raw_data_path}/fmp_cash_flow.json")
        
        # FMP ratios and metrics
        fmp_ratios = self.fmp.get_ratios(self.symbol)
        self._save_json(fmp_ratios, f"{self.raw_data_path}/fmp_ratios.json")
        
        fmp_metrics = self.fmp.get_key_metrics(self.symbol)
        self._save_json(fmp_metrics, f"{self.raw_data_path}/fmp_key_metrics.json")
        
        fmp_dcf = self.fmp.get_dcf(self.symbol)
        self._save_json(fmp_dcf, f"{self.raw_data_path}/fmp_dcf_valuation.json")
        
        fmp_enterprise = self.fmp.get_enterprise_values(self.symbol)
        self._save_json(fmp_enterprise, f"{self.raw_data_path}/fmp_enterprise_values.json")
        
    def _collect_economic_data(self):
        """Collect relevant economic indicators"""
        print("Collecting economic indicators...")
        
        # Gold prices
        gold_prices = self.fred.get_gold_price()
        gold_prices.to_csv(f"{self.raw_data_path}/fred_gold_prices.csv")
        
        # Economic indicators
        inflation = self.fred.get_inflation_rate()
        inflation.to_csv(f"{self.raw_data_path}/fred_inflation.csv")
        
        interest_rates = self.fred.get_interest_rates()
        interest_rates.to_csv(f"{self.raw_data_path}/fred_interest_rates.csv")
        
        gdp_growth = self.fred.get_gdp_growth()
        gdp_growth.to_csv(f"{self.raw_data_path}/fred_gdp_growth.csv")
        
        unemployment = self.fred.get_unemployment_rate()
        unemployment.to_csv(f"{self.raw_data_path}/fred_unemployment.csv")
        
        dollar_index = self.fred.get_dollar_index()
        dollar_index.to_csv(f"{self.raw_data_path}/fred_dollar_index.csv")
        
        mining_production = self.fred.get_mining_production_index()
        mining_production.to_csv(f"{self.raw_data_path}/fred_mining_production.csv")
        
    def _collect_news_data(self):
        """Collect news and sentiment data"""
        print("Collecting news and sentiment data...")
        
        # Company-specific news
        company_news = self.news.get_company_news(self.company_name, self.symbol, 30)
        self._save_json(company_news, f"{self.raw_data_path}/company_news.json")
        
        # Sector news
        sector_news = self.news.get_sector_news("mining", 14)
        self._save_json(sector_news, f"{self.raw_data_path}/sector_news.json")
        
        # Market news
        market_news = self.news.get_market_news(7)
        self._save_json(market_news, f"{self.raw_data_path}/market_news.json")
        
    def collect_peer_data(self):
        """Collect peer company data for benchmarking"""
        print("Collecting peer company data...")
        
        # Get peer list
        peers = self.fmp.get_peer_list(self.symbol)
        
        # Major gold mining peers if API doesn't return good results
        if not peers:
            peers = ['NEM', 'AEM', 'KGC', 'AU', 'EGO', 'GG', 'HMY']  # Major gold miners
            
        peer_data = {}
        
        for peer in peers[:10]:  # Limit to top 10 peers
            try:
                print(f"Collecting data for peer: {peer}")
                
                # Basic company info
                peer_profile = self.fmp.get_company_overview(peer)
                
                # Key metrics
                peer_ratios = self.fmp.get_ratios(peer)
                peer_metrics = self.fmp.get_key_metrics(peer)
                
                # Price data (1 year)
                peer_prices = self.fmp.get_price_data(peer, "1year")
                
                peer_data[peer] = {
                    'profile': peer_profile,
                    'ratios': peer_ratios,
                    'metrics': peer_metrics,
                    'prices': peer_prices.to_dict() if not peer_prices.empty else {}
                }
                
            except Exception as e:
                print(f"Error collecting data for {peer}: {e}")
                continue
                
        self._save_json(peer_data, f"{self.raw_data_path}/peer_analysis_data.json")
        
    def _save_json(self, data, filepath):
        """Save data as JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
    def get_data_summary(self):
        """Generate summary of collected data"""
        summary = {
            'collection_date': datetime.now().isoformat(),
            'symbol': self.symbol,
            'company_name': self.company_name,
            'data_sources': [
                'Alpha Vantage - Company overview, financials, prices',
                'FMP - Comprehensive financials, ratios, DCF',
                'Polygon - Market data, news',
                'FRED - Economic indicators, gold prices',
                'News API - Company and sector news'
            ]
        }
        
        self._save_json(summary, f"{self.processed_data_path}/data_collection_summary.json")
        return summary

if __name__ == "__main__":
    collector = BarrickDataCollector()
    collector.collect_all_data()
    collector.collect_peer_data()
    summary = collector.get_data_summary()
    print(f"Data collection completed: {summary}")