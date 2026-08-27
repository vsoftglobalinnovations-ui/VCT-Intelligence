import asyncio
from telegram import Bot
from config import BOT_TOKEN, CHAT_ID

async def main():
    bot=Bot(BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID,text="🚀 VCT Intelligence Desk is LIVE. Telegram connection works.")
asyncio.run(main())
