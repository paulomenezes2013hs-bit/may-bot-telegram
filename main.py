from flask import Flask, request
import telegram

TOKEN = 8468549874:AAFUKgQltSmjC13ghrrpUuwHFqPEMYMof8c"
bot = telegram.Bot(token=TOKEN)

app = Flask(_name_)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        text = update.message.text
        chat_id = update.message.chat.id

        bot.send_message(chat_id=chat_id, text=f"Você disse: {text}")

    return "ok"

@app.route("/")
def home():
    return "Bot rodando!"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
