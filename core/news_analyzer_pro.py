import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

class NewsAnalyzerPro:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        self.model_name = "llama3"
    def fetch_news(self, stock_id):
        url = f"https://news.google.com/rss/search?q={stock_id}+台股&hl=zh-TW&gl=TW"
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.content, 'xml')
            items = soup.find_all('item')
            return [{"title": item.title.text} for item in items[:5]]
        except: return []
    def analyze_with_llm(self, stock_id, news_list):
        if not news_list: return 50, "無可用新聞", "Neutral"
        news_text = "\n".join([f"- {n['title']}" for n in news_list])
        prompt = f"分析股票 {stock_id} 的新聞：\n{news_text}\n請輸出JSON: {{'sentiment_score': 0-100, 'reasoning': '...', 'sentiment': 'Positive/Negative/Neutral'}}"
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            res_json = json.loads(response.choices[0].message.content)
            return res_json["sentiment_score"], res_json["reasoning"], res_json["sentiment"]
        except: return 50, "AI分析暫時不可用", "Neutral"
