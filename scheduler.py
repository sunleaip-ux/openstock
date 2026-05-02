from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from main import run_stock_picker
from utils.market_sentry import MarketSentry
from config import TIMEZONE, SENTRY_INTERVAL_MINUTES
import time

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    sentry = MarketSentry()
    scheduler.add_job(run_stock_picker, trigger=CronTrigger(hour=8, minute=30), id='daily_scan')
    scheduler.add_job(sentry.run_sentry_cycle, trigger=IntervalTrigger(minutes=SENTRY_INTERVAL_MINUTES), id='market_sentry')
    scheduler.start()
    print("📅 Scheduler started.")

if __name__ == '__main__':
    start_scheduler()
    while True: time.sleep(1)
