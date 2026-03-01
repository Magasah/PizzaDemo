import asyncio
import os
from aiogram import Bot, Dispatcher

try:
    from config import BOT_TOKEN
except Exception:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

import handlers


async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Set the BOT_TOKEN environment variable or provide a config.py"
        )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    handlers.register_handlers(dp)

    print("Bot is starting. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
