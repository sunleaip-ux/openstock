import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    @staticmethod
    def analyze(df):
        if df.empty or len(df) < 60: return 0, False
        
        # 1. Calculate MA (Simple Moving Average)
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()
        
        # 2. Calculate RSI (14)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 3. Calculate MACD (12, 26, 9)
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        last_row = df.iloc[-1]
        is_bullish = (last_row['MA5'] > last_row['MA20'] > last_row['MA60'])
        rsi_ok = last_row['RSI'] < 70 if not pd.isna(last_row['RSI']) else False
        macd_cross = last_row['MACD'] > last_row['Signal'] if not pd.isna(last_row['MACD']) else False
        
        score = 0
        if is_bullish: score += 40
        if rsi_ok: score += 30
        if macd_cross: score += 30
        
        return score, (is_bullish and macd_cross)
