from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram import F

# Каждый роутер отвечает за свой набор команд/действий
router = Router()

_INFO_MESSAGES = {
    "about_authors": "Авторы",

    "help": '''Вы можете отправить как свое видео, так и ссылку на видео в Youtube (из Youtube можно получить как аудио, так и видео).
\nПоддерживаемые форматы:\n - Аудио - mp3, ogg, flac, wav;\n - Видео - mp4, avi, mov, mkv, webm'''
}


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в наш конвертер!\nЗдесь вы можете получить аудио из вашего видео.")


@router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"Вы нажали: {callback.data}")