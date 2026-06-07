import os

from aiogram import F
from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.menu import get_back_keyboard, get_url_choice_keyboard
from keyboards.menu import get_audio_format_keyboard, get_video_format_keyboard
from states.url_download import URLDownloadState

from Services.config import POSSIBLE_VIDEO_FORMATS
from Services.youtube_converter import YoutubeConverter

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


@router.callback_query(F.data.in_(POSSIBLE_VIDEO_FORMATS), StateFilter(URLDownloadState.waiting_video_format))
async def upload_video(callback: types.CallbackQuery, state: FSMContext):
    url = await state.get_value('url')

    video = YoutubeConverter(url=url)
    file_name = video.get_video_title()
    video.download_file(filename=f"{file_name}.{callback.data}")

    video_path = FSInputFile(f"temp_videos/{file_name}.{callback.data}")

    await callback.answer()
    await callback.message.answer_document(document=video_path, caption="Сделано с душой)")

    # Чистим видео файл
    if os.path.exists(f"temp_videos/{file_name}.{callback.data}"):
        os.remove(f"temp_videos/{file_name}.{callback.data}")

    await state.clear()


@router.callback_query(F.data == "mp3", StateFilter(URLDownloadState.waiting_audio_format))
async def upload_audio(callback: types.CallbackQuery, state: FSMContext):
    # Заглушка, просто возврат ссылки
    await callback.answer()
    await callback.message.answer(f"{await state.get_value('url')}")
    await callback.message.answer("Сделано с душой)")

    await state.clear()
