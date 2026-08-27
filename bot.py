
import os
import threading
import asyncio
import requests
from flask import Flask
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Prevent multiple polling threads when Gunicorn starts workers
_started = False

@app.route("/")
def home():
    return "VCT Intelligence Desk is running."

def score_coin(coin):
    score = 50
    reasons = []

    if coin.get("market_cap_rank", 999) <= 50:
        score += 20
        reasons.append("Large-cap strength")

    score += 10
    reasons.append("Trending narrative")

    if score >= 80:
        verdict = "BUY"
    elif score >= 60:
        verdict = "WATCH"
    else:
        verdict = "AVOID"

    return score, verdict, reasons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 VCT Intelligence Desk is ready.\n\nTry /hunt"
    )

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get(
        "https://api.coingecko.com/api/v3/search/trending",
        timeout=10
    ).json()["coins"]

    msg = "🎯 *VCT Hunt*\n\n"

    for c in data[:5]:
        coin = c["item"]
        score, verdict, reasons = score_coin(coin)

        msg += (
            f"*{coin['name']} ({coin['symbol'].upper()})*\n"
            f"{verdict} — {score}/100\n"
            f"Why: {', '.join(reasons)}\n\n"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")

async def auto_scan(context: ContextTypes.DEFAULT_TYPE):
    data = requests.get(
        "https://api.coingecko.com/api/v3/search/trending",
        timeout=10
    ).json()["coins"]

    coin = data[0]["item"]
    score, verdict, reasons = score_coin(coin)

    if score >= 80:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"🚨 VCT AUTO ALERT\n\n{coin['name']} ({coin['symbol'].upper()})\n{verdict} — {score}/100\nWhy: {', '.join(reasons)}"
        )

def telegram_worker():
    app_tg = Application.builder().token(BOT_TOKEN).build()

    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CommandHandler("hunt", hunt))

    app_tg.job_queue.run_repeating(auto_scan, interval=1800, first=30)

    app_tg.run_polling(drop_pending_updates=True)

def start_background():
    global _started
    if not _started:
        _started = True
        threading.Thread(target=telegram_worker, daemon=True).start()

# Start Telegram when Gunicorn imports this file
start_background()
