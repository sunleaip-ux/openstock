import requests
import json
from config import LLM_MODEL, LLM_API_BASE

class NewsAnalyzerPro:
    @staticmethod
    def fetch_news(sid):
        # Since we are in test mode, we return a realistic simulated news string
        # In production, this would call a News API
        return f"近期關於{sid}的市場分析顯示其在AI領域具備強大的競爭力，產能持續擴張。"

    @staticmethod
    def analyze_news(sid, name, news_content):
        if not news_content or news_content == "":
            return "無足夠的新聞數據可供分析。"
        try:
            url = f"{LLM_API_BASE}/chat/completions"
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一位資深的量化分析師，請針對提供的個股新聞，給出簡短、專業、直接的投資洞察（50字以內）。"},
                    {"role": "user", "content": f"個股：{name}({sid})\n新聞：{news_content}\n請給出投資洞察："}
                ],
                "temperature": 0.7
            }
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"AI Analysis Error for {sid}: {e}")
            return "AI分析暫時不可用"
