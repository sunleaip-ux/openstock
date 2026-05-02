import os
from dotenv import load_dotenv
load_dotenv()
FINMIND_TOKEN = os.getenv("FINMIND_API_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LLM_MODEL = "llama3"
LLM_API_BASE = "http://localhost:11434/v1"
INDEX_CRASH_THRESHOLD = -0.02
STOCK_CRASH_THRESHOLD = -0.03
