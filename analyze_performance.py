import os
import json
from datetime import datetime
import yfinance as yf

def generate_report_summary():
    path = "data/trade_history.json"
    if not os.path.exists(path):
        return "❌ لا يوجد سجل توصيات."

    with open(path, "r", encoding="utf-8") as f:
        history = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    today_trades = [x for x in history if x["timestamp"].startswith(today)]

    if not today_trades:
        return "❌ لا توجد توصيات تم إرسالها اليوم."

    categories = {
        "top": "📁 Top Stocks:",
        "watchlist": "📁 Watchlist:",
        "pump": "📁 Pump Stocks:"
    }

    report_by_cat = {k: [] for k in categories}

    for trade in today_trades:
        symbol = trade["symbol"]
        entry = float(trade["entry_price"])
        score = float(trade["score"])
        timestamp = trade["timestamp"]

        # تصنيف الفئة بدقة
        raw_cat = trade.get("category", "").strip().lower()
        if "top" in raw_cat:
            category = "top"
        elif "watch" in raw_cat:
            category = "watchlist"
        elif "pump" in raw_cat:
            category = "pump"
        else:
            category = "unknown"

        # حساب الأهداف ووقف الخسارة
        target1 = round(entry * 1.1, 2)
        target2 = round(entry * 1.25, 2)
        stop_loss = round(entry * 0.85, 2)

        # السعر الحالي
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            current_price = round(hist.iloc[-1]["Close"], 2) if not hist.empty else entry
        except:
            current_price = entry

        # الحالة النهائية
        status = "✅ الحالة: أرباح محققة" if current_price >= target1 else "❌ الحالة: لم يحقق أرباح"
        target1_hit = "✅ تحقق" if current_price >= target1 else "❌ لم يتحقق"
        target2_hit = "✅ تحقق" if current_price >= target2 else "❌ لم يتحقق"

        msg = f"""
{status}
📈 {symbol}
📅 تاريخ التوصية: {timestamp}
💰 سعر الدخول: {entry}
📈 السعر الحالي: {current_price}
🎯 الهدف 1: {target1} {target1_hit}
🏁 الهدف 2: {target2} {target2_hit}
🛑 وقف الخسارة: {stop_loss}
📊 نسبة النجاح: {score:.2f}%
""".strip()

        if category in report_by_cat:
            report_by_cat[category].append(msg)

    final_report = f"📊 تقرير أداء يوم {today}:\n\n"
    for cat_key, cat_title in categories.items():
        final_report += f"{cat_title}\n\n"
        if report_by_cat[cat_key]:
            final_report += "\n\n".join(report_by_cat[cat_key]) + "\n\n"
        else:
            final_report += "❌ لا توجد توصيات في هذه الفئة.\n\n"

    return final_report.strip()
