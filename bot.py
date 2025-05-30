import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ✅ توکن‌ها
TELEGRAM_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
HF_API_TOKEN = "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"

# 📡 آدرس مدل GPT2 فارسی
API_URL = "https://api-inference.huggingface.co/models/HooshvareLab/gpt2-fa"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# 🧠 دریافت و ارسال پاسخ از مدل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    payload = {"inputs": user_input}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        output = response.json()[0]["generated_text"]
    except Exception as e:
        output = "متاسفم، نتونستم پاسخ بدم. دوباره تلاش کن."

    await update.message.reply_text(output)

# 👋 پیام شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من یه ربات هوش مصنوعی فارسی هستم. ازم سوال بپرس 😊")

# 🏃 اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات در حال اجراست...")
    app.run_polling()
