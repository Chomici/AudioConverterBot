import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.common import router as common_router
from handlers.file_download import router as file_download_router
from handlers.url_download import router as url_download_router

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())  # MemoryStorage нужен для хранения состояний

    # Порядок важен - он определяет приоритет обработки
    dp.include_router(url_download_router)
    dp.include_router(file_download_router)
    dp.include_router(common_router)  # common последним, ибо он содержит самые обобщенные обработчики

    os.makedirs("temp_videos", exist_ok=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
