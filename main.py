from config import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


BOT_TOKEN = settings.TELEGRAM_API_TOKEN
print(BOT_TOKEN[:5])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        print("Received /start command")
        await update.message.reply_text("hello")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()