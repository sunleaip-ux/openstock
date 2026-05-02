from config import MIN_ROE, MIN_EPS_GROWTH, MIN_REVENUE_GROWTH
class FundamentalAnalyzer:
    @staticmethod
    def analyze(df):
        if df.empty: return 0, False
        latest = df.iloc[-1]
        roe = latest.get('ROE', 0)
        eps_growth = latest.get('EPS_growth', 0)
        rev_growth = latest.get('Revenue_growth', 0)
        score = 0
        if roe > MIN_ROE: score += 40
        if eps_growth > MIN_EPS_GROWTH: score += 30
        if rev_growth > MIN_REVENUE_GROWTH: score += 30
        return score, (roe > MIN_ROE)
