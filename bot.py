
import os
import asyncio
import threading

from flask import Flask
from telegram import Bot

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.route("/")
def home():
    return "VCT Intelligence Desk is running."


async def startup():
    bot = Bot(BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🟢 VCT Intelligence Desk is online and monitoring."
    )


def run_startup():
    asyncio.run(startup())


if __name__ == "__main__":
    threading.Thread(target=run_startup).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
