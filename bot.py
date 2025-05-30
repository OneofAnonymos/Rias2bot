import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
OPENROUTER_API_KEY = "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"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "تو یک دستیار هوش مصنوعی فارسی هستی. فقط به زبان فارسی محترمانه و دقیق پاسخ بده."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        output = response.json()['choices'][0]['message']['content']
    except Exception as e:
        output = "متاسفم، مشکلی در پاسخ‌گویی پیش آمده 😓"

    await update.message.reply_text(output)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من دستیار فارسی شما هستم. هر سوالی داشتی بپرس 🤖")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
