import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()

# Создаем объекты бота и диспетчера
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Нажми меня", callback_data="btn_1")],
    [InlineKeyboardButton(text="Ссылка", url="https://example.com")]
])

@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()  # убирает "часики" на кнопке
    await callback.message.edit_text(f"Вы нажали: {callback.data}")

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот на aiogram!")

# Обработчик простого текста
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())