import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from core.data_collector import DataCollector
from core.technical_analyzer import TechnicalAnalyzer
from core.chip_analyzer import ChipAnalyzer
from core.fundamental_analyzer import FundamentalAnalyzer
from core.news_analyzer_pro import NewsAnalyzerPro
from engine.scoring_engine import ScoringEngine
from utils.dashboard_generator import DashboardGenerator
from utils.notifier import Notifier

load_dotenv()

def run_stock_picker():
    print("🚀 Starting market scan with dynamic dates...")
    collector = DataCollector()
    tech_anal = TechnicalAnalyzer()
    chip_anal = ChipAnalyzer()
    fund_anal = FundamentalAnalyzer()
    news_anal = NewsAnalyzerPro()
    
    # Dynamic Dates: Last 365 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    print(f"📅 Analysis Range: {start_date} to {end_date}")

    watchlist = [
        {"id": "2330", "name": "台積電"},
        {"id": "2454", "name": "聯發科"},
        {"id": "2317", "name": "鴻海"},
        {"id": "2388", "name": "富邦金"},
        {"id": "2881", "name": "台中商業銀行"}
    ]
    
    final_candidates = []
    for stock in watchlist:
        sid = stock["id"]
        print(f"Analyzing {stock['name']} ({sid})...")
        
        # 1. Data Collection
        price_df = collector.get_price_data(sid, start_date, end_date)
        chip_df = collector.get_chip_data(sid, start_date, end_date)
        fund_df = collector.get_fundamental_data(sid)
        
        # LOG: Check if data was actually fetched
        print(f"   - Price data: {len(price_df)} rows")
        print(f"   - Chip data: {len(chip_df)} rows")
        
        # 2. Analysis
        t_score, t_bull = tech_anal.analyze(price_df)
        c_score, c_bull = chip_anal.analyze(chip_df)
        f_score, f_bull = fund_anal.analyze(fund_df)
        
        news_list = news_anal.fetch_news(sid)
        n_score, n_reason, n_sentiment = news_anal.analyze_with_llm(sid, news_list)
        
        # 3. Scoring
        scores = {"fundamental": f_score, "technical": t_score, "chip": c_score, "news": n_score}
        final_score = ScoringEngine.calculate_final_score(scores)
        
        final_candidates.append({
            "id": sid,
            "name": stock["name"],
            "score": final_score,
            "component_scores": [f_score, t_score, c_score, n_score],
            "reasons": [f"技術面{t_score}分", f"籌碼面{c_score}分", f"基本面{f_score}分"],
            "ai_insight": n_reason,
            "risk": "Low" if final_score > 80 else "Medium"
        })

    print("Generating dashboard...")
    DashboardGenerator.generate(final_candidates, "Bullish")
    DashboardGenerator.deploy()
    
    try:
        Notifier.notify_all(final_candidates, "https://sunleaip-ux.github.io/openstock/")
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")

    print("✅ Full process completed successfully!")

if __name__ == '__main__':
    run_stock_picker()
