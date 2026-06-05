from aiogram import F
from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.menu import get_menu_keyboard, get_back_keyboard, get_url_choice_keyboard
from keyboards.menu import get_audio_format_keyboard, get_video_format_keyboard
from states.url_download import URLDownloadState

router = Router()


@router.callback_query(F.data.in_(["url_get_video", "url_get_audio"]))
async def show_paste_url_prompt(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(URLDownloadState.waiting_url)
    # Берем состояние сразу, ибо ссылку в обоих случаях принимаем
    await state.update_data(type=callback.data)

    await callback.answer()
    await callback.message.edit_text("Вставьте ссылку на ваше видео (Youtube):",
                                     reply_markup=get_back_keyboard())


@router.callback_query(F.data == "back", StateFilter(URLDownloadState.waiting_url))
async def back_to_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_url_choice_keyboard())


@router.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"), StateFilter(URLDownloadState.waiting_url))
async def handle_paste_url(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(url=url)

    action_type = await state.get_value("type")

    if action_type == "url_get_video":
        await state.set_state(URLDownloadState.waiting_video_format)
        await message.answer("Выберите формат видео:", reply_markup=get_video_format_keyboard())
    elif action_type == "url_get_audio":
        await state.set_state(URLDownloadState.waiting_audio_format)
        await message.answer("Выберите формат аудиофайла:", reply_markup=get_audio_format_keyboard())


@router.message(StateFilter(URLDownloadState.waiting_url))
async def handle_invalid_url(message: types.Message):
    await message.answer("Неверная ссылка, повторите ещё раз.")


@router.callback_query(F.data == "mp4", StateFilter(URLDownloadState.waiting_video_format))
async def upload_video(callback: types.CallbackQuery, state: FSMContext):
    # Заглушка, просто возврат ссылки
    await callback.answer()
    await callback.message.answer(f"{await state.get_value('url')}")
    await callback.message.answer("Сделано с душой)")

    await state.clear()


@router.callback_query(F.data == "mp3", StateFilter(URLDownloadState.waiting_audio_format))
async def upload_audio(callback: types.CallbackQuery, state: FSMContext):
    # Заглушка, просто возврат ссылки
    await callback.answer()
    await callback.message.answer(f"{await state.get_value('url')}")
    await callback.message.answer("Сделано с душой)")

    await state.clear()


@router.callback_query(F.data == "main_menu", StateFilter(URLDownloadState.waiting_url))
async def to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_menu_keyboard())
