import requests
import json
from config import LLM_MODEL, LLM_API_BASE

class NewsAnalyzerPro:
    @staticmethod
    def analyze_news(sid, name, news_content):
        if not news_content or news_content == "":
            return "無足夠的新聞數據可供分析。"
        
        try:
            # Use the standard OpenAI-compatible API format for Ollama
            url = f"{LLM_API_BASE}/chat/completions"
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一位資深的量化分析師，請針對提供的個股新聞，給出簡短、專業、直接的投資洞察（50字以內）。請直接輸出結論，不要說『根據分析』等廢話。"},
                    {"role": "user", "content": f"個股：{name}({sid})\n新聞：{news_content}\n請給出投資洞察："}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"AI Analysis Error for {name}: {e}")
            return "AI分析暫時不可用"

