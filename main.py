import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters, CommandHandler

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
DONO_USERNAME = "catalogoseriesfilmes" # COLOQUE SEU USER AQUI SEM O @

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# 1. FUNÇÃO DE TESTE
async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot está ouvindo!")

# 2. BOAS-VINDAS REFORÇADA
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pega qualquer tipo de atualização de membro (entrada/saída/promoção)
    result = update.chat_member or update.my_chat_member
    if not result:
        return

    # Se o status mudou para 'member', a pessoa entrou
    if result.new_chat_member.status == "member":
        user_name = result.new_chat_member.user.first_name
        print(f"Detectada entrada de: {user_name}")
        
        await context.bot.send_message(
            chat_id=result.chat.id,
            text=f"👋 Olá {user_name}, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# 3. PAGAMENTO
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "Para liberar seu acesso, envie o comprovante de pagamento e o nome da obra no privado do dono.\n\n"
        "💰 **Pix:** `81991172344` (Toque para copiar)\n\n"
        "🍿 Aproveite!"
    )
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante no Privado", url=f"https://t.me/{DONO_USERNAME}")]]
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# REGISTROS
application.add_handler(CommandHandler("teste", teste))
# Monitora especificamente membros de chat (essencial para boas-vindas)
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

@app.route("/")
def home(): return "Bot Ativo", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(application.initialize())
        loop.run_until_complete(application.process_update(update))
    finally:
        loop.close()
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
