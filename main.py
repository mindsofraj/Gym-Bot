import asyncio
import os
from flask import Flask
from telegram import Bot
from telegram.error import TelegramError
from telegram.request import HTTPXRequest 

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

app = Flask(__name__)

async def send_daily_poll():
    try:
        # Create a fresh HTTP session for each run
        req = HTTPXRequest(
            connection_pool_size=1,
            pool_timeout=10,
            read_timeout=30
        )
        bot = Bot(token=BOT_TOKEN, request=req)

        await bot.send_poll(
            chat_id=int(CHAT_ID),
            question="Who's coming to the gym today?",
            options=["Yes 💪", "No ❌", "Maybe 🤔"],
            is_anonymous=False
        )
        print("✅ Poll sent successfully!")
    except TelegramError as e:
        print("⚠️ Telegram error:", e)
    except Exception as e:
        print("❌ Unexpected error:", e)

@app.route("/")
def home():
    return "Gym Bot is running!", 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/trigger_poll")
def trigger_poll():
    asyncio.run(send_daily_poll())
    return "✅ Poll triggered.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)