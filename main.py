import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from handlers.common import router as common_router

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(common_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
