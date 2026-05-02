import requests
from config import LLM_MODEL, LLM_API_BASE

class NewsAnalyzerPro:
    @staticmethod
    def analyze(sid, name):
        # Simulated news fetch
        news_content = f"{name}({sid})近期在AI晶片需求增加與產能擴張方面有積極表現。"
        try:
            url = f"{LLM_API_BASE}/chat/completions"
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一位資深的量化分析師，請針對個股給出簡短、專業的投資洞察（50字以內）。"},
                    {"role": "user", "content": f"個股：{name}({sid})\n最新消息：{news_content}\n請給出投資洞察："}
                ],
                "temperature": 0.7
            }
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip(), 75
        except Exception as e:
            print(f"AI Error for {sid}: {e}")
            return "AI分析暫時不可用", 0
