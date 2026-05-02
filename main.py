import os
import pandas as pd
import numpy as np
import requests
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
FINMIND_TOKEN = os.getenv("FINMIND_API_TOKEN")
LLM_MODEL = "llama3"
LLM_API_BASE = "http://localhost:11434/v1"

def get_score_label(score, dimension):
    if dimension == "fund":
        labels = {True: "基本面極其強勁", False: "基本面尚可", "low": "基本面需關注"}
    elif dimension == "tech":
        labels = {True: "技術趨勢強勢", False: "技術面盤整", "low": "技術面疲弱"}
    elif dimension == "chip":
        labels = {True: "籌碼面強力買入", False: "籌碼面分歧", "low": "籌碼面流出"}
    else:
        labels = {True: "表現強勢", False: "表現一般", "low": "表現較弱"}
    if score >= 70: return labels[True]
    if score >= 40: return labels[False]
    return labels["low"]

def get_price_data(sid, start, end):
    dates = pd.date_range(start=start, end=end)
    return pd.DataFrame({"close": np.random.uniform(100, 1000, len(dates))}, index=dates)

def get_chip_data(sid, start, end):
    dates = pd.date_range(start=start, end=end)
    return pd.DataFrame({"buy": np.random.randint(0, 1000, len(dates)), "sell": np.random.randint(0, 1000, len(dates))}, index=dates)

def get_fund_data(sid):
    return {"roe": np.random.uniform(5, 20), "eps_growth": np.random.uniform(-10, 30), "revenue_growth": np.random.uniform(-10, 30)}

def analyze_tech(df):
    try:
        close = df['close']
        ma_short = close.rolling(5).mean().iloc[-1]
        ma_long = close.rolling(20).mean().iloc[-1]
        return 100 if ma_short > ma_long else 0
    except: return 0

def analyze_chip(df):
    try:
        net_buy = df['buy'].sum() - df['sell'].sum()
        return 100 if net_buy > 0 else 0
    except: return 0

def analyze_fund(data):
    score = 0
    if data.get('roe', 0) > 10: score += 50
    if data.get('eps_growth', 0) > 5: score += 50
    return score

def analyze_ai(sid, name):
    try:
        url = f"{LLM_API_BASE}/chat/completions"
        payload = {"model": LLM_MODEL, "messages": [{"role": "system", "content": "你是一位專業的量化分析師。請針對個股提供簡短、精準的投資洞察（50字以內）。請務必使用繁體中文回答，直接輸出結論，不要有開場白。"}, {"role": "user", "content": f"個股：{name}({sid})\n請給出投資洞察："}] , "temperature": 0.7}
        res = requests.post(url, json=payload, timeout=10)
        return res.json()['choices'][0]['message']['content'].strip(), 70
    except: return "AI分析暫時不可用", 0

def run():
    print("🚀 Starting Market Scan...")
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    watchlist = [{"id": "2330", "name": "台積電"}, {"id": "2454", "name": "聯發科"}, {"id": "2317", "name": "鴻海"}, {"id": "2388", "name": "富邦金"}, {"id": "2881", "name": "台中商業銀行"}]
    candidates = []
    for s in watchlist:
        print(f"Analyzing {s['name']}...")
        try:
            p_df = get_price_data(s['id'], start, end)
            c_df = get_chip_data(s['id'], start, end)
            f_data = get_fund_data(s['id'])
            t_s, c_s, f_s = analyze_tech(p_df), analyze_chip(c_df), analyze_fund(f_data)
            ai_i, ai_s = analyze_ai(s['id'], s['name'])
            total = (f_s*0.3) + (t_s*0.25) + (c_s*0.25) + (ai_s*0.2)
            reasons = [get_score_label(f_s, "fund"), get_score_label(t_s, "tech"), get_score_label(c_s, "chip")]
            candidates.append({"id": s['id'], "name": s['name'], "total_score": round(total, 2), "scores": {"fundamental": f_s, "technical": t_s, "chip": c_s, "ai": ai_s}, "ai_insight": ai_i, "reasons": reasons, "risk": "Low" if total > 60 else "Medium"})
            print(f"   - Score: {total:.2f} | AI: {ai_insight[:30]}...")
        except Exception as e:
            print(f"   - ❌ Error: {e}")
    DashboardGenerator.generate(candidates, "Bullish")
    DashboardGenerator.deploy()
    print("✅ DONE!")

if __name__ == "__main__":
    run()
