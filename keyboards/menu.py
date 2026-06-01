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