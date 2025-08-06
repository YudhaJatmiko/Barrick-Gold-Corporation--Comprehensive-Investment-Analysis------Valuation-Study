import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class FinancialAnalysisEngine:
    """Professional-grade financial analysis and modeling engine"""
    
    def __init__(self, symbol: str = "ABX.TO", company_name: str = "Barrick Gold Corporation"):
        self.symbol = symbol
        self.company_name = company_name
        self.load_data()
        
    def load_data(self):
        """Load all collected financial data"""
        try:
            # Price data
            self.price_data = pd.read_csv('data/raw/abx_daily_prices.csv', index_col=0, parse_dates=True)
            
            # Company info
            with open('data/raw/abx_company_info.json', 'r') as f:
                self.company_info = json.load(f)
                
            # Peer data
            with open('data/raw/peer_comparison_data.json', 'r') as f:
                self.peer_data = json.load(f)
                
            print(f"Data loaded successfully for {self.company_name}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def calculate_technical_indicators(self) -> pd.DataFrame:
        """Calculate comprehensive technical indicators"""
        df = self.price_data.copy()
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Volume indicators
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        # Price performance
        df['Returns_1D'] = df['Close'].pct_change()
        df['Returns_5D'] = df['Close'].pct_change(5)
        df['Returns_22D'] = df['Close'].pct_change(22)
        
        # Volatility
        df['Volatility_30D'] = df['Returns_1D'].rolling(window=30).std() * np.sqrt(252)
        
        return df
        
    def perform_valuation_analysis(self) -> Dict[str, any]:
        """Comprehensive valuation analysis"""
        valuation = {}
        
        # Current market metrics
        current_price = self.price_data['Close'].iloc[-1]
        market_cap = self.company_info.get('marketCap', 0)
        
        # Multiples analysis
        pe_ratio = self.company_info.get('forwardPE', self.company_info.get('trailingPE', 0))
        pb_ratio = self.company_info.get('priceToBook', 0)
        ps_ratio = self.company_info.get('priceToSalesTrailing12Months', 0)
        ev_revenue = self.company_info.get('enterpriseToRevenue', 0)
        ev_ebitda = self.company_info.get('enterpriseToEbitda', 0)
        
        valuation['current_metrics'] = {
            'price': current_price,
            'market_cap': market_cap,
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'ps_ratio': ps_ratio,
            'ev_revenue': ev_revenue,
            'ev_ebitda': ev_ebitda
        }
        
        # Peer comparison
        peer_multiples = self._calculate_peer_multiples()
        valuation['peer_comparison'] = peer_multiples
        
        # DCF Model (simplified)
        dcf_value = self._simple_dcf_model()
        valuation['dcf_valuation'] = dcf_value
        
        # Price targets based on different methods
        price_targets = self._calculate_price_targets(peer_multiples, dcf_value)
        valuation['price_targets'] = price_targets
        
        return valuation
        
    def _calculate_peer_multiples(self) -> Dict[str, any]:
        """Calculate peer group valuation multiples"""
        peer_metrics = {
            'pe_ratios': [],
            'pb_ratios': [],
            'market_caps': []
        }
        
        # Filter for main gold mining peers (avoid duplicates)
        main_peers = ['NEM', 'AEM', 'KGC', 'AU', 'EGO']
        
        for symbol in main_peers:
            if symbol in self.peer_data:
                data = self.peer_data[symbol]
                if data['pe_ratio'] > 0:
                    peer_metrics['pe_ratios'].append(data['pe_ratio'])
                if data['pb_ratio'] > 0:
                    peer_metrics['pb_ratios'].append(data['pb_ratio'])
                peer_metrics['market_caps'].append(data['market_cap'])
        
        # Calculate statistics
        return {
            'pe_median': np.median(peer_metrics['pe_ratios']) if peer_metrics['pe_ratios'] else 0,
            'pe_mean': np.mean(peer_metrics['pe_ratios']) if peer_metrics['pe_ratios'] else 0,
            'pb_median': np.median(peer_metrics['pb_ratios']) if peer_metrics['pb_ratios'] else 0,
            'pb_mean': np.mean(peer_metrics['pb_ratios']) if peer_metrics['pb_ratios'] else 0,
            'market_cap_median': np.median(peer_metrics['market_caps']) if peer_metrics['market_caps'] else 0,
            'peer_count': len(main_peers)
        }
        
    def _simple_dcf_model(self) -> Dict[str, float]:
        """Simplified DCF valuation model"""
        try:
            # Basic assumptions for DCF
            current_price = self.price_data['Close'].iloc[-1]
            
            # Estimate free cash flow (simplified using market cap and margins)
            market_cap = self.company_info.get('marketCap', 0)
            operating_margin = self.company_info.get('operatingMargins', 0.15)  # Default 15%
            revenue_growth = self.company_info.get('revenueGrowth', 0.05)  # Default 5%
            
            # Simplified DCF calculation
            estimated_revenue = market_cap / 2  # Rough estimate
            estimated_fcf = estimated_revenue * operating_margin * 0.8  # Convert to FCF
            
            # 5-year projection
            wacc = 0.08  # Assumed weighted average cost of capital
            terminal_growth = 0.03  # Long-term growth rate
            
            pv_fcf = 0
            for year in range(1, 6):
                fcf = estimated_fcf * (1 + revenue_growth) ** year
                pv = fcf / (1 + wacc) ** year
                pv_fcf += pv
                
            # Terminal value
            terminal_fcf = estimated_fcf * (1 + revenue_growth) ** 5 * (1 + terminal_growth)
            terminal_value = terminal_fcf / (wacc - terminal_growth)
            pv_terminal = terminal_value / (1 + wacc) ** 5
            
            enterprise_value = pv_fcf + pv_terminal
            shares_outstanding = market_cap / current_price if current_price > 0 else 1
            dcf_price_per_share = enterprise_value / shares_outstanding if shares_outstanding > 0 else 0
            
            return {
                'dcf_value_per_share': dcf_price_per_share,
                'current_price': current_price,
                'upside_downside': (dcf_price_per_share - current_price) / current_price * 100 if current_price > 0 else 0,
                'assumptions': {
                    'wacc': wacc,
                    'terminal_growth': terminal_growth,
                    'revenue_growth': revenue_growth,
                    'operating_margin': operating_margin
                }
            }
        except Exception as e:
            print(f"DCF calculation error: {e}")
            return {'dcf_value_per_share': 0, 'current_price': 0, 'upside_downside': 0}
            
    def _calculate_price_targets(self, peer_multiples, dcf_value) -> Dict[str, float]:
        """Calculate price targets using different methodologies"""
        current_price = self.price_data['Close'].iloc[-1]
        
        # Peer multiple-based targets
        pe_target = 0
        pb_target = 0
        
        if peer_multiples['pe_median'] > 0:
            # Estimate EPS from P/E ratio
            current_pe = self.company_info.get('forwardPE', 0)
            if current_pe > 0:
                estimated_eps = current_price / current_pe
                pe_target = estimated_eps * peer_multiples['pe_median']
                
        if peer_multiples['pb_median'] > 0:
            # Estimate book value per share
            current_pb = self.company_info.get('priceToBook', 0)
            if current_pb > 0:
                estimated_bvps = current_price / current_pb
                pb_target = estimated_bvps * peer_multiples['pb_median']
        
        # Technical targets
        recent_high = self.price_data['High'].tail(252).max()  # 1-year high
        recent_low = self.price_data['Low'].tail(252).min()   # 1-year low
        
        # Average of all methods
        targets = [t for t in [pe_target, pb_target, dcf_value.get('dcf_value_per_share', 0)] if t > 0]
        avg_target = np.mean(targets) if targets else current_price
        
        return {
            'pe_multiple_target': pe_target,
            'pb_multiple_target': pb_target,
            'dcf_target': dcf_value.get('dcf_value_per_share', 0),
            'average_target': avg_target,
            'current_price': current_price,
            'year_high': recent_high,
            'year_low': recent_low,
            'upside_to_avg_target': (avg_target - current_price) / current_price * 100 if current_price > 0 else 0
        }
        
    def risk_analysis(self) -> Dict[str, any]:
        """Comprehensive risk analysis"""
        risk_metrics = {}
        
        # Price volatility analysis
        returns = self.price_data['Close'].pct_change().dropna()
        
        risk_metrics['volatility'] = {
            'daily_volatility': returns.std(),
            'annual_volatility': returns.std() * np.sqrt(252) * 100,
            'var_95': np.percentile(returns, 5) * 100,  # 5% Value at Risk
            'var_99': np.percentile(returns, 1) * 100   # 1% Value at Risk
        }
        
        # Drawdown analysis
        price_series = self.price_data['Close']
        rolling_max = price_series.expanding().max()
        drawdown = (price_series / rolling_max - 1) * 100
        
        risk_metrics['drawdowns'] = {
            'current_drawdown': drawdown.iloc[-1],
            'max_drawdown': drawdown.min(),
            'avg_drawdown': drawdown[drawdown < 0].mean() if len(drawdown[drawdown < 0]) > 0 else 0
        }
        
        # Beta calculation (vs market proxy)
        # Note: This is simplified - normally would use market index
        beta = self.company_info.get('beta', 1.0)
        
        risk_metrics['market_risk'] = {
            'beta': beta,
            'correlation_vs_peers': self._calculate_peer_correlation()
        }
        
        # Liquidity risk
        avg_volume = self.price_data['Volume'].tail(30).mean()
        risk_metrics['liquidity'] = {
            'avg_daily_volume': avg_volume,
            'dollar_volume': avg_volume * self.price_data['Close'].iloc[-1]
        }
        
        return risk_metrics
        
    def _calculate_peer_correlation(self) -> float:
        """Calculate correlation with peer group (simplified)"""
        # This would normally require peer price data
        # For now, return a reasonable estimate
        return 0.75  # Gold miners typically have high correlation
        
    def generate_investment_thesis(self) -> Dict[str, any]:
        """Generate comprehensive investment thesis"""
        technical_analysis = self.calculate_technical_indicators()
        valuation = self.perform_valuation_analysis()
        risk_analysis = self.risk_analysis()
        
        # Current position analysis
        current_price = self.price_data['Close'].iloc[-1]
        sma_50 = technical_analysis['SMA_50'].iloc[-1]
        sma_200 = technical_analysis['SMA_200'].iloc[-1]
        rsi = technical_analysis['RSI'].iloc[-1]
        
        # Determine trend
        trend = "Bullish" if current_price > sma_50 > sma_200 else "Bearish" if current_price < sma_50 < sma_200 else "Neutral"
        
        # Technical signals
        signals = []
        if rsi > 70:
            signals.append("Overbought (RSI > 70)")
        elif rsi < 30:
            signals.append("Oversold (RSI < 30)")
            
        if current_price > technical_analysis['BB_Upper'].iloc[-1]:
            signals.append("Above Bollinger Upper Band")
        elif current_price < technical_analysis['BB_Lower'].iloc[-1]:
            signals.append("Below Bollinger Lower Band")
        
        # Investment recommendation
        upside = valuation['price_targets']['upside_to_avg_target']
        
        if upside > 20:
            recommendation = "BUY"
        elif upside > 10:
            recommendation = "OVERWEIGHT"
        elif upside > -10:
            recommendation = "HOLD"
        else:
            recommendation = "UNDERWEIGHT"
        
        return {
            'company': self.company_name,
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'current_price': current_price,
            'recommendation': recommendation,
            'price_target': valuation['price_targets']['average_target'],
            'upside_potential': upside,
            'trend': trend,
            'technical_signals': signals,
            'key_metrics': {
                'pe_ratio': valuation['current_metrics']['pe_ratio'],
                'pb_ratio': valuation['current_metrics']['pb_ratio'],
                'market_cap_bn': valuation['current_metrics']['market_cap'] / 1e9,
                'beta': risk_analysis['market_risk']['beta'],
                'annual_volatility': risk_analysis['volatility']['annual_volatility'],
                'rsi': rsi
            },
            'risk_factors': [
                f"High volatility: {risk_analysis['volatility']['annual_volatility']:.1f}% annual",
                f"Maximum drawdown: {risk_analysis['drawdowns']['max_drawdown']:.1f}%",
                "Commodity price exposure",
                "Mining operational risks",
                "Regulatory and environmental risks"
            ],
            'peer_comparison': {
                'vs_peers': 'outperforming' if valuation['current_metrics']['pe_ratio'] < valuation['peer_comparison']['pe_median'] else 'underperforming',
                'peer_median_pe': valuation['peer_comparison']['pe_median'],
                'peer_median_pb': valuation['peer_comparison']['pb_median']
            }
        }

# Usage example
if __name__ == "__main__":
    analyzer = FinancialAnalysisEngine()
    thesis = analyzer.generate_investment_thesis()
    
    print("=== INVESTMENT THESIS ===")
    print(f"Company: {thesis['company']}")
    print(f"Recommendation: {thesis['recommendation']}")
    print(f"Price Target: ${thesis['price_target']:.2f}")
    print(f"Upside Potential: {thesis['upside_potential']:.1f}%")
    print(f"Current Trend: {thesis['trend']}")
    print(f"Risk Level: {thesis['key_metrics']['annual_volatility']:.1f}% volatility")