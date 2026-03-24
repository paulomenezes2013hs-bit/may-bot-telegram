from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Me fala qual série você quer? Um Admin, logo te responderá 👍")

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for membro in update.message.new_chat_members:
        nome = membro.first_name
        await update.message.reply_text(
            f"Olá, seja bem-vindo(a) ao Grupo ✨Catálogo Séries & Animes✨!\n"
            f"Estamos aqui para te ajudar a encontrar sua série.\n"
            f"Faça seu pedido e aguarde um Admin.\n\n"
            f"{nome} 🎉"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))

print("Bot rodando...")
app.run_polling()