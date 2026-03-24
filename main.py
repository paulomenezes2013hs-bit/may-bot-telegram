import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler
import asyncio

# Substitua pelo seu Token real (mantenha as aspas)
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

app = Flask(__name__)

# Criar aplicação do bot (v20+ do python-telegram-bot)
application = ApplicationBuilder().token(TOKEN).build()

# Função de boas-vindas
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica se há um novo membro no chat
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# Handler de entrada no grupo
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))

@app.route("/")
def home():
    return "Bot rodando!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        # Usamos create_task para processar sem travar a resposta do Flask
        asyncio.create_task(application.process_update(update))
        return "ok", 200
    return "Forbidden", 403

# Ponto de entrada corrigido
if __name__ == "__main__":
    # O Render define a porta automaticamente na variável PORT
    port = int(os.environ.get("PORT", 10000))
    
    # IMPORTANTE: No Render, usamos o Flask para ouvir a porta, 
    # e o Telegram envia as mensagens para a rota do Webhook.
    app.run(host="0.0.0.0", port=port)
