from flask import Flask, request
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Токен должен быть задан в Render -> Environment

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("===> NEW TELEGRAM UPDATE:")
    print(data)

    if isinstance(data, dict) and "message" in data:
        message = data["message"]
        if isinstance(message, dict) and "web_app_data" in message:
            user = message["from"]
            chat_id = message["chat"]["id"]
            payload = message["web_app_data"]["data"]

            print(f"ПОЛЬЗОВАТЕЛЬ {user['id']} прислал из WebApp: {payload}")

            # Отправляем ответ пользователю
            send_message(chat_id, f"✅ Вы отправили: {payload}")

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "✅ Render-бекенд работает, жду данные из WebApp"
