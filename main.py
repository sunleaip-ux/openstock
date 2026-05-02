from datetime import datetime, timedelta
from core.data_collector import DataCollector
from core.technical_analyzer import TechnicalAnalyzer
from core.chip_analyzer import ChipAnalyzer
from core.fundamental_analyzer import FundamentalAnalyzer
from core.news_analyzer_pro import NewsAnalyzerPro
from engine.scoring_engine import ScoringEngine
from engine.decision_engine import DecisionEngine
from utils.notifier import Notifier
from utils.dashboard_generator import DashboardGenerator

def run_stock_picker():
    print(f"🚀 {datetime.now()} Scanning market...")
    collector = DataCollector()
    tech_anal = TechnicalAnalyzer()
    chip_anal = ChipAnalyzer()
    fund_anal = FundamentalAnalyzer()
    news_anal = NewsAnalyzerPro()
    watchlist = [{"id":"2330","name":"台積電"}, {"id":"2317","name":"鴻海"}]
    final_candidates = []
    for stock in watchlist:
        sid = stock['id']
        try:
            price_df = collector.get_price_data(sid, '2026-01-01', '2026-12-31')
            chip_df = collector.get_chip_data(sid, '2026-01-01', '2026-12-31')
            fund_df = collector.get_fundamental_data(sid)
            t_score, t_strong = tech_anal.analyze(price_df)
            c_score, c_strong = chip_anal.analyze(chip_df)
            f_score, f_strong = fund_anal.analyze(fund_df)
            news_list = news_anal.fetch_news(sid)
            n_score, n_reason, n_sentiment = news_anal.analyze_with_llm(sid, news_list)
            scores = {"technical": t_score, "chip": c_score, "fundamental": f_score, "news": n_score}
            final_score = ScoringEngine.calculate_final_score(scores)
            reasons = []
            if t_strong: reasons.append("技術面突破")
            if c_strong: reasons.append("法人買超")
            if f_strong: reasons.append("基本面強")
            final_candidates.append({"id": sid, "name": stock['name'], "score": final_score, "component_scores": [f_score, t_score, c_score, n_score], "reasons": reasons, "ai_insight": n_reason, "risk": "Normal"})
        except: pass
    filtered = DecisionEngine.filter_stocks(final_candidates)
    final_list = sorted(filtered, key=lambda x: x['score'], reverse=True)[:5]
    DashboardGenerator.generate(final_list, 'Normal')
    DashboardGenerator.deploy()
    Notifier.notify_all(final_list, f"https://sunleaip-ux.github.io/openstock/")
    print("✅ Done.")

if __name__ == '__main__': run_stock_picker()
