from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Загрузить файл", callback_data="file_download")
    builder.button(text="Загрузить по ссылке", callback_data="download_by_url")
    builder.button(text="Справка", callback_data="help")
    builder.button(text="Об авторах", callback_data="about_authors")

    # Разделяет кнопки по числу на строку
    builder.adjust(2, 1, 1)

    return builder.as_markup()


def get_file_choice_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    builder.button(text="Получить аудио", callback_data="file_get_audio")

    return builder.as_markup()


def get_upload_prompt_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    builder.button(text="В главное меню", callback_data="main_menu")

    return builder.as_markup()


def get_audio_format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="MP3", callback_data="mp3")

    return builder.as_markup()
