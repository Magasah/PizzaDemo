import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
import handlers


async def main():
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
