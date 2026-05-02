import requests
import pandas as pd
from config import FINMIND_TOKEN

class DataCollector:
    def __init__(self):
        self.api_url = "https://api.finmindtrade.com/api/v4/data"
        self.token = FINMIND_TOKEN

    def _fetch(self, params):
        params["token"] = self.token
        try:
            resp = requests.get(self.api_url, params=params, timeout=15)
            data = resp.json()
            if "data" in data:
                return pd.DataFrame(data["data"])
            return pd.DataFrame()
        except Exception as e:
            print(f"API Error: {e}")
            return pd.DataFrame()

    def get_price_data(self, stock_id, start_date, end_date):
        params = {"stock_id": stock_id, "start_date": start_date, "end_date": end_date}
        return self._fetch(params)

    def get_chip_data(self, stock_id, start_date, end_date):
        params = {"stock_id": stock_id, "start_date": start_date, "end_date": end_date, "data_id": "institutional_investors"}
        return self._fetch(params)

    def get_fundamental_data(self, stock_id):
        params = {"stock_id": stock_id, "data_id": "financial_statement"}
        return self._fetch(params)

    def get_current_price(self, stock_id):
        df = self.get_price_data(stock_id, '2026-01-01', '2026-12-31')
        return df.iloc[-1]['close'] if not df.empty else 0
