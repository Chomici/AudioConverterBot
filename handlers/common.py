from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram import F

# Каждый роутер отвечает за свой набор команд/действий
router = Router()

_INFO_MESSAGES = {
    "about_authors": "Авторы",
    "help": "Справка"
}


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Загрузить файл", callback_data="file_download")
    builder.button(text="Загрузить по ссылке", callback_data="download_by_url")
    builder.button(text="Справка", callback_data="help")
    builder.button(text="Об авторах", callback_data="about_authors")

    # Разделяет кнопки по числу на строку
    builder.adjust(2, 1, 1)

    return builder.as_markup()


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
async def handle_file_download(callback: types.CallbackQuery):
    await callback.answer()

    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    builder.button(text="Получить аудио", callback_data="get_audio")

    await callback.message.edit_text("Выберите действие:", reply_markup=builder.as_markup())


@router.callback_query(F.data == "back")
async def handle_back(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_menu_keyboard())


@router.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()  # Без всплывающего уведомления
    await callback.message.edit_text(f"Вы нажали: {callback.data}")
