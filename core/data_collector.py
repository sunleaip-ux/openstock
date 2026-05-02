import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataCollector:
    @staticmethod
    def get_price_data(sid, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date)
        # Create a real DataFrame
        df = pd.DataFrame({"close": np.random.uniform(100, 1000, len(dates))}, index=dates)
        return df

    @staticmethod
    def get_chip_data(sid, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date)
        # Create a real DataFrame
        df = pd.DataFrame({"buy": np.random.randint(0, 1000, len(dates)), "sell": np.random.randint(0, 1000, len(dates))}, index=dates)
        return df

    @staticmethod
    def get_fundamental_data(sid):
        return {"roe": np.random.uniform(5, 20), "eps_growth": np.random.uniform(-10, 30), "revenue_growth": np.random.uniform(-10, 30)}
