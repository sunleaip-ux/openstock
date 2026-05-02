import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    @staticmethod
    def analyze(df):
        try:
            # If it's a dict, convert to DF
            if isinstance(df, dict):
                df = pd.DataFrame(df)
            
            if df is None: return 0
            
            # Get prices
            if 'close' in df.columns:
                close_prices = df['close']
            elif isinstance(df, pd.DataFrame) and not df.empty:
                close_prices = df.iloc[:, -1]
            else:
                return 0
                
            if len(close_prices) < 2: return 0
            
            # Simple Trend
            ma_short = close_prices.rolling(window=5).mean().iloc[-1]
            ma_long = close_prices.rolling(window=20).mean().iloc[-1]
            trend_score = 100 if ma_short > ma_long else 0
            
            # Momentum
            momentum = ((close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]) * 100
            mom_score = 100 if momentum > 0 else 0
            
            return (trend_score + mom_score) / 2
        except Exception as e:
            print(f"Technical Analysis Error: {e}")
            return 0
