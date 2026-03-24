import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# Configurações
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
# Substitua pelo seu @ de usuário (sem o @) para o botão de contato
DONO_USERNAME = "SEU_USER_AQUI" 

app = Flask(__name__)

# Criar aplicação
application = ApplicationBuilder().token(TOKEN).build()

# 1. Função de Boas-vindas
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# 2. Resposta de Pagamento com Botão
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    # Texto da resposta formatado
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "Para liberar seu acesso, envie o comprovante de pagamento e o nome da obra no privado do dono.\n\n"
        "💰 **Pix:** `81991172344` (Toque para copiar)\n\n"
        "🍿 Aproveite o melhor do entretenimento!"
    )
    
    # Criando o botão para o privado
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante no Privado", url=f"https://t.me/{DONO_USERNAME}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

# Handlers
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

@app.route("/")
def home():
    return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.create_task(application.process_update(update))
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
