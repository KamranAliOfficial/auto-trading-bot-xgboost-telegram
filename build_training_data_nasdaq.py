# build_training_data_nasdaq.py

import pandas as pd
import yfinance as yf
import os
import time
from tqdm import tqdm

# تحميل الرموز من الملف
symbols_df = pd.read_csv("all_symbols.csv")
symbols = symbols_df["symbol"].dropna().astype(str).unique().tolist()

# ✅ تصفية الرموز الحقيقية فقط
symbols = [s for s in symbols if s.isalpha() and len(s) <= 5]

# مسار ملف الإخراج
output_file = "training_data_nasdaq_full.csv"

# إذا الملف موجود، نكمل عليه
if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    done_symbols = set(existing_df["Symbol"].unique())
    print(f"✅ استئناف: تم تحليل {len(done_symbols)} سهم سابقًا.")
else:
    existing_df = pd.DataFrame()
    done_symbols = set()

print(f"🚀 بدأ تحميل وتحليل {len(symbols)} سهم...")

# حلقة التحميل والتحليل
for symbol in tqdm(symbols, desc="📊 معالجة الأسهم"):
    if symbol in done_symbols:
        continue

    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo", interval="1d")

        if df.empty or len(df) < 30:
            continue

        df["MA10"] = df["Close"].rolling(window=10).mean()
        df["MA30"] = df["Close"].rolling(window=30).mean()
        df["Avg_Volume"] = df["Volume"].rolling(window=10).mean()
        df["Change"] = df["Close"].pct_change() * 100
        df["Future"] = df["Close"].shift(-3)
        df["Signal"] = ((df["Future"] - df["Close"]) / df["Close"] * 100 >= 5).astype(int)

        rows = []
        for i in range(len(df)):
            close = df["Close"].iloc[i]
            if pd.notna(close) and 0 < close <= 20:
                row = {
                    "Symbol": symbol,
                    "MA10": df["MA10"].iloc[i],
                    "MA30": df["MA30"].iloc[i],
                    "Volume": df["Volume"].iloc[i],
                    "Avg_Volume": df["Avg_Volume"].iloc[i],
                    "Change": df["Change"].iloc[i],
                    "Signal": df["Signal"].iloc[i]
                }
                if all(pd.notna(v) for v in row.values()):
                    rows.append(row)

        if rows:
            pd.DataFrame(rows).to_csv(output_file, mode='a', index=False, header=not os.path.exists(output_file))
            done_symbols.add(symbol)

        # ✅ تأخير بين الطلبات لتفادي الحظر
        time.sleep(0.3)

    except Exception as e:
        print(f"⚠️ خطأ في السهم {symbol}: {e}")
        continue

print("✅ تم حفظ كل البيانات في training_data_nasdaq_full.csv")
