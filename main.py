import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# Seu Token
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

app = Flask(__name__)

# Criar aplicação do bot
application = ApplicationBuilder().token(TOKEN).build()

# 1. Função de Boas-vindas (Entrada no Grupo)
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        print(f"Novo membro detectado no chat: {update.chat_member.chat.id}")
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá! Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# 2. NOVA FUNÇÃO: Resposta automática para mensagens de texto
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Evita que o bot responda a si mesmo ou mensagens vazias
    if not update.message or not update.message.text:
        return
        
    print(f"Mensagem recebida de {update.message.from_user.first_name}: {update.message.text}")
    
    texto_resposta = (
        "Que bom que você já tem sua Série/Anime escolhida. "
        "Favor enviar o comprovante do pagamento com o nome da sua série no privado do dono do grupo.\n\n"
        "Pix: 81991172344\n\n"
        "E aproveite todos os episódios! 🍿"
    )
    
    await update.message.reply_text(texto_resposta)

# --- REGISTRO DOS HANDLERS ---
# Monitora entrada de membros
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))

# Monitora todas as mensagens de texto (exceto comandos)
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

@app.route("/")
def home():
    return "Bot rodando com sucesso!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.create_task(application.process_update(update))
        return "ok", 200
    return "Forbidden", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
