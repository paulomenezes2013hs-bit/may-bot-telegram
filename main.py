import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
# IMPORTANTE: Coloque seu nome de usuário do Telegram abaixo (sem o @)
DONO_USERNAME = "catalogoseriesfilmes" 

app = Flask(__name__)

# Criar aplicação
application = ApplicationBuilder().token(TOKEN).build()

# 1. FUNÇÃO DE BOAS-VINDAS (Sempre que entrar no grupo)
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verificamos se houve uma atualização de membro de chat
    result = update.chat_member
    if not result:
        return

    # Se o novo status for 'member', a pessoa acabou de entrar (ou voltar)
    if result.new_chat_member.status == "member":
        print(f"Usuário {result.from_user.first_name} entrou no grupo.")
        await context.bot.send_message(
            chat_id=result.chat.id,
            text="👋 Olá, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
        )

# 2. RESPOSTA DE PAGAMENTO COM BOTÃO
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

# --- REGISTRO DOS HANDLERS ---
# ChatMemberHandler monitora entradas e saídas
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
# MessageHandler monitora conversas
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

@app.route("/")
def home():
    return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        
        # Cria um novo loop para evitar o erro 'Event loop is closed'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(application.initialize())
            loop.run_until_complete(application.process_update(update))
        except Exception as e:
            print(f"Erro ao processar: {e}")
        finally:
            loop.close()
            
        return "ok", 200
    return "Forbidden", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
