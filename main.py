import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
DONO_USERNAME = "catalogoseriesfilmes" # COLOQUE SEU @ SEM O @

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# 1. FUNÇÃO DE BOAS-VINDAS
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member or update.my_chat_member
    if result and result.new_chat_member.status == "member":
        user_name = result.new_chat_member.user.first_name
        await context.bot.send_message(
            chat_id=result.chat.id,
            text=f"👋 Olá {user_name}, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para te ajudar. Faça seu pedido e aguarde.🇧🇷"
        )

# 2. RESPOSTA DO PIX
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "💰 **Pix:** `81991172344` (Toque para copiar)\n\n"
        "🍿 Aproveite o melhor do entretenimento!"
    )
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante", url=f"https://t.me/{DONO_USERNAME}")]]
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# REGISTROS
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

# --- A MÁGICA QUE RESOLVE O ERRO DE LOOP ---
def process_in_background(update):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(application.initialize())
        loop.run_until_complete(application.process_update(update))
    finally:
        loop.close()

@app.route("/")
def home(): return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        # CRIA UMA THREAD PARA RODAR O BOT EM SEGUNDO PLANO
        threading.Thread(target=process_in_background, args=(update,)).start()
        return "ok", 200
    return "Forbidden", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
