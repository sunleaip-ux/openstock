import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
class FinanceSync:
    def sync_trades(self):
        print("✅ Syncing trades to Google Sheets...")
        return "Synced"
