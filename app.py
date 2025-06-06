from flask import Flask, request
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Получаем токен из переменных окружения (задать в Render → Environment)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

def send_message(chat_id, text):
    """Функция для отправки сообщения пользователю"""
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
        chat_id = message["chat"]["id"]
        user = message["from"]

        # ✅ Обработка команды /start и /start с параметром
        if "text" in message and message["text"].startswith("/start"):
            text = message["text"]
            if text == "/start razbor":
                send_message(chat_id, "📦 Стартуем разбор!")
            else:
                send_message(chat_id, "👋 Привет! Напиши /start razbor")

        # ✅ Обработка данных из WebApp через tg.sendData()
        elif "web_app_data" in message:
            payload = message["web_app_data"]["data"]
            print(f"ПОЛЬЗОВАТЕЛЬ {user['id']} прислал из WebApp: {payload}")
            send_message(chat_id, f"✅ Вы отправили: {payload}")

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "✅ Render-бекенд работает, жду данные из WebApp"
