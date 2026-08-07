from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from search import search_places


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🤖 أهلاً بيك في Lead Hunter

الأوامر:

/search النشاط | المدينة | الدولة

مثال:

/search مطاعم | القاهرة | Egypt
"""

    await update.message.reply_text(text)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "مثال:\n/search مطاعم | القاهرة | Egypt"
        )
        return

    await update.message.reply_text("🔍 جاري البحث...")

    result = search_places(query)

    await update.message.reply_text(result)


def start_bot():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    print("🚀 Lead Hunter Started")

    app.run_polling()
