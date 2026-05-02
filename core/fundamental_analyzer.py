from config import MIN_ROE, MIN_EPS_GROWTH, MIN_REVENUE_GROWTH

class FundamentalAnalyzer:
    @staticmethod
    def analyze(df):
        if df.empty: return 0, False
        latest = df.iloc[-1]
        
        # Use lowercase to match data_collector.py
        roe = latest.get('roe', 0)
        eps_growth = latest.get('eps', 0) # Using eps as a proxy for growth in simulation
        rev_growth = latest.get('revenue_growth', 0)
        
        score = 0
        if roe > MIN_ROE: score += 40
        if eps_growth > MIN_EPS_GROWTH: score += 30
        if rev_growth > MIN_REVENUE_GROWTH: score += 30
        
        return score, (roe > MIN_ROE)
