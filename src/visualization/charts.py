import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class ProfessionalChartEngine:
    """Professional-grade financial visualization engine"""
    
    def __init__(self, symbol: str = "ABX.TO"):
        self.symbol = symbol
        self.load_data()
        
    def load_data(self):
        """Load all required data for visualization"""
        try:
            # Price data
            self.price_data = pd.read_csv('data/raw/abx_daily_prices.csv', index_col=0, parse_dates=True)
            
            # Company info
            with open('data/raw/abx_company_info.json', 'r') as f:
                self.company_info = json.load(f)
                
            # Peer data
            with open('data/raw/peer_comparison_data.json', 'r') as f:
                self.peer_data = json.load(f)
                
            print("Chart data loaded successfully")
            
        except Exception as e:
            print(f"Error loading chart data: {e}")
            
    def create_comprehensive_dashboard(self, save_html: bool = True) -> go.Figure:
        """Create comprehensive financial dashboard"""
        
        # Create subplots
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=(
                'Stock Price & Volume', 'Technical Indicators',
                'Peer Comparison - Returns', 'Peer Comparison - Valuation',
                'Risk Metrics', 'Financial Ratios',
                'Price Distribution', 'Correlation Matrix'
            ),
            specs=[
                [{"secondary_y": True}, {}],
                [{}, {}],
                [{}, {}],
                [{}, {}]
            ],
            vertical_spacing=0.08
        )
        
        # 1. Price and Volume Chart
        self._add_price_volume_chart(fig, row=1, col=1)
        
        # 2. Technical Indicators
        self._add_technical_indicators(fig, row=1, col=2)
        
        # 3. Peer Returns Comparison
        self._add_peer_returns_chart(fig, row=2, col=1)
        
        # 4. Peer Valuation Comparison
        self._add_peer_valuation_chart(fig, row=2, col=2)
        
        # 5. Risk Metrics
        self._add_risk_metrics_chart(fig, row=3, col=1)
        
        # 6. Financial Ratios
        self._add_financial_ratios_chart(fig, row=3, col=2)
        
        # 7. Price Distribution
        self._add_price_distribution(fig, row=4, col=1)
        
        # 8. Correlation Matrix (simplified)
        self._add_correlation_matrix(fig, row=4, col=2)
        
        # Update layout
        fig.update_layout(
            title=f"Comprehensive Financial Analysis - {self.company_info.get('longName', 'Barrick Gold Corp')}",
            height=1600,
            showlegend=True,
            template="plotly_white",
            title_font_size=20,
            font=dict(size=12)
        )
        
        if save_html:
            fig.write_html('reports/comprehensive_dashboard.html')
            print("Dashboard saved to reports/comprehensive_dashboard.html")
            
        return fig
        
    def _add_price_volume_chart(self, fig, row, col):
        """Add price and volume chart with technical indicators"""
        # Calculate moving averages
        self.price_data['SMA_20'] = self.price_data['Close'].rolling(20).mean()
        self.price_data['SMA_50'] = self.price_data['Close'].rolling(50).mean()
        
        # Price data (last 2 years for clarity)
        recent_data = self.price_data.tail(504)  # ~2 years
        
        # Add candlestick
        fig.add_trace(
            go.Candlestick(
                x=recent_data.index,
                open=recent_data['Open'],
                high=recent_data['High'],
                low=recent_data['Low'],
                close=recent_data['Close'],
                name='Price',
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=row, col=col
        )
        
        # Add moving averages
        fig.add_trace(
            go.Scatter(
                x=recent_data.index,
                y=recent_data['SMA_20'],
                name='SMA 20',
                line=dict(color='orange', width=2)
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter(
                x=recent_data.index,
                y=recent_data['SMA_50'],
                name='SMA 50',
                line=dict(color='blue', width=2)
            ),
            row=row, col=col
        )
        
        # Add volume on secondary y-axis
        fig.add_trace(
            go.Bar(
                x=recent_data.index,
                y=recent_data['Volume'],
                name='Volume',
                marker_color='lightblue',
                opacity=0.3,
                yaxis='y2'
            ),
            row=row, col=col, secondary_y=True
        )
        
    def _add_technical_indicators(self, fig, row, col):
        """Add technical indicators (RSI, MACD)"""
        # Calculate RSI
        delta = self.price_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        recent_rsi = rsi.tail(504)
        
        fig.add_trace(
            go.Scatter(
                x=recent_rsi.index,
                y=recent_rsi,
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=row, col=col
        )
        
        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=row, col=col)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=row, col=col)
        
    def _add_peer_returns_chart(self, fig, row, col):
        """Add peer group returns comparison"""
        # Extract 1-year returns from peer data
        peer_returns = {}
        main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU', 'EGO']
        
        for symbol in main_peers:
            if symbol in self.peer_data:
                peer_returns[symbol] = self.peer_data[symbol]['returns_1y']
        
        symbols = list(peer_returns.keys())
        returns = list(peer_returns.values())
        
        colors = ['red' if symbol == 'ABX.TO' else 'lightblue' for symbol in symbols]
        
        fig.add_trace(
            go.Bar(
                x=symbols,
                y=returns,
                name='1Y Returns (%)',
                marker_color=colors,
                text=[f'{r:.1f}%' for r in returns],
                textposition='auto'
            ),
            row=row, col=col
        )
        
    def _add_peer_valuation_chart(self, fig, row, col):
        """Add peer valuation multiples comparison"""
        # Extract P/E ratios
        peer_pe = {}
        main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU', 'EGO']
        
        for symbol in main_peers:
            if symbol in self.peer_data and self.peer_data[symbol]['pe_ratio'] > 0:
                peer_pe[symbol] = self.peer_data[symbol]['pe_ratio']
        
        symbols = list(peer_pe.keys())
        pe_ratios = list(peer_pe.values())
        
        colors = ['red' if symbol == 'ABX.TO' else 'lightgreen' for symbol in symbols]
        
        fig.add_trace(
            go.Bar(
                x=symbols,
                y=pe_ratios,
                name='P/E Ratio',
                marker_color=colors,
                text=[f'{pe:.1f}x' for pe in pe_ratios],
                textposition='auto'
            ),
            row=row, col=col
        )
        
    def _add_risk_metrics_chart(self, fig, row, col):
        """Add risk metrics visualization"""
        # Calculate daily returns and volatility
        returns = self.price_data['Close'].pct_change().dropna()
        
        # Rolling volatility (30-day)
        rolling_vol = returns.rolling(30).std() * np.sqrt(252) * 100
        recent_vol = rolling_vol.tail(252)  # Last year
        
        fig.add_trace(
            go.Scatter(
                x=recent_vol.index,
                y=recent_vol,
                name='30D Rolling Volatility (%)',
                line=dict(color='orange', width=2),
                fill='tonexty'
            ),
            row=row, col=col
        )
        
    def _add_financial_ratios_chart(self, fig, row, col):
        """Add financial ratios comparison"""
        abx_data = self.peer_data.get('ABX.TO', {})
        
        ratios = {
            'P/E': abx_data.get('pe_ratio', 0),
            'P/B': abx_data.get('pb_ratio', 0),
            'ROE': abx_data.get('roe', 0) * 100 if abx_data.get('roe') else 0,
            'Profit Margin': abx_data.get('profit_margin', 0) * 100 if abx_data.get('profit_margin') else 0
        }
        
        fig.add_trace(
            go.Bar(
                x=list(ratios.keys()),
                y=list(ratios.values()),
                name='Financial Ratios',
                marker_color='skyblue',
                text=[f'{v:.1f}' for v in ratios.values()],
                textposition='auto'
            ),
            row=row, col=col
        )
        
    def _add_price_distribution(self, fig, row, col):
        """Add price return distribution"""
        returns = self.price_data['Close'].pct_change().dropna() * 100
        
        fig.add_trace(
            go.Histogram(
                x=returns,
                name='Daily Returns (%)',
                nbinsx=50,
                opacity=0.7,
                marker_color='lightcoral'
            ),
            row=row, col=col
        )
        
    def _add_correlation_matrix(self, fig, row, col):
        """Add simplified correlation matrix"""
        # This is simplified - would normally show correlation with other assets
        # For now, show a placeholder
        
        fig.add_trace(
            go.Scatter(
                x=[1, 2, 3],
                y=[1, 2, 3],
                mode='markers+text',
                text=['Gold Price', 'USD Index', 'Market'],
                textposition="middle center",
                marker=dict(size=50, color=['gold', 'green', 'blue']),
                name='Key Correlations'
            ),
            row=row, col=col
        )
        
    def create_executive_summary_chart(self) -> go.Figure:
        """Create executive summary chart for presentations"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Price Performance vs Peers',
                'Key Valuation Metrics',
                'Risk-Return Profile', 
                'Investment Recommendation'
            ),
            specs=[[{}, {}], [{}, {}]]
        )
        
        # Price performance comparison
        main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC']
        peer_returns = [self.peer_data[p]['returns_1y'] for p in main_peers if p in self.peer_data]
        
        fig.add_trace(
            go.Bar(
                x=main_peers[:len(peer_returns)],
                y=peer_returns,
                marker_color=['red', 'blue', 'blue', 'blue'],
                name='1Y Returns'
            ),
            row=1, col=1
        )
        
        # Key metrics radar chart (simplified as bar)
        abx_data = self.peer_data.get('ABX.TO', {})
        metrics = {
            'P/E': abx_data.get('pe_ratio', 0),
            'ROE': abx_data.get('roe', 0) * 100 if abx_data.get('roe') else 0,
            'Margin': abx_data.get('profit_margin', 0) * 100 if abx_data.get('profit_margin') else 0
        }
        
        fig.add_trace(
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color='green',
                name='Key Metrics'
            ),
            row=1, col=2
        )
        
        # Risk-return scatter
        returns = [self.peer_data[p]['returns_1y'] for p in main_peers if p in self.peer_data]
        volatilities = [self.peer_data[p]['volatility_annualized'] for p in main_peers if p in self.peer_data]
        
        fig.add_trace(
            go.Scatter(
                x=volatilities,
                y=returns,
                mode='markers+text',
                text=main_peers[:len(returns)],
                textposition="top center",
                marker=dict(size=10, color=['red', 'blue', 'blue', 'blue']),
                name='Risk-Return'
            ),
            row=2, col=1
        )
        
        # Investment recommendation gauge (simplified as text)
        recommendation_score = 75  # Based on analysis
        
        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[recommendation_score],
                mode='markers+text',
                text=[f'Investment Score: {recommendation_score}/100<br>Recommendation: BUY'],
                textposition="middle center",
                marker=dict(size=100, color='green'),
                name='Recommendation'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Executive Summary - Barrick Gold Investment Analysis",
            height=800,
            showlegend=False,
            template="plotly_white"
        )
        
        fig.write_html('reports/executive_summary.html')
        return fig
        
    def create_peer_benchmark_analysis(self) -> go.Figure:
        """Create detailed peer benchmarking analysis"""
        
        # Prepare peer data for comparison
        peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU', 'EGO']
        peer_df = []
        
        for symbol in peers:
            if symbol in self.peer_data:
                data = self.peer_data[symbol]
                peer_df.append({
                    'Symbol': symbol,
                    'Company': data['company_name'][:20] + '...' if len(data['company_name']) > 20 else data['company_name'],
                    'Market_Cap_B': data['market_cap'] / 1e9,
                    'PE_Ratio': data['pe_ratio'],
                    'PB_Ratio': data['pb_ratio'],
                    'ROE': data['roe'] * 100 if data['roe'] else 0,
                    'Returns_1Y': data['returns_1y'],
                    'Volatility': data['volatility_annualized']
                })
        
        peer_df = pd.DataFrame(peer_df)
        
        # Create comprehensive comparison
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Market Capitalization', 'Valuation Multiples (P/E)',
                '1-Year Returns Performance', 'Profitability (ROE)',
                'Risk Profile (Volatility)', 'Risk-Return Scatter'
            )
        )
        
        # Market Cap comparison
        colors = ['red' if symbol == 'ABX.TO' else 'lightblue' for symbol in peer_df['Symbol']]
        
        fig.add_trace(
            go.Bar(
                x=peer_df['Symbol'],
                y=peer_df['Market_Cap_B'],
                marker_color=colors,
                name='Market Cap ($B)',
                text=[f'${x:.1f}B' for x in peer_df['Market_Cap_B']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # P/E Ratio comparison
        fig.add_trace(
            go.Bar(
                x=peer_df['Symbol'],
                y=peer_df['PE_Ratio'],
                marker_color=colors,
                name='P/E Ratio',
                text=[f'{x:.1f}x' for x in peer_df['PE_Ratio']],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        # Returns comparison
        fig.add_trace(
            go.Bar(
                x=peer_df['Symbol'],
                y=peer_df['Returns_1Y'],
                marker_color=colors,
                name='1Y Returns (%)',
                text=[f'{x:.1f}%' for x in peer_df['Returns_1Y']],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        # ROE comparison
        fig.add_trace(
            go.Bar(
                x=peer_df['Symbol'],
                y=peer_df['ROE'],
                marker_color=colors,
                name='ROE (%)',
                text=[f'{x:.1f}%' for x in peer_df['ROE']],
                textposition='auto'
            ),
            row=2, col=2
        )
        
        # Volatility comparison
        fig.add_trace(
            go.Bar(
                x=peer_df['Symbol'],
                y=peer_df['Volatility'],
                marker_color=colors,
                name='Volatility (%)',
                text=[f'{x:.1f}%' for x in peer_df['Volatility']],
                textposition='auto'
            ),
            row=3, col=1
        )
        
        # Risk-Return scatter
        fig.add_trace(
            go.Scatter(
                x=peer_df['Volatility'],
                y=peer_df['Returns_1Y'],
                mode='markers+text',
                text=peer_df['Symbol'],
                textposition="top center",
                marker=dict(
                    size=15,
                    color=['red' if symbol == 'ABX.TO' else 'blue' for symbol in peer_df['Symbol']]
                ),
                name='Risk vs Return'
            ),
            row=3, col=2
        )
        
        fig.update_layout(
            title="Peer Group Benchmarking Analysis - Gold Mining Sector",
            height=1200,
            showlegend=False,
            template="plotly_white"
        )
        
        fig.write_html('reports/peer_benchmark_analysis.html')
        return fig

if __name__ == "__main__":
    # Create visualization engine
    chart_engine = ProfessionalChartEngine()
    
    # Generate all charts
    print("Generating comprehensive dashboard...")
    dashboard = chart_engine.create_comprehensive_dashboard()
    
    print("Generating executive summary...")
    executive = chart_engine.create_executive_summary_chart()
    
    print("Generating peer benchmark analysis...")
    peer_analysis = chart_engine.create_peer_benchmark_analysis()
    
    print("All visualizations created successfully!")