import os from flask import Flask from telegram import Bot import asyncio import threading
app = Flask(name)
BOT_TOKEN = os.getenv("BOT_TOKEN") CHAT_ID = os.getenv("CHAT_ID")
@app.route("/") def home(): return "VCT Intelligence Desk is running."
async def startup(): bot = Bot(BOT_TOKEN) await bot.send_message( chat_id=CHAT_ID, text="🟢 VCT Intelligence Desk is online and monitoring." )
def run_startup(): asyncio.run(startup())
threading.Thread(target=run_startup).start()
