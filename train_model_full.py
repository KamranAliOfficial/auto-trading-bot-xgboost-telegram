import pandas as pd
import xgboost as xgb
import os

# المسارات
DATA_PATH = "training_data_nasdaq_full.csv"
MODEL_PATH = "models/xgb_model_full.json"

# تحميل البيانات
df = pd.read_csv(DATA_PATH)

# الأعمدة المطلوبة
required = ["MA10", "MA30", "Volume", "Avg_Volume", "Change", "Signal"]
if not all(col in df.columns for col in required):
    raise ValueError(f"❌ الملف لا يحتوي على الأعمدة المطلوبة: {required}")

# تنظيف وتحويل الأنواع
df = df[required].copy()
df = df.dropna()
df[required[:-1]] = df[required[:-1]].astype(float)
df["Signal"] = df["Signal"].astype(int)

# التحقق من تنوع الإشارات
if df["Signal"].nunique() < 2:
    raise ValueError("❌ البيانات تحتوي على فئة واحدة فقط من Signal (0 أو 1)، لا يمكن التدريب.")

# فصل البيانات
X = df[["MA10", "MA30", "Volume", "Avg_Volume", "Change"]]
y = df["Signal"]

# تدريب النموذج
print("🧠 جاري تدريب نموذج XGBoost ...")
model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
model.fit(X, y)

# حفظ النموذج
booster = model.get_booster()
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
booster.save_model(MODEL_PATH)

print(f"✅ تم حفظ النموذج بنجاح في {MODEL_PATH}")
