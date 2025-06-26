import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# راه‌اندازی لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن‌ها از محیط
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# کلاینت OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🤖 *دستیار و هوش مصنوعی آروکس* خوش‌اومدی!

Arvox یک ربات هوشمند با شخصیت شوخ‌طبع و پاسخگو به تمام سوالات شماست.
- پشتیبانی از زبان فارسی
- تولید پاسخ متنی با GPT
- پاسخ به سوالات علمی، عمومی، شخصی
- و قابلیت‌های آینده مثل: ساخت تصویر، تبدیل متن به ویس و پشتیبانی از صدا

✨ *برنامه دستیار هوشمند آروکس به‌زودی منتشر خواهد شد...*
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# پردازش پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ خطا در ارتباط با OpenAI: {e}")
        reply = "❌ متاسفم، مشکلی پیش اومد هنگام ارتباط با هوش مصنوعی."

    await update.message.reply_text(reply)

# اجرای ربات
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
