import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

load_dotenv()

# Создаем объекты бота и диспетчера
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Загрузить файл", callback_data="download_file")
    builder.button(text="Загрузить по ссылке", callback_data="download_by_url")
    builder.button(text="Справка", callback_data="help")
    builder.button(text="Об авторах", callback_data="about_authors")

    # Разделяет кнопки по числу на строку
    builder.adjust(2, 1, 1)

    return builder.as_markup()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в наш конвертер!\nЗдесь вы можете получить аудио из вашего видео.")
    await cmd_menu(message)


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_menu_keyboard())


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")


@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()  # Без всплывающего уведомления
    await callback.message.edit_text(f"Вы нажали: {callback.data}")


async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
