from config import INSTITUTION_BUY_DAYS
class ChipAnalyzer:
    @staticmethod
    def analyze(df):
        if df.empty: return 0, False
        recent = df.tail(INSTITUTION_BUY_DAYS)
        foreign_buy = (recent['buy_sell'].astype(float) > 0).all()
        investment_buy = (recent['investment_buy_sell'].astype(float) > 0).all()
        score = 0
        if foreign_buy: score += 60
        if investment_buy: score += 40
        return score, foreign_buy
