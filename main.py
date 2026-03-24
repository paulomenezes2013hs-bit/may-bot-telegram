import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
DONO_USERNAME = "catalogoseriesfilmes" # COLOQUE SEU USER DO TELEGRAM SEM O @

app = Flask(__name__)
# Criamos apenas o objeto do Bot, sem a "Application" pesada
import telegram
bot = telegram.Bot(token=TOKEN)

# 1. FUNÇÃO DE RESPOSTA (Boas-vindas e Pix)
async def processar_evento(update_data):
    update = Update.de_json(update_data, bot)
    
    # Se for entrada de novo membro
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        chat_id = update.chat_member.chat.id
        nome = update.chat_member.new_chat_member.user.first_name
        texto = f"👋 Olá {nome}, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para te ajudar. Faça seu pedido e aguarde.🇧🇷"
        await bot.send_message(chat_id=chat_id, text=texto)

    # Se for mensagem de texto comum
    elif update.message and update.message.text:
        chat_id = update.message.chat.id
        texto_pix = (
            "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
            "💰 **Pix:** `81991172344` (Toque para copiar)\n\n"
            "🍿 Aproveite o melhor do entretenimento!"
        )
        keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante", url=f"https://t.me/{DONO_USERNAME}")]]
        await bot.send_message(chat_id=chat_id, text=texto_pix, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# --- ROTAS DO RENDER ---
@app.route("/")
def home(): return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # Esta é a parte que resolve o erro de uma vez por todas:
    # Criamos um loop novo só para essa mensagem e fechamos logo depois.
    dados = request.get_json(force=True)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(processar_evento(dados))
    finally:
        loop.close()
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
