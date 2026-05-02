import requests
from config import LINE_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
class Notifier:
    @staticmethod
    def send_line(message):
        if not LINE_TOKEN: return
        requests.post("https://notify-api.line.me/api/notify", headers={"Authorization": f"Bearer {LINE_TOKEN}"}, data={"message": message})
    @staticmethod
    def send_telegram(message):
        if not TELEGRAM_TOKEN: return
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
    @classmethod
    def notify_all(cls, recommended_stocks, url=None):
        msg = "📈 今日 AI 選股推薦\n\n" if recommended_stocks else "📉 今日無推薦標的"
        for i, s in enumerate(recommended_stocks, 1):
            msg += f"{i}️⃣ {s['name']} ({s['id']})\n分數：{s['score']}\n原因：\n- " + "\n- ".join(s['reasons']) + "\n風險：{s['risk']}\n---\n"
        if url: msg += f"\n🔗 儀表板：{url}"
        cls.send_line(msg)
        cls.send_telegram(msg)
