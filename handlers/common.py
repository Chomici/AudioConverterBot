from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types

from keyboards.menu import get_idle_keyboard

router = Router()

_INFO_MESSAGES = {
    "Об авторах": "Авторы",

    "Справка": '''Вы можете отправить как свое видео, так и ссылку на видео в Youtube (из Youtube можно получить как аудио, так и видео).
\nПоддерживаемые форматы:\n - Аудио - mp3, ogg, flac, wav;\n - Видео - mp4, avi, mov, mkv, webm'''
}


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в наш конвертер!\nЗдесь вы можете получить аудио из вашего видео.",
                         reply_markup=get_idle_keyboard())


@router.message(F.text.in_(_INFO_MESSAGES.keys()))
async def cmd_info(message: types.Message):
    await message.answer(_INFO_MESSAGES.get(message.text))


@router.message(F.text == "Отмена", ~StateFilter(None))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=get_idle_keyboard())