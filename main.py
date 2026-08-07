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
        await update.message.reply_text("اكتب مثلا:\n/search مطاعم القاهرة")
        return

    await update.message.reply_text("🔍 جاري البحث...")

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "Telegram Leads Bot"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        await update.message.reply_text("حدث خطأ أثناء البحث.")
        return

    data = response.json()

    if not data:
        await update.message.reply_text("❌ لم يتم العثور على نتائج.")
        return

    text = "📍 النتائج:\n\n"

    for i, place in enumerate(data, 1):
        text += f"{i}- {place['display_name']}\n"
        text += f"https://www.google.com/maps?q={place['lat']},{place['lon']}\n\n"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

print("🚀 Telegram Bot Started")

app.run_polling()
