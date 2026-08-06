from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.config import POSSIBLE_VIDEO_FORMATS, POSSIBLE_AUDIO_CODECS


def get_url_choice_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить видео", callback_data="url_get_video")
    builder.button(text="Получить аудио", callback_data="url_get_audio")
    builder.button(text="Назад", callback_data="back")

    builder.adjust(2, 1)

    return builder.as_markup()


def get_audio_format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Если будут новые форматы для удобства добавления новых
    for audio_type in list(POSSIBLE_AUDIO_CODECS.keys()):
        builder.button(text=audio_type.upper(), callback_data=audio_type.lower())

    # Автоматически ставит максимум 2 кнопки в ряд
    builder.adjust(2)

    return builder.as_markup()


def get_video_format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for video_type in POSSIBLE_VIDEO_FORMATS:
        builder.button(text=video_type.upper(), callback_data=video_type.lower())

    builder.adjust(2)

    return builder.as_markup()
