import requests
from config import LLM_MODEL, LLM_API_BASE

class NewsAnalyzerPro:
    @staticmethod
    def analyze(sid, name):
        try:
            url = f"{LLM_API_BASE}/chat/completions"
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一位專業的量化分析師。請針對個股提供簡短、精準的投資洞察（50字以內）。請務必使用繁體中文回答，直接輸出結論，不要有開場白。"},
                    {"role": "user", "content": f"個股：{name}({sid})\n請給出投資洞察："}
                ],
                "temperature": 0.7
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip(), 70
        except Exception as e:
            print(f"AI Error for {sid}: {e}")
            return "AI分析暫時不可用", 0
