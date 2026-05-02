import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self):
        pass

    def get_price_data(self, stock_id, start_date, end_date):
        # Create simulated price data for testing visual effects
        dates = pd.date_range(start=start_date, end=end_date)
        np.random.seed(int(stock_id)) # Consistent randomness
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
        df = pd.DataFrame({"close": prices, "open": prices*0.99, "high": prices*1.01, "low": prices*0.98, "volume": np.random.randint(1000, 10000, len(dates))}, index=dates)
        df.index.name = "date"
        return df.reset_index()

    def get_chip_data(self, stock_id, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date)
        np.random.seed(int(stock_id) + 1)
        df = pd.DataFrame({
            "date": dates,
            "institutional_buy": np.random.randint(100, 1000, len(dates)),
            "institutional_sell": np.random.randint(100, 1000, len(dates))
        })
        return df

    def get_fundamental_data(self, stock_id):
        np.random.seed(int(stock_id) + 2)
        return pd.DataFrame([{
            "roe": np.random.uniform(5, 25),
            "eps": np.random.uniform(2, 20),
            "revenue_growth": np.random.uniform(-0.1, 0.3)
        }])

    def get_current_price(self, stock_id):
        return 100.0
