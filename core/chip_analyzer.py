import pandas as pd

class ChipAnalyzer:
    @staticmethod
    def analyze(df):
        if df.empty or len(df) < 5: return 0, False
        
        # Support both real (buy_sell) and simulated (institutional_buy) columns
        if 'buy_sell' in df.columns:
            recent = df.tail(5)
            is_bullish = (recent['buy_sell'].astype(float) > 0).all()
            score = 100 if is_bullish else 50
        elif 'institutional_buy' in df.columns:
            recent = df.tail(5)
            is_bullish = (recent['institutional_buy'] > recent['institutional_sell']).all()
            score = 100 if is_bullish else 50
        else:
            score, is_bullish = 0, False
            
        return score, is_bullish
