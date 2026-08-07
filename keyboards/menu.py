from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from services.config import POSSIBLE_VIDEO_FORMATS, POSSIBLE_AUDIO_CODECS

def get_idle_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Справка")
    builder.button(text="Об авторах")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def get_url_choice_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Получить видео")
    builder.button(text="Получить аудио")
    builder.button(text="Отмена")

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


def get_audio_format_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    # Если будут новые форматы для удобства добавления новых
    for audio_type in list(POSSIBLE_AUDIO_CODECS.keys()):
        builder.button(text=audio_type.upper())
    builder.button(text="Отмена")

    # Автоматически ставит максимум 2 кнопки в ряд
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_video_format_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for video_type in POSSIBLE_VIDEO_FORMATS:
        builder.button(text=video_type.upper())
    builder.button(text="Отмена")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
