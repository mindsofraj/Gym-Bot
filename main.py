
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def send_daily_poll():
    try:
        await bot.send_poll(
            chat_id=int(CHAT_ID),
            question="Who's coming to the gym today?",
            options=["Yes 💪", "No ❌", "Maybe 🤔"],
            is_anonymous=False
        )
        print("Poll sent!")
    except TelegramError as e:
        print(f"Error sending poll: {e}")

def send_poll_sync():
    asyncio.run(send_daily_poll())

# Scheduler: everyday at 07:00 AM
scheduler = AsyncIOScheduler()
scheduler.add_job(send_poll_sync, 'cron', hour=7, minute=0)
scheduler.start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/test_poll")
async def test_poll():
    await send_daily_poll()
    return "Test poll sent!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
