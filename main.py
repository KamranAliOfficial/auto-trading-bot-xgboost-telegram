import os
import json
import logging
import asyncio
import schedule
import yfinance as yf
import requests
import nest_asyncio
import shutil
from datetime import datetime, timedelta, timezone
from modules.auto_trader import scheduled_tasks
from modules.auto_trader import IBKRConnection
from modules.auto_trader import close_all_positions_before_market_close


ib_connection: IBKRConnection = IBKRConnection()

from telegram import Bot
from modules.analyze_performance import generate_report_summary
from modules.tv_data import (
    fetch_stocks_from_tradingview,
    analyze_single_stock,
    analyze_market
)
from modules.tv_data import analyze_high_movement_stocks
from modules.notifier import send_telegram_message
from modules.auto_trader import send_pnl_summary
import schedule
import asyncio
from modules.ml_model import train_model_daily
from modules.symbols_updater import fetch_all_us_symbols, save_symbols_to_csv
from modules.telegram_bot import start_telegram_bot
from modules.notifier import notify_new_stock, compare_stock_lists_and_alert, check_cross_list_movements
from modules.pump_detector import detect_pump_stocks
from modules.price_tracker import check_targets, clean_old_trades
#from modules.auto_trader import close_all_positions_before_market_close  # تأكد من استيرادها

nest_asyncio.apply()

NEWS_API_KEY = "BpXXFMPQ3JdCinpg81kfn4ohvmnhGZOwEmHjLIre"
POSITIVE_NEWS_FILE = "data/positive_watchlist.json"
BOT_TOKEN = "7994128773:AAEnoWDCi33KxYGaEaLKjm3zGq8SSI7fwN8"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    print(msg)
    logging.info(msg)
import pytz
from datetime import datetime, timezone, timedelta
from modules.auto_trader import log_action  # يمكن استخدام نفس نظام التسجيل

def is_market_open() -> bool:
    """
    تحقق إذا كان السوق الأمريكي مفتوحًا (9:30 AM - 4 PM بتوقيت نيويورك).
    تُستبدل الدالة القديمة التي كانت تستخدم UTC+3.
    """
    ny_tz = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_tz)
    
    if ny_time.weekday() >= 5:  # السوق مغلق في عطلة نهاية الأسبوع
        return False
    
    market_open = (9, 30)  # 9:30 AM
    market_close = (16, 0)  # 4:00 PM
    
    current_time = (ny_time.hour, ny_time.minute)
    return market_open <= current_time < market_close

def is_market_weak() -> bool:
    """
    تحقق إذا كان السوق ضعيفًا (انخفاض SPY بأكثر من 1%).
    تبقى كما هي لأنها لا تعتمد على التوقيت المحلي.
    """
    try:
        spy = yf.Ticker("SPY")
        hist = spy.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist["Close"].iloc[-2]
            today_close = hist["Close"].iloc[-1]
            change_pct = (today_close - prev_close) / prev_close * 100
            return change_pct < -1
    except Exception as e:
        log_action(f"❌ خطأ في تحليل SPY: {e}", "error")
    return False

def fetch_news_sentiment(symbol):
    try:
        url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("data", [])
            for article in articles:
                title = article.get("title", "").lower()
                if "bankruptcy" in title or "dilution" in title:
                    return "negative"
                if "record revenue" in title or "strong earnings" in title:
                    return "positive"
        return "neutral"
    except Exception as e:
        log(f"❌ خطأ في تحليل الأخبار لـ {symbol}: {e}")
        return "neutral"

def watch_positive_news_stocks():
    log("🟢 فحص الأسهم ذات الأخبار الإيجابية...")
    try:
        stocks = fetch_stocks_from_tradingview()
        positive_stocks = []

        old_symbols = []
        if os.path.exists(POSITIVE_NEWS_FILE):
            with open(POSITIVE_NEWS_FILE, "r", encoding="utf-8") as f:
                old_list = json.load(f)
            old_symbols = [s["symbol"] for s in old_list]

        for stock in stocks:
            symbol = stock["symbol"]
            sentiment = fetch_news_sentiment(symbol)
            if sentiment == "positive" and symbol not in old_symbols:
                message = f"📢 سهم جديد بأخبار إيجابية:\n📈 {symbol}\n✅ تم رصده في السوق"
                send_telegram_message(message)
                positive_stocks.append(stock)

        if positive_stocks:
            os.makedirs(os.path.dirname(POSITIVE_NEWS_FILE), exist_ok=True)
            with open(POSITIVE_NEWS_FILE, "w", encoding="utf-8") as f:
                json.dump(positive_stocks, f, indent=2, ensure_ascii=False)
            log(f"✅ تم حفظ {len(positive_stocks)} سهم في قائمة الأخبار الإيجابية.")
        else:
            log("⚠️ لا توجد أسهم إيجابية حالياً.")
    except Exception as e:
        log(f"❌ فشل في مراقبة الأخبار الإيجابية: {e}")

async def update_market_data(bot):
    if not is_market_open():
        log("⏸️ السوق مغلق - إلغاء التحديث")
        return

    log("📊 تحليل وتحديث السوق...")
    try:
        if os.path.exists("data/top_stocks.json"):
            shutil.copy("data/top_stocks.json", "data/top_stocks_old.json")
        if os.path.exists("data/pump_stocks.json"):
            shutil.copy("data/pump_stocks.json", "data/pump_stocks_old.json")
        if os.path.exists("data/high_movement_stocks.json"):
            shutil.copy("data/high_movement_stocks.json", "data/high_movement_stocks_old.json")

        await analyze_market()
        log("✅ تم تحليل السوق بنجاح.")

        compare_stock_lists_and_alert("data/top_stocks_old.json", "data/top_stocks.json", "🌀 سهم قوي جديد:")
        await check_cross_list_movements(bot)

    except Exception as e:
        log(f"❌ فشل تحليل السوق: {e}")

async def update_symbols():
    log("🔁 تحديث رموز السوق...")
    try:
        symbols = fetch_all_us_symbols()
        if symbols:
            save_symbols_to_csv(symbols)
            log(f"✅ تم تحديث {len(symbols)} رمز سوق.")
    except Exception as e:
        log(f"❌ فشل تحديث الرموز: {e}")

async def update_pump_stocks():
    if not is_market_open():
        return
    log("💣 تحليل الانفجارات السعرية...")
    try:
        if os.path.exists("data/pump_stocks.json"):
            shutil.copy("data/pump_stocks.json", "data/pump_stocks_old.json")
        detect_pump_stocks()
        log("✅ تم تحديث أسهم الانفجار.")

        compare_stock_lists_and_alert("data/pump_stocks_old.json", "data/pump_stocks.json", "💥 سهم انفجاري جديد:")
    except Exception as e:
        log(f"❌ فشل تحليل الانفجارات: {e}")

async def update_high_movement_stocks():
    if not is_market_open():
        return
    log("🚀 تحليل الأسهم ذات الحركة العالية...")
    try:
        if os.path.exists("data/high_movement_stocks.json"):
            shutil.copy("data/high_movement_stocks.json", "data/high_movement_stocks_old.json")
        await asyncio.to_thread(analyze_high_movement_stocks)
        log("✅ تم تحديث أسهم الحركة العالية.")

        compare_stock_lists_and_alert("data/high_movement_stocks_old.json", "data/high_movement_stocks.json", "🚀 سهم نشط جديد:")
    except Exception as e:
        log(f"❌ فشل تحليل الأسهم ذات الحركة العالية: {e}")

async def track_targets(bot):
    log("🎯 متابعة لحظية للأسهم...")
    try:
        await check_targets(bot)
    except Exception as e:
        log(f"❌ خطأ في متابعة الأهداف: {e}")

async def send_daily_report_task():
    if is_market_open():
        log("⏸️ السوق مفتوح - تأجيل إرسال التقرير")
        return
    await generate_report_summary()

async def clean_trade_history_task():
    clean_old_trades()

async def daily_model_training():
    log("🔁 تدريب يومي للنموذج الذكي...")
    try:
        train_model_daily()
        log("✅ تم تدريب النموذج اليومي بنجاح.")
    except Exception as e:
        log(f"❌ فشل تدريب النموذج: {e}")

async def main():
    bot_instance = Bot(token=BOT_TOKEN)
    
    asyncio.create_task(scheduled_tasks(bot_instance))

    await daily_model_training()
    await update_market_data(bot_instance)
    await update_pump_stocks()
    await update_high_movement_stocks()
    
    schedule.every().day.at("00:00").do(lambda: asyncio.create_task(daily_model_training()))
    schedule.every().day.at("03:00").do(lambda: asyncio.create_task(update_symbols()))
    schedule.every(5).minutes.do(lambda: asyncio.create_task(update_market_data(bot_instance)))
    schedule.every(5).minutes.do(lambda: asyncio.create_task(update_pump_stocks()))
    schedule.every(5).minutes.do(lambda: asyncio.create_task(update_high_movement_stocks()))
    schedule.every(5).minutes.do(lambda: asyncio.create_task(track_targets(bot_instance)))
    schedule.every(10).minutes.do(watch_positive_news_stocks)
    schedule.every().day.at("20:00").do(lambda: asyncio.create_task(send_daily_report_task()))
    schedule.every().day.at("00:05").do(lambda: asyncio.create_task(clean_trade_history_task())) # داخل دالة main():
    schedule.every(15).minutes.do(lambda: asyncio.create_task(send_pnl_summary(bot_instance)))
    schedule.every().day.at("15:50").do(lambda: asyncio.create_task(close_all_positions_before_market_close(bot_instance)))
    schedule.every(1).minutes.do(lambda: asyncio.run(verify_active_stop_orders()))



    
    async def keep_running_schedules():
        while True:
            schedule.run_pending()
            await asyncio.sleep(30)

    await asyncio.gather(
        start_telegram_bot(),
        keep_running_schedules()
    )

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
