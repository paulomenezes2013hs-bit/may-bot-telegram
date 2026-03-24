from flask import Flask, request
import telegram

TOKEN = "COLE_SEU_TOKEN_AQUI"

bot = telegram.Bot(token=TOKEN)
app = Flask(_name_)

@app.route("/")
def home():
    return "Bot rodando!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Verificar se há uma nova pessoa entrando no grupo
    if update.message and update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            chat_id = update.message.chat.id
            # Mensagem de boas-vindas quando alguém entra no grupo
            bot.send_message(
                chat_id=chat_id,
                text="👋 Olá! Seja Bem-vindo(a) ao Grupo ✨Catálogo De Séries e Animes✨!\nEstamos aqui para poder te ajudar a encontrar sua série. Faça seu pedido e espere um Admin te atender.🇧🇷"
            )

    # Resposta normal para as mensagens
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        text = update.message.text
        bot.send_message(
            chat_id=chat_id,
            text=f"Você disse: {text}"
        )

    return "ok"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
