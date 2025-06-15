from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_daily_poll():
    bot.send_poll(
        chat_id=int(CHAT_ID),
        question="Who's coming to the gym today?",
        options=["Yes 💪", "No ❌", "Maybe 🤔"],
        is_anonymous=False
    )
    print("Poll sent!")

# Scheduler: everyday at 07:00 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_poll, 'cron', hour=7, minute=0)
scheduler.start()

app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)