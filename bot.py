import os import asyncio from threading import Thread from flask import Flask from telegram import Bot
app = Flask(name)
BOT_TOKEN = os.getenv("BOT_TOKEN") CHAT_ID = os.getenv("CHAT_ID")
@app.route("/") def home(): return "VCT Intelligence Desk is running."
async def send_startup(): bot = Bot(BOT_TOKEN) await bot.send_message( chat_id=CHAT_ID, text="🟢 VCT Intelligence Desk is online and monitoring." )
def start_bot(): asyncio.run(send_startup())
if name == "main": Thread(target=start_bot).start() app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
