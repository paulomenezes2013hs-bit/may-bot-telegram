import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
# IMPORTANTE: Coloque seu nome de usuário do Telegram abaixo (sem o @)
DONO_USERNAME = "SEU_USER_AQUI" 

app = Flask(__name__)

# Criar aplicação
application = ApplicationBuilder().token(TOKEN).build()

# Função de Boas-Vindas
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# Resposta de Pagamento
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "Para liberar seu acesso, envie o comprovante de pagamento e o nome da obra no privado do dono.\n\n"
        "💰 **Pix:** `81991172344` (Toque no número para copiar)\n\n"
        "🍿 Aproveite o melhor do entretenimento!"
    )
    
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante no Privado", url=f"https://t.me/{DONO_USERNAME}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

# Registro dos Handlers
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

@app.route("/")
def home():
    return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # Esta é a parte que resolve o erro "Event loop is closed"
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        
        # Cria um novo loop de eventos para cada mensagem de forma segura
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(application.initialize())
            loop.run_until_complete(application.process_update(update))
        finally:
            loop.close()
            
        return "ok", 200
    return "Forbidden", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
