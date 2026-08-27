
import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route("/")
def home():
    return "VCT Intelligence Desk is running."

def score_coin(coin):
    score = 50
    reasons = []

    if coin.get("market_cap_rank", 999) <= 50:
        score += 20
        reasons.append("Large-cap strength")

    if coin.get("price_btc", 0) > 0:
        score += 10
        reasons.append("Strong market attention")

    if score >= 80:
        verdict = "BUY"
    elif score >= 60:
        verdict = "WATCH"
    else:
        verdict = "AVOID"

    return score, verdict, reasons

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/search/trending"
    data = requests.get(url, timeout=10).json()["coins"]

    text = "🎯 *VCT Hunt*\n\n"

    for c in data[:5]:
        coin = c["item"]
        score, verdict, reasons = score_coin(coin)

        text += (
            f"*{coin['name']} ({coin['symbol'].upper()})*\n"
            f"Verdict: *{verdict}* ({score}/100)\n"
            f"Why: {', '.join(reasons)}\n\n"
        )

    await update.message.reply_text(text, parse_mode="Markdown")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await hunt(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 VCT Intelligence Desk\n\nUse:\n/hunt\n/today"
    )

async def auto_scan(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.getenv("CHAT_ID")

    url = "https://api.coingecko.com/api/v3/search/trending"
    data = requests.get(url, timeout=10).json()["coins"]

    coin = data[0]["item"]
    score, verdict, reasons = score_coin(coin)

    if score >= 80:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🚨 VCT AUTO ALERT\n\n"
                f"{coin['name']} ({coin['symbol'].upper()})\n"
                f"{verdict} ({score}/100)\n"
                f"Why: {', '.join(reasons)}"
            ),
            parse_mode="Markdown",
        )

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hunt", hunt))
    application.add_handler(CommandHandler("today", today))

    application.job_queue.run_repeating(
        auto_scan,
        interval=1800,
        first=30,
    )

    application.run_polling()

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=int(os.getenv("PORT", 10000)),
        ),
        daemon=True,
    ).start()

    run_bot()
