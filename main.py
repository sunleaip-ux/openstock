import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from core.data_collector import DataCollector
from core.technical_analyzer import TechnicalAnalyzer
from core.chip_analyzer import ChipAnalyzer
from core.fundamental_analyzer import FundamentalAnalyzer
from core.news_analyzer_pro import NewsAnalyzerPro
from utils.dashboard_generator import DashboardGenerator
from utils.notifier import Notifier

load_dotenv()

def run_stock_picker():
    print("🚀 Starting market scan...")
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    watchlist = [{"id": "2330", "name": "台積電"}, {"id": "2454", "name": "聯發科"}, {"id": "2317", "name": "鴻海"}, {"id": "2388", "name": "富邦金"}, {"id": "2881", "name": "台中商業銀行"}]
    final_candidates = []
    for stock in watchlist:
        sid, name = stock['id'], stock['name']
        print(f"Analyzing {name} ({sid})...")
        try:
            price_df = DataCollector.get_price_data(sid, start_date, end_date)
            chip_df = DataCollector.get_chip_data(sid, start_date, end_date)
            fund_data = DataCollector.get_fundamental_data(sid)
            tech_score = TechnicalAnalyzer.analyze(price_df)
            chip_score = ChipAnalyzer.analyze(chip_df)
            fund_score = FundamentalAnalyzer.analyze(fund_data)
            ai_insight, ai_score = NewsAnalyzerPro.analyze(sid, name)
            total_score = (fund_score * 0.3) + (tech_score * 0.25) + (chip_score * 0.25) + (ai_score * 0.2)
            final_candidates.append({"id": sid, "name": name, "total_score": round(total_score, 2), "scores": {"fundamental": fund_score, "technical": tech_score, "chip": chip_score, "ai": ai_score}, "ai_insight": ai_insight})
            print(f"   - Score: {total_score:.2f} | AI: {ai_insight[:30]}...")
        except Exception as e:
            print(f"   - ❌ Error: {e}")
    DashboardGenerator.generate(final_candidates, "Bullish")
    DashboardGenerator.deploy()
    Notifier.send_summary(final_candidates)
    print("✅ Full process completed successfully!")

if __name__ == "__main__":
    run_stock_picker()
