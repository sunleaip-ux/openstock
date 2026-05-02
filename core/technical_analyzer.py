import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    @staticmethod
    def analyze(df):
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            return 0
        try:
            # Use basic calculations to avoid any dependency errors
            close_prices = df['close'] if 'close' in df.columns else df.iloc[:, -1]
            if len(close_prices) < 2: return 0
            
            # Simple Moving Average Trend
            ma_short = close_prices.rolling(window=5).mean().iloc[-1]
            ma_long = close_prices.rolling(window=20).mean().iloc[-1]
            trend_score = 100 if ma_short > ma_long else 0
            
            # Price Momentum
            momentum = ((close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]) * 100
            mom_score = 100 if momentum > 0 else 0
            
            return (trend_score + mom_score) / 2
        except Exception as e:
            print(f"Technical Analysis Error: {e}")
            return 0
