from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from search import search_places
from exporter import export_to_csv


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🤖 أهلاً بيك في Lead Hunter

استخدم الأمر بالشكل التالي:

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

    msg = await update.message.reply_text(
        "🔍 جاري البحث..."
    )

    results = search_places(query)
    print(results)

    if not results:

        await msg.edit_text(
            "❌ لم يتم العثور على نتائج."
        )

        return

    filename = export_to_csv(results)

    await msg.edit_text(
        f"✅ تم العثور على {len(results)} نتيجة.\n\n📄 جاري إرسال الملف..."
    )

    with open(filename, "rb") as file:

        await update.message.reply_document(
            document=file,
            filename="results.csv",
            caption="📊 نتائج البحث"
        )


def start_bot():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("search", search)
    )

    print("🚀 Lead Hunter Started")

    app.run_polling()
