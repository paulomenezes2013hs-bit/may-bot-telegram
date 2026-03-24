from flask import Flask
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot rodando!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot funcionando!")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()

    import os
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)
