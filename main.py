import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler, MessageHandler, filters, CommandHandler

# --- CONFIGURAÇÕES ---
TOKEN = "8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
# Coloque seu @ do Telegram aqui (sem o @) para o botão de comprovante funcionar
DONO_USERNAME = "catalogoseriesfilmes" 

app = Flask(__name__)

# Criar a aplicação do bot
application = ApplicationBuilder().token(TOKEN).build()

# 1. COMANDO DE TESTE (Para conferir se o bot está vivo)
async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ O bot está online e funcionando!")

# 2. FUNÇÃO DE BOAS-VINDAS (Ativada quando alguém entra no grupo)
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pega os dados de quem entrou
    result = update.chat_member or update.my_chat_member
    if not result:
        return

    # Se o novo status for 'member', a pessoa acabou de entrar
    if result.new_chat_member.status == "member":
        user_name = result.new_chat_member.user.first_name
        print(f"--- LOG: Enviando boas-vindas para {user_name} ---")
        
        await context.bot.send_message(
            chat_id=result.chat.id,
            text=(
                f"👋 Olá {user_name}, Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\n\n"
                "Estamos aqui para poder te ajudar a encontrar sua série. "
                "Faça seu pedido e espere um Admin te atender.🇧🇷"
            )
        )

# 3. RESPOSTA AUTOMÁTICA COM PIX (Para qualquer mensagem de texto)
async def responder_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    texto = (
        "✅ **Que bom que você já escolheu sua Série/Anime!**\n\n"
        "Para liberar seu acesso, envie o comprovante de pagamento e o nome da obra no privado do dono.\n\n"
        "💰 **Pix:** `81991172344` (Toque no número para copiar)\n\n"
        "🍿 Aproveite o melhor do entretenimento!"
    )
    
    # Botão para o seu privado
    keyboard = [[InlineKeyboardButton("📩 Enviar Comprovante no Privado", url=f"https://t.me/{DONO_USERNAME}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

# --- REGISTRO DE COMANDOS E EVENTOS ---
application.add_handler(CommandHandler("teste", teste))
application.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_pagamento))

# --- ROTAS DO SERVIDOR FLASK ---
@app.route("/")
def home():
    return "Bot Online!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Esta função resolve o erro 'Event loop is closed'"""
    if request.method == "POST":
        # Pega a mensagem vinda do Telegram
        update = Update.de_json(request.get_json(force=True), application.bot)
        
        # Cria um novo loop de eventos (A solução para o erro do Render)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Inicializa e processa
            loop.run_until_complete(application.initialize())
            loop.run_until_complete(application.process_update(update))
        except Exception as e:
            print(f"Erro no processamento: {e}")
        finally:
            loop.close()
            
        return "ok", 200
    return "Forbidden", 403

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
