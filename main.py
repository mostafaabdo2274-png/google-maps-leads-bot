
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ البوت شغال.\n\n"
        "اكتب:\n"
        "/search مطاعم القاهرة"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("اكتب:\n/search مطاعم القاهرة")
        return

    await update.message.reply_text(
        f"🔍 جاري البحث عن:\n{query}\n\n"
        "⚠️ مرحلة التجهيز... هيتم إضافة جلب النتائج في الخطوة القادمة."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

print("🚀 Telegram Bot Started")

app.run_polling()،
