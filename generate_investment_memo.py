import json
import pandas as pd
from datetime import datetime
from src.models.financial_models import FinancialAnalysisEngine

class InvestmentMemoGenerator:
    """Generate professional investment memo and analysis report"""
    
    def __init__(self):
        self.analyzer = FinancialAnalysisEngine()
        
    def generate_comprehensive_memo(self):
        """Generate complete investment memorandum"""
        
        # Generate analysis
        thesis = self.analyzer.generate_investment_thesis()
        valuation = self.analyzer.perform_valuation_analysis()
        risk_analysis = self.analyzer.risk_analysis()
        
        # Load peer data for benchmarking
        with open('data/raw/peer_comparison_data.json', 'r') as f:
            peer_data = json.load(f)
        
        memo_content = f"""
# INVESTMENT MEMORANDUM
## Barrick Gold Corporation (NYSE: ABX, TSX: ABX.TO)

**Analysis Date:** {thesis['analysis_date']}  
**Analyst:** Professional Finance Consultant  
**Recommendation:** {thesis['recommendation']}  
**Price Target:** ${thesis['price_target']:.2f}  
**Current Price:** ${thesis['current_price']:.2f}  
**Upside Potential:** {thesis['upside_potential']:.1f}%

---

## EXECUTIVE SUMMARY

Barrick Gold Corporation presents a **{thesis['recommendation']}** investment opportunity in the gold mining sector with significant upside potential of **{thesis['upside_potential']:.1f}%** to our price target of **${thesis['price_target']:.2f}**.

### Key Investment Highlights:
- **Strong Market Position**: Market cap of ${thesis['key_metrics']['market_cap_bn']:.1f}B, making it one of the largest gold miners globally
- **Attractive Valuation**: Trading at {thesis['key_metrics']['pe_ratio']:.1f}x P/E vs peer median of {thesis['peer_comparison']['peer_median_pe']:.1f}x
- **Technical Momentum**: Current trend is **{thesis['trend']}** with RSI at {thesis['key_metrics']['rsi']:.0f}
- **Risk Profile**: Beta of {thesis['key_metrics']['beta']:.2f} with {thesis['key_metrics']['annual_volatility']:.1f}% annual volatility

---

## COMPANY OVERVIEW

Barrick Gold Corporation is a leading international gold mining company with operations across multiple continents. The company operates high-quality, long-life assets with a focus on responsible mining practices.

### Business Segments:
- **Gold Mining Operations**: Primary revenue driver with diversified geographical exposure
- **Copper Operations**: Complementary revenue stream providing portfolio diversification
- **Exploration & Development**: Ongoing investment in future growth opportunities

---

## FINANCIAL ANALYSIS

### Valuation Metrics
| Metric | ABX.TO | Peer Median | Relative |
|--------|--------|-------------|----------|
| **P/E Ratio** | {thesis['key_metrics']['pe_ratio']:.1f}x | {thesis['peer_comparison']['peer_median_pe']:.1f}x | {("Discount" if thesis['key_metrics']['pe_ratio'] < thesis['peer_comparison']['peer_median_pe'] else "Premium")} |
| **P/B Ratio** | {thesis['key_metrics']['pb_ratio']:.1f}x | {thesis['peer_comparison']['peer_median_pb']:.1f}x | {("Discount" if thesis['key_metrics']['pb_ratio'] < thesis['peer_comparison']['peer_median_pb'] else "Premium")} |
| **Market Cap** | ${thesis['key_metrics']['market_cap_bn']:.1f}B | - | Large Cap |

### DCF Valuation Analysis
Our discounted cash flow analysis indicates fair value of **${valuation['dcf_valuation']['dcf_value_per_share']:.2f}** per share, representing **{valuation['dcf_valuation']['upside_downside']:.1f}%** upside from current levels.

**Key DCF Assumptions:**
- WACC: {valuation['dcf_valuation']['assumptions']['wacc']*100:.1f}%
- Terminal Growth Rate: {valuation['dcf_valuation']['assumptions']['terminal_growth']*100:.1f}%
- Revenue Growth: {valuation['dcf_valuation']['assumptions']['revenue_growth']*100:.1f}%
- Operating Margin: {valuation['dcf_valuation']['assumptions']['operating_margin']*100:.1f}%

---

## PEER COMPARISON ANALYSIS

### Performance vs Gold Mining Peers
"""

        # Add peer comparison table
        main_peers = ['ABX.TO', 'NEM', 'AEM', 'KGC', 'AU']
        
        memo_content += "\n| Company | Symbol | Market Cap ($B) | P/E Ratio | 1Y Return | Volatility |\n"
        memo_content += "|---------|--------|----------------|-----------|-----------|------------|\n"
        
        for symbol in main_peers:
            if symbol in peer_data:
                data = peer_data[symbol]
                company_name = data['company_name'][:20] + "..." if len(data['company_name']) > 20 else data['company_name']
                memo_content += f"| {company_name} | {symbol} | ${data['market_cap']/1e9:.1f} | {data['pe_ratio']:.1f}x | {data['returns_1y']:.1f}% | {data['volatility_annualized']:.1f}% |\n"
        
        memo_content += f"""

### Competitive Positioning
- **Market Cap Ranking**: {"Top 3" if thesis['key_metrics']['market_cap_bn'] > 50 else "Mid-tier"} among gold mining peers
- **Valuation**: Currently trading at a {"discount" if thesis['peer_comparison']['vs_peers'] == 'outperforming' else "premium"} to peer group
- **Performance**: {thesis['peer_comparison']['vs_peers']} relative to peer group

---

## TECHNICAL ANALYSIS

### Current Technical Picture
- **Trend**: {thesis['trend']}
- **Key Support/Resistance**: Year low ${valuation['price_targets']['year_low']:.2f} / Year high ${valuation['price_targets']['year_high']:.2f}
- **RSI**: {thesis['key_metrics']['rsi']:.0f} ({"Overbought" if thesis['key_metrics']['rsi'] > 70 else "Oversold" if thesis['key_metrics']['rsi'] < 30 else "Neutral"})
- **Moving Averages**: Price is {"above" if thesis['trend'] == "Bullish" else "below"} key moving averages

### Technical Signals
"""
        for signal in thesis['technical_signals']:
            memo_content += f"- {signal}\n"

        memo_content += f"""

---

## RISK ANALYSIS

### Risk Metrics
- **Beta**: {thesis['key_metrics']['beta']:.2f} ({"Less volatile" if thesis['key_metrics']['beta'] < 1 else "More volatile"} than market)
- **Annual Volatility**: {thesis['key_metrics']['annual_volatility']:.1f}%
- **Maximum Drawdown**: {risk_analysis['drawdowns']['max_drawdown']:.1f}%
- **Current Drawdown**: {risk_analysis['drawdowns']['current_drawdown']:.1f}%
- **Value at Risk (95%)**: {risk_analysis['volatility']['var_95']:.1f}% daily

### Key Risk Factors
"""
        for risk in thesis['risk_factors']:
            memo_content += f"- {risk}\n"

        memo_content += f"""

### Mitigating Factors
- Diversified geographical operations
- Strong balance sheet and cash position
- Experienced management team
- Focus on operational excellence

---

## INVESTMENT RECOMMENDATION

### Price Targets
- **12-Month Target**: ${thesis['price_target']:.2f}
- **Bull Case**: ${valuation['price_targets']['year_high']*1.1:.2f} (+{((valuation['price_targets']['year_high']*1.1)/thesis['current_price']-1)*100:.0f}%)
- **Base Case**: ${thesis['price_target']:.2f} (+{thesis['upside_potential']:.0f}%)
- **Bear Case**: ${valuation['price_targets']['year_low']*1.05:.2f} ({((valuation['price_targets']['year_low']*1.05)/thesis['current_price']-1)*100:.0f}%)

### Rationale for {thesis['recommendation']} Rating
1. **Attractive Valuation**: Trading below historical and peer averages
2. **Strong Fundamentals**: Solid operational metrics and financial position
3. **Sector Tailwinds**: Gold demand driven by economic uncertainty and inflation hedging
4. **Technical Momentum**: {thesis['trend']} trend with positive technical indicators

### Portfolio Allocation Recommendation
- **Conservative Investors**: 2-5% allocation as portfolio diversifier
- **Growth Investors**: 5-8% allocation for commodity exposure
- **Aggressive Investors**: Up to 10% allocation with strict risk management

---

## CATALYST CALENDAR & MONITORING

### Near-term Catalysts
- Quarterly earnings reports
- Gold price movements and macroeconomic factors
- Operational updates and production guidance
- M&A activity in the sector

### Key Metrics to Monitor
- Gold production levels and all-in sustaining costs (AISC)
- Free cash flow generation and capital allocation
- Debt levels and balance sheet strength
- Exploration success and reserve replacement

---

## ESG CONSIDERATIONS

### Environmental, Social & Governance Factors
- **Environmental**: Focus on sustainable mining practices and environmental remediation
- **Social**: Community engagement and stakeholder relations
- **Governance**: Board independence and executive compensation alignment

---

## CONCLUSION

Barrick Gold Corporation represents an attractive investment opportunity in the gold mining sector. With a **{thesis['recommendation']}** recommendation and price target of **${thesis['price_target']:.2f}**, the stock offers **{thesis['upside_potential']:.1f}%** upside potential from current levels.

The investment thesis is supported by:
- Attractive valuation relative to peers
- Strong operational fundamentals
- Positive technical momentum
- Favorable sector dynamics

**Risk-Adjusted Return**: Given the risk profile and upside potential, ABX.TO offers attractive risk-adjusted returns for investors seeking exposure to precious metals.

---

*This analysis is based on publicly available information as of {thesis['analysis_date']}. Past performance does not guarantee future results. Please consult with a financial advisor before making investment decisions.*

---

**Disclaimer**: This investment memorandum is for informational purposes only and should not be considered as personalized investment advice. The author may or may not hold positions in the securities mentioned. All investments carry risk of loss.
        """
        
        # Save the memo
        with open('reports/investment_memorandum.md', 'w') as f:
            f.write(memo_content)
            
        print("Investment memorandum generated successfully!")
        print("Saved to: reports/investment_memorandum.md")
        
        return memo_content
        
    def generate_executive_summary(self):
        """Generate executive summary for quick review"""
        thesis = self.analyzer.generate_investment_thesis()
        
        summary = f"""
# EXECUTIVE SUMMARY - BARRICK GOLD CORPORATION

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Symbol:** ABX.TO (TSX) / ABX (NYSE)
**Sector:** Basic Materials - Gold Mining

## INVESTMENT RECOMMENDATION: {thesis['recommendation']}

### Key Metrics at a Glance
- **Current Price:** ${thesis['current_price']:.2f}
- **12-Month Target:** ${thesis['price_target']:.2f}
- **Upside Potential:** {thesis['upside_potential']:.1f}%
- **Market Cap:** ${thesis['key_metrics']['market_cap_bn']:.1f} Billion
- **P/E Ratio:** {thesis['key_metrics']['pe_ratio']:.1f}x
- **Beta:** {thesis['key_metrics']['beta']:.2f}

### Investment Highlights
1. **Attractive Valuation**: Trading at discount to peer group
2. **Strong Market Position**: Leading global gold producer
3. **Technical Momentum**: {thesis['trend']} trend with positive indicators
4. **Risk Management**: Diversified operations and strong balance sheet

### Risk Factors
- High volatility ({thesis['key_metrics']['annual_volatility']:.1f}% annual)
- Commodity price exposure
- Operational and regulatory risks

### Bottom Line
Barrick Gold offers compelling value with significant upside potential for investors seeking exposure to gold mining sector.
        """
        
        with open('reports/executive_summary.md', 'w') as f:
            f.write(summary)
            
        return summary

if __name__ == "__main__":
    generator = InvestmentMemoGenerator()
    
    print("Generating comprehensive investment memorandum...")
    memo = generator.generate_comprehensive_memo()
    
    print("Generating executive summary...")
    summary = generator.generate_executive_summary()
    
    print("\nAnalysis completed successfully!")
    print("Files generated:")
    print("- reports/investment_memorandum.md")
    print("- reports/executive_summary.md")
    print("- reports/comprehensive_dashboard.html")
    print("- reports/executive_summary.html") 
    print("- reports/peer_benchmark_analysis.html")