import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataCollector:
    @staticmethod
    def get_price_data(sid, start_date, end_date):
        # Simulated realistic data for testing
        dates = pd.date_range(start=start_date, end=end_date)
        df = pd.DataFrame({"date": dates, "close": np.random.uniform(100, 1000, len(dates))})
        return df.set_index("date")

    @staticmethod
    def get_chip_data(sid, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date)
        df = pd.DataFrame({"date": dates, "buy": np.random.randint(0, 1000, len(dates)), "sell": np.random.randint(0, 1000, len(dates))})
        return df.set_index("date")

    @staticmethod
    def get_fundamental_data(sid):
        return {"roe": np.random.uniform(5, 20), "eps_growth": np.random.uniform(-10, 30), "revenue_growth": np.random.uniform(-10, 30)}
