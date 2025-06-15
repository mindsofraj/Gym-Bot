
import asyncio
import threading
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = "7614379751:AAGPa1hR0NLwsArzgAihp8nsiENHLZZhH5k"
CHAT_ID = "4870741901"

bot = Bot(token=BOT_TOKEN)

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

def send_poll_sync():
    asyncio.run(send_daily_poll())

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_poll_sync, 'cron', hour=7, minute=0)
    print("Scheduler started. Daily poll will be sent at 7:00 AM IST")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped")

app = Flask(__name__)

@app.route("/")
def home():
    return "Gym Bot is running! Daily polls scheduled at 7:00 AM. Status: OK"

@app.route("/health")
def health():
    return {"status": "healthy", "bot": "running", "scheduler": "active"}, 200

@app.route("/test_poll")
def test_poll():
    try:
        asyncio.run(send_daily_poll())
        return "Test poll sent successfully!"
    except Exception as e:
        return f"Error sending test poll: {e}", 500

if __name__ == "__main__":
    # Start scheduler in a separate daemon thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("Starting Flask app on port 8080...")
    print("Bot will send daily polls at 7:00 AM")
    print("UptimeRobot can monitor: https://your-repl-url.replit.app/health")
    
    # Start Flask app
    app.run(host="0.0.0.0", port=8080, debug=False)
