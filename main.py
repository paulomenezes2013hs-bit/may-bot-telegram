import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
DONO_USERNAME = "catalogoseriesfilmes" # COLOQUE SEU USER SEM O @

app = Flask(__name__)
bot = Bot(token=TOKEN)

async def enviar_boas_vindas(chat_id, nome):
    texto = (f"👋 Olá {nome}, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\n\n"
             "Estamos aqui para te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷")
    await bot.send_message(chat_id=chat_id, text=texto)

async def enviar_pix(chat_id):
    texto = ("✅ **Que bom que você já escolheu sua Série/Anime, manda no privado o nome!**\n\n"
             "💰 **Pix:** `81991172344` (Toque para copiar)\n\n"
             "🍿 Aproveite o melhor do entretenimento!")
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante", url=f"https://t.me/{DONO_USERNAME}")]]
    await bot.send_message(chat_id=chat_id, text=texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

@app.route("/")
def home():
    return "Bot Online", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    
    # Criar um loop apenas para esta execução específica
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # 1. Verifica entrada de novos membros
        if update.chat_member and update.chat_member.new_chat_member.status == "member":
            chat_id = update.chat_member.chat.id
            nome = update.chat_member.new_chat_member.user.first_name
            loop.run_until_complete(enviar_boas_vindas(chat_id, nome))
            
        # 2. Verifica mensagens de texto (para o Pix)
        elif update.message and update.message.text:
            chat_id = update.message.chat.id
            # Ignora comandos como /start ou /teste
            if not update.message.text.startswith('/'):
                loop.run_until_complete(enviar_pix(chat_id))
                
    except Exception as e:
        print(f"Erro no processamento: {e}")
    finally:
        loop.close()

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
