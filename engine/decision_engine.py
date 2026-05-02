from config import FINAL_SCORE_THRESHOLD
class DecisionEngine:
    @staticmethod
    def apply_risk_control(market_trend, candidate_list):
        if market_trend == 'Overheated': return candidate_list[:2]
        return candidate_list[:5]
    @staticmethod
    def filter_stocks(stock_results):
        return [s for s in stock_results if s['score'] >= FINAL_SCORE_THRESHOLD]
