import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from handlers.common import router as common_router

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(common_router)


async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
