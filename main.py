import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"

# IMPORTANTE: Mude 'SEU_USER_AQUI' para o seu @ do Telegram (sem o @)
# Exemplo: DONO_USERNAME = "MaySeries"
DONO_USERNAME = "catalogoseriesfilmes" 

app = Flask(__name__)

# Criar aplicação do Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Variável para controlar se o bot já foi iniciado
initialized = False

# 1. FUNÇÃO DE BOAS-VINDAS
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member and update.chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# 2. RESPOSTA AUTOMÁTICA COM BOTÃO PIX
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "Para liberar seu acesso, envie o comprovante de pagamento e o nome da obra no privado do dono.\n\n"
        "💰 **Pix:** `81991172344` (Toque no número para copiar)\n\n"
        " popcorn Aproveite o melhor do entretenimento!"
    )
    
    # Botão que leva para o seu privado
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante no Privado", url=f"https://t.me/{DONO_USERNAME}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

# --- REGISTRO DE FUNÇÕES ---
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

# --- ROTAS DO FLASK ---
@app.route("/")
def home():
    return "Bot Online e Operacional!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    global initialized
    if request.method == "POST":
        try:
            # Inicializa o bot se ainda não estiver ligado
            if not initialized:
                await application.initialize()
                await application.start()
                initialized = True
            
            # Recebe e processa a atualização do Telegram
            update = Update.de_json(request.get_json(force=True), application.bot)
            asyncio.create_task(application.process_update(update))
            return "ok", 200
        except Exception as e:
            print(f"Erro no processamento: {e}")
            return "error", 500
    return "Forbidden", 403

# --- INICIALIZAÇÃO DO SERVIDOR ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # Host 0.0.0.0 é obrigatório para o Render
    app.run(host="0.0.0.0", port=port)
