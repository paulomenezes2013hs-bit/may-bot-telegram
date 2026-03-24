from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler

TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

app = Flask(_name_)

# Criar aplicação do bot
application = ApplicationBuilder().token(TOKEN).build()

# Função de boas-vindas
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# Handler de entrada no grupo
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))

@app.route("/")
def home():
    return "Bot rodando!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

if _name_ == "_main_":
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"https://SEU-APP.onrender.com/{TOKEN}"
    )
