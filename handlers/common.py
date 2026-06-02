from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram import F

from keyboards.menu import get_menu_keyboard, get_file_choice_keyboard, get_url_choice_keyboard

# Каждый роутер отвечает за свой набор команд/действий
router = Router()

_INFO_MESSAGES = {
    "about_authors": "Авторы",
    "help": "Справка"
}


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в наш конвертер!\nЗдесь вы можете получить аудио из вашего видео.")
    await cmd_menu(message)


@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_menu_keyboard())


@router.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")


@router.callback_query(F.data.in_(_INFO_MESSAGES))
async def handle_info_buttons(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"{_INFO_MESSAGES.get(callback.data, "Нет информации")}")


@router.callback_query(F.data == "file_download")
async def show_file_choice(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_file_choice_keyboard())


@router.callback_query(F.data == "download_by_url")
async def show_url_choice(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_url_choice_keyboard())


@router.callback_query(F.data == "back")
async def handle_back(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_menu_keyboard())


@router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery):
    await callback.answer()  # Без всплывающего уведомления
    await callback.message.edit_text(f"Вы нажали: {callback.data}")
