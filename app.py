from flask import Flask, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("===> NEW TELEGRAM UPDATE:")
    print(data)

    if isinstance(data, dict) and "message" in data:
        message = data["message"]
        if isinstance(message, dict) and "web_app_data" in message:
            user = message["from"]
            payload = message["web_app_data"]["data"]
            print(f"ПОЛЬЗОВАТЕЛЬ {user['id']} прислал из WebApp: {payload}")

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "✅ Render-бекенд работает, жду данные из WebApp"
