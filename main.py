import asyncio
import os
from flask import Flask
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

async def send_daily_poll():
    try:
        await bot.send_poll(
            chat_id=int(CHAT_ID),
            question="Who's coming to the gym today?",
            options=["Yes 💪", "No ❌", "Maybe 🤔"],
            is_anonymous=False
        )
        print("Poll sent successfully!")
    except TelegramError as e:
        print(f"Error sending poll: {e}")

@app.route("/")
def home():
    return "Telegram Gym Bot is running."

@app.route("/trigger_poll")
def trigger_poll():
    try:
        asyncio.run(send_daily_poll())
        return "Poll sent successfully.", 200
    except Exception as e:
        return f"Error sending poll: {e}", 500

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)