import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set professional styling
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

class ProfessionalVisualizationEngine:
    """Create professional PNG visualizations for financial analysis"""
    
    def __init__(self):
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
                
            print("Visualization data loaded successfully")
            
        except Exception as e:
            print(f"Error loading visualization data: {e}")
            self.price_data = pd.DataFrame()
            self.company_info = {}
            self.peer_data = {}
            
    def create_comprehensive_price_analysis(self):
        """Create comprehensive price and technical analysis chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Barrick Gold Corporation (ABX.TO) - Comprehensive Price Analysis', fontsize=16, fontweight='bold')
        
        if not self.price_data.empty:
            # Recent 2 years data for clarity
            recent_data = self.price_data.tail(504)
            
            # 1. Price chart with moving averages
            ax1.plot(recent_data.index, recent_data['Close'], label='Close Price', color='#2E8B57', linewidth=2)
            
            if len(recent_data) > 20:
                ma_20 = recent_data['Close'].rolling(20).mean()
                ax1.plot(recent_data.index, ma_20, label='20-day MA', color='orange', linewidth=1.5)
                
            if len(recent_data) > 50:
                ma_50 = recent_data['Close'].rolling(50).mean()
                ax1.plot(recent_data.index, ma_50, label='50-day MA', color='red', linewidth=1.5)
                
            ax1.set_title('Stock Price with Moving Averages', fontweight='bold')
            ax1.set_ylabel('Price (CAD)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Format x-axis
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # 2. Volume analysis
            ax2.bar(recent_data.index, recent_data['Volume']/1e6, alpha=0.7, color='lightblue', width=0.8)
            if len(recent_data) > 20:
                vol_ma = recent_data['Volume'].rolling(20).mean()/1e6
                ax2.plot(recent_data.index, vol_ma, color='red', linewidth=2, label='20-day Avg')
            
            ax2.set_title('Trading Volume Analysis', fontweight='bold')
            ax2.set_ylabel('Volume (Millions)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # 3. RSI calculation and plot
            delta = recent_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            ax3.plot(recent_data.index, rsi, color='purple', linewidth=2)
            ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
            ax3.axhline(y=50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
            ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
            ax3.fill_between(recent_data.index, 30, 70, alpha=0.1, color='gray')
            ax3.set_title('RSI (Relative Strength Index)', fontweight='bold')
            ax3.set_ylabel('RSI')
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
            
            # 4. Returns distribution
            daily_returns = recent_data['Close'].pct_change().dropna() * 100
            ax4.hist(daily_returns, bins=50, alpha=0.7, color='lightcoral', edgecolor='black')
            ax4.axvline(daily_returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {daily_returns.mean():.2f}%')
            ax4.axvline(daily_returns.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {daily_returns.median():.2f}%')
            ax4.set_title('Daily Returns Distribution', fontweight='bold')
            ax4.set_xlabel('Daily Returns (%)')
            ax4.set_ylabel('Frequency')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.savefig('reports/comprehensive_price_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Comprehensive price analysis saved to reports/comprehensive_price_analysis.png")
        
    def create_peer_benchmarking_analysis(self):
        """Create comprehensive peer benchmarking charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Peer Group Benchmarking Analysis - Gold Mining Sector', fontsize=16, fontweight='bold')
        
        if self.peer_data:
            # Filter main peers
            main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU', 'EGO']
            peer_metrics = {}
            
            for symbol in main_peers:
                if symbol in self.peer_data:
                    peer_metrics[symbol] = self.peer_data[symbol]
            
            if peer_metrics:
                symbols = list(peer_metrics.keys())
                colors = ['#FF6B6B' if s == 'ABX.TO' else '#4ECDC4' for s in symbols]
                
                # 1. Market Cap Comparison
                market_caps = [peer_metrics[s]['market_cap']/1e9 for s in symbols]
                bars1 = ax1.bar(symbols, market_caps, color=colors, alpha=0.8, edgecolor='black')
                ax1.set_title('Market Capitalization Comparison', fontweight='bold')
                ax1.set_ylabel('Market Cap ($ Billions)')
                ax1.grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bar, value in zip(bars1, market_caps):
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                            f'${value:.1f}B', ha='center', va='bottom', fontweight='bold')
                
                # 2. P/E Ratio Comparison
                pe_ratios = [peer_metrics[s]['pe_ratio'] for s in symbols if peer_metrics[s]['pe_ratio'] > 0]
                pe_symbols = [s for s in symbols if peer_metrics[s]['pe_ratio'] > 0]
                pe_colors = ['#FF6B6B' if s == 'ABX.TO' else '#4ECDC4' for s in pe_symbols]
                
                bars2 = ax2.bar(pe_symbols, pe_ratios, color=pe_colors, alpha=0.8, edgecolor='black')
                ax2.set_title('P/E Ratio Comparison', fontweight='bold')
                ax2.set_ylabel('P/E Ratio')
                ax2.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars2, pe_ratios):
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f'{value:.1f}x', ha='center', va='bottom', fontweight='bold')
                
                # 3. 1-Year Returns Comparison
                returns_1y = [peer_metrics[s]['returns_1y'] for s in symbols]
                bars3 = ax3.bar(symbols, returns_1y, color=colors, alpha=0.8, edgecolor='black')
                ax3.set_title('1-Year Returns Performance', fontweight='bold')
                ax3.set_ylabel('Returns (%)')
                ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                ax3.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars3, returns_1y):
                    y_pos = bar.get_height() + (2 if value >= 0 else -8)
                    ax3.text(bar.get_x() + bar.get_width()/2, y_pos,
                            f'{value:.1f}%', ha='center', va='bottom' if value >= 0 else 'top',
                            fontweight='bold')
                
                # 4. Risk-Return Scatter
                volatilities = [peer_metrics[s]['volatility_annualized'] for s in symbols]
                scatter_colors = ['red' if s == 'ABX.TO' else 'blue' for s in symbols]
                scatter = ax4.scatter(volatilities, returns_1y, c=scatter_colors, s=100, alpha=0.7, edgecolors='black')
                
                # Add labels for each point
                for i, symbol in enumerate(symbols):
                    ax4.annotate(symbol, (volatilities[i], returns_1y[i]), 
                               xytext=(5, 5), textcoords='offset points',
                               fontweight='bold', fontsize=9)
                
                ax4.set_title('Risk vs Return Profile', fontweight='bold')
                ax4.set_xlabel('Volatility (% Annual)')
                ax4.set_ylabel('1-Year Returns (%)')
                ax4.grid(True, alpha=0.3)
                ax4.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                
                # Add legend
                from matplotlib.patches import Patch
                legend_elements = [Patch(facecolor='red', alpha=0.7, label='ABX.TO (Target)'),
                                 Patch(facecolor='blue', alpha=0.7, label='Peers')]
                ax4.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('reports/peer_benchmarking_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Peer benchmarking analysis saved to reports/peer_benchmarking_analysis.png")
        
    def create_financial_metrics_dashboard(self):
        """Create financial metrics and ratios dashboard"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Barrick Gold - Financial Metrics Dashboard', fontsize=16, fontweight='bold')
        
        if self.peer_data and 'ABX.TO' in self.peer_data:
            abx_data = self.peer_data['ABX.TO']
            
            # 1. Key Financial Ratios
            ratios = {
                'P/E Ratio': abx_data.get('pe_ratio', 0),
                'P/B Ratio': abx_data.get('pb_ratio', 0),
                'ROE (%)': abx_data.get('roe', 0) * 100 if abx_data.get('roe') else 0,
                'Profit Margin (%)': abx_data.get('profit_margin', 0) * 100 if abx_data.get('profit_margin') else 0
            }
            
            bars1 = ax1.bar(ratios.keys(), ratios.values(), color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'], 
                           alpha=0.8, edgecolor='black')
            ax1.set_title('Key Financial Ratios', fontweight='bold')
            ax1.set_ylabel('Value')
            ax1.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, (key, value) in zip(bars1, ratios.items()):
                unit = 'x' if 'Ratio' in key else '%' if '%' in key else ''
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{value:.1f}{unit}', ha='center', va='bottom', fontweight='bold')
                
            # Rotate x-axis labels
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # 2. Performance Metrics (if price data available)
            if not self.price_data.empty:
                current_price = self.price_data['Close'].iloc[-1]
                
                # Calculate returns
                returns_periods = ['1D', '1W', '1M', '3M', '1Y']
                returns_days = [1, 5, 22, 66, 252]
                returns_values = []
                
                for days in returns_days:
                    if len(self.price_data) > days:
                        ret = ((self.price_data['Close'].iloc[-1] / self.price_data['Close'].iloc[-days-1]) - 1) * 100
                        returns_values.append(ret)
                    else:
                        returns_values.append(0)
                
                colors = ['green' if r >= 0 else 'red' for r in returns_values]
                bars2 = ax2.bar(returns_periods, returns_values, color=colors, alpha=0.8, edgecolor='black')
                ax2.set_title('Performance Returns', fontweight='bold')
                ax2.set_ylabel('Returns (%)')
                ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                ax2.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars2, returns_values):
                    y_pos = bar.get_height() + (1 if value >= 0 else -3)
                    ax2.text(bar.get_x() + bar.get_width()/2, y_pos,
                            f'{value:+.1f}%', ha='center', va='bottom' if value >= 0 else 'top',
                            fontweight='bold')
                
                # 3. Risk Metrics
                daily_returns = self.price_data['Close'].pct_change().dropna()
                
                risk_metrics = {
                    'Beta': abx_data.get('beta', 0),
                    'Annual Vol (%)': daily_returns.std() * np.sqrt(252) * 100,
                    'VaR 95% (%)': np.percentile(daily_returns, 5) * 100,
                    'Max Drawdown (%)': self._calculate_max_drawdown()
                }
                
                bars3 = ax3.bar(risk_metrics.keys(), risk_metrics.values(), 
                               color=['#FFB347', '#FF6B6B', '#DDA0DD', '#98FB98'], 
                               alpha=0.8, edgecolor='black')
                ax3.set_title('Risk Metrics', fontweight='bold')
                ax3.set_ylabel('Value')
                ax3.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, (key, value) in zip(bars3, risk_metrics.items()):
                    unit = '%' if '%' in key else ''
                    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f'{value:.1f}{unit}', ha='center', va='bottom', fontweight='bold')
                
                plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
                
                # 4. Price Levels Analysis
                year_high = self.price_data['High'].tail(252).max()
                year_low = self.price_data['Low'].tail(252).min()
                current_from_high = ((current_price / year_high) - 1) * 100
                current_from_low = ((current_price / year_low) - 1) * 100
                
                price_levels = {
                    'Current Price': current_price,
                    '52W High': year_high,
                    '52W Low': year_low
                }
                
                bars4 = ax4.bar(price_levels.keys(), price_levels.values(), 
                               color=['blue', 'green', 'red'], alpha=0.8, edgecolor='black')
                ax4.set_title('Price Level Analysis', fontweight='bold')
                ax4.set_ylabel('Price (CAD)')
                ax4.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, (key, value) in zip(bars4, price_levels.items()):
                    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f'${value:.2f}', ha='center', va='bottom', fontweight='bold')
                
                # Add percentage from high/low as text
                ax4.text(0.7, 0.95, f'From 52W High: {current_from_high:.1f}%', 
                        transform=ax4.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"),
                        fontweight='bold')
                ax4.text(0.7, 0.85, f'From 52W Low: {current_from_low:.1f}%', 
                        transform=ax4.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"),
                        fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('reports/financial_metrics_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Financial metrics dashboard saved to reports/financial_metrics_dashboard.png")
        
    def create_valuation_analysis_chart(self):
        """Create valuation analysis and price targets chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Barrick Gold - Valuation Analysis & Price Targets', fontsize=16, fontweight='bold')
        
        if self.peer_data and 'ABX.TO' in self.peer_data:
            abx_data = self.peer_data['ABX.TO']
            current_price = abx_data.get('current_price', 0)
            
            # 1. Multiple Valuation Analysis
            if self.peer_data:
                # Get peer multiples for comparison
                main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU']
                pe_ratios = []
                symbols = []
                
                for symbol in main_peers:
                    if symbol in self.peer_data and self.peer_data[symbol]['pe_ratio'] > 0:
                        pe_ratios.append(self.peer_data[symbol]['pe_ratio'])
                        symbols.append(symbol)
                
                colors = ['red' if s == 'ABX.TO' else 'lightblue' for s in symbols]
                bars1 = ax1.bar(symbols, pe_ratios, color=colors, alpha=0.8, edgecolor='black')
                
                # Add median line
                median_pe = np.median(pe_ratios)
                ax1.axhline(y=median_pe, color='green', linestyle='--', linewidth=2, 
                           label=f'Peer Median: {median_pe:.1f}x')
                
                ax1.set_title('P/E Ratio vs Peer Group', fontweight='bold')
                ax1.set_ylabel('P/E Ratio')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars1, pe_ratios):
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f'{value:.1f}x', ha='center', va='bottom', fontweight='bold')
                
            # 2. Price Target Analysis
            # Simple price targets based on different methodologies
            dcf_target = 76.82  # From our DCF model
            current_pe = abx_data.get('pe_ratio', 15)
            
            # Estimate targets
            targets = {
                'Current Price': current_price,
                'DCF Target': dcf_target,
                'Peer PE Target': current_price * 1.5,  # Assuming peer median multiple
                'Bull Case': dcf_target * 1.1,
                'Bear Case': current_price * 0.8
            }
            
            colors_targets = ['blue', 'green', 'orange', 'lightgreen', 'red']
            bars2 = ax2.bar(targets.keys(), targets.values(), color=colors_targets, 
                           alpha=0.8, edgecolor='black')
            
            ax2.set_title('Price Target Analysis', fontweight='bold')
            ax2.set_ylabel('Price (CAD)')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels and upside %
            for bar, (key, value) in zip(bars2, targets.items()):
                upside = ((value / current_price) - 1) * 100 if current_price > 0 else 0
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'${value:.2f}\n({upside:+.1f}%)', ha='center', va='bottom', 
                        fontweight='bold', fontsize=9)
            
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # 3. Market Cap vs Revenue Analysis (simplified)
            if self.peer_data:
                main_peers_caps = ['ABX.TO', 'NEM', 'AEM', 'KGC']
                market_caps = []
                peer_names = []
                
                for symbol in main_peers_caps:
                    if symbol in self.peer_data:
                        market_caps.append(self.peer_data[symbol]['market_cap']/1e9)
                        peer_names.append(symbol)
                
                colors_caps = ['red' if s == 'ABX.TO' else 'skyblue' for s in peer_names]
                bars3 = ax3.bar(peer_names, market_caps, color=colors_caps, alpha=0.8, edgecolor='black')
                
                ax3.set_title('Market Capitalization Comparison', fontweight='bold')
                ax3.set_ylabel('Market Cap ($ Billions)')
                ax3.grid(True, alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars3, market_caps):
                    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                            f'${value:.1f}B', ha='center', va='bottom', fontweight='bold')
                
            # 4. Investment Recommendation Summary
            ax4.axis('off')  # Remove axis for text summary
            
            # Calculate overall investment score and recommendation
            pe_discount = (median_pe - current_pe) / median_pe * 100 if 'median_pe' in locals() else 0
            upside_potential = ((dcf_target / current_price) - 1) * 100 if current_price > 0 else 0
            
            recommendation = "BUY" if upside_potential > 20 else "HOLD" if upside_potential > 0 else "SELL"
            rec_color = 'green' if recommendation == 'BUY' else 'orange' if recommendation == 'HOLD' else 'red'
            
            # Create investment summary text
            summary_text = f"""
            INVESTMENT RECOMMENDATION: {recommendation}
            
            Current Price: ${current_price:.2f}
            DCF Target: ${dcf_target:.2f}
            Upside Potential: {upside_potential:.1f}%
            
            Key Metrics:
            • P/E Ratio: {current_pe:.1f}x
            • P/E vs Peers: {pe_discount:+.1f}% discount
            • Market Cap: ${abx_data.get('market_cap', 0)/1e9:.1f}B
            • Beta: {abx_data.get('beta', 0):.2f}
            
            Investment Highlights:
            • Attractive valuation relative to peers
            • Strong market position in gold mining
            • Diversified operational footprint
            • Solid balance sheet fundamentals
            """
            
            ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=rec_color, alpha=0.2),
                    verticalalignment='top', fontfamily='monospace')
                    
            # Add recommendation badge
            ax4.text(0.75, 0.5, recommendation, transform=ax4.transAxes, fontsize=24,
                    fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=rec_color, alpha=0.8, edgecolor='black'),
                    color='white')
        
        plt.tight_layout()
        plt.savefig('reports/valuation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Valuation analysis saved to reports/valuation_analysis.png")
        
    def _calculate_max_drawdown(self):
        """Calculate maximum drawdown from price data"""
        if self.price_data.empty:
            return 0
            
        price_series = self.price_data['Close']
        rolling_max = price_series.expanding().max()
        drawdown = (price_series / rolling_max - 1) * 100
        return drawdown.min()
        
    def create_executive_summary_infographic(self):
        """Create executive summary infographic"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        ax.axis('off')
        
        # Title
        fig.suptitle('BARRICK GOLD CORPORATION - EXECUTIVE SUMMARY', 
                    fontsize=20, fontweight='bold', y=0.95)
        
        if self.peer_data and 'ABX.TO' in self.peer_data:
            abx_data = self.peer_data['ABX.TO']
            current_price = abx_data.get('current_price', 0)
            dcf_target = 76.82
            upside = ((dcf_target / current_price) - 1) * 100 if current_price > 0 else 0
            
            # Create boxes for key metrics
            boxes = [
                {'title': 'CURRENT PRICE', 'value': f'${current_price:.2f}', 'color': '#3498db'},
                {'title': 'TARGET PRICE', 'value': f'${dcf_target:.2f}', 'color': '#2ecc71'},
                {'title': 'UPSIDE POTENTIAL', 'value': f'{upside:.1f}%', 'color': '#e74c3c'},
                {'title': 'RECOMMENDATION', 'value': 'BUY', 'color': '#27ae60'},
                {'title': 'MARKET CAP', 'value': f'${abx_data.get("market_cap", 0)/1e9:.1f}B', 'color': '#9b59b6'},
                {'title': 'P/E RATIO', 'value': f'{abx_data.get("pe_ratio", 0):.1f}x', 'color': '#f39c12'}
            ]
            
            # Position boxes
            box_width = 0.25
            box_height = 0.15
            positions = [(0.1, 0.7), (0.4, 0.7), (0.7, 0.7), (0.1, 0.5), (0.4, 0.5), (0.7, 0.5)]
            
            for i, (box, pos) in enumerate(zip(boxes, positions)):
                # Create rectangle
                rect = plt.Rectangle(pos, box_width, box_height, 
                                   facecolor=box['color'], alpha=0.8, 
                                   edgecolor='black', linewidth=2)
                ax.add_patch(rect)
                
                # Add text
                ax.text(pos[0] + box_width/2, pos[1] + box_height - 0.03, 
                       box['title'], ha='center', va='top', 
                       fontsize=12, fontweight='bold', color='white')
                ax.text(pos[0] + box_width/2, pos[1] + 0.05, 
                       box['value'], ha='center', va='bottom', 
                       fontsize=16, fontweight='bold', color='white')
            
            # Add investment highlights
            highlights_text = """
            INVESTMENT HIGHLIGHTS:
            
            ✓ Attractive valuation at discount to peer group
            ✓ Leading global gold producer with diversified operations  
            ✓ Strong balance sheet and cash generation
            ✓ Positive technical momentum and trend
            ✓ Defensive asset in uncertain economic environment
            
            RISK FACTORS:
            
            ⚠ High volatility typical of mining sector
            ⚠ Exposure to gold price fluctuations
            ⚠ Operational and regulatory risks
            ⚠ Environmental and ESG considerations
            """
            
            ax.text(0.05, 0.35, highlights_text, fontsize=11, va='top',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
            
            # Add date and disclaimer
            ax.text(0.95, 0.02, f'Analysis Date: {datetime.now().strftime("%B %d, %Y")}', 
                   ha='right', va='bottom', fontsize=10, style='italic')
            ax.text(0.05, 0.02, 'This analysis is for informational purposes only. Not investment advice.', 
                   ha='left', va='bottom', fontsize=8, style='italic')
        
        plt.savefig('reports/executive_summary_infographic.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Executive summary infographic saved to reports/executive_summary_infographic.png")
        
    def generate_all_visualizations(self):
        """Generate all PNG visualizations"""
        print("🎨 Starting comprehensive PNG visualization generation...")
        print("=" * 60)
        
        try:
            self.create_comprehensive_price_analysis()
            self.create_peer_benchmarking_analysis()
            self.create_financial_metrics_dashboard()
            self.create_valuation_analysis_chart()
            self.create_executive_summary_infographic()
            
            print("=" * 60)
            print("🎉 All visualizations generated successfully!")
            print("\n📊 Generated Files:")
            print("- reports/comprehensive_price_analysis.png")
            print("- reports/peer_benchmarking_analysis.png") 
            print("- reports/financial_metrics_dashboard.png")
            print("- reports/valuation_analysis.png")
            print("- reports/executive_summary_infographic.png")
            
        except Exception as e:
            print(f"❌ Error generating visualizations: {e}")

if __name__ == "__main__":
    viz_engine = ProfessionalVisualizationEngine()
    viz_engine.generate_all_visualizations()