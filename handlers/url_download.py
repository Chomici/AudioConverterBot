import asyncio

from aiogram import F
from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.menu import get_back_keyboard, get_url_choice_keyboard
from keyboards.menu import get_audio_format_keyboard, get_video_format_keyboard
from states.url_download import URLDownloadState

from services.config import POSSIBLE_VIDEO_FORMATS, POSSIBLE_AUDIO_CODECS, OUTPUT_DIR
from services.utils import download_video, download_audio

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
    video_path = None  # Для доступа в блоке finally

    await callback.answer()
    status_msg = await callback.message.answer("Скачиваю видео, подождите...")

    try:
        # Чтобы не выносить в несколько потоков, выполняем в отдельной функции
        file_name = await asyncio.to_thread(download_video,
                                            url=url,
                                            target_format=callback.data)

        video_path = OUTPUT_DIR / f"{file_name}.{callback.data}"
        video_file = FSInputFile(video_path)

        await callback.message.answer_document(document=video_file, caption="Сделано с душой)")

    # Ошибки загрузки через поток или непредвиденные ошибки
    except Exception as ex:
        await callback.message.answer("Неизвестная ошибка во время загрузки видео")
        print(f"Сбой в url_download.py (upload_video): {ex}")

    finally:
        # Удаляем статусное сообщение
        try:
            await status_msg.delete()
        except Exception:
            pass  # Если сообщение уже удалено

        # Чистим видео файл
        if video_path and video_path.exists():
            video_path.unlink()

        await state.clear()


@router.callback_query(F.data.in_(list(POSSIBLE_AUDIO_CODECS.keys())),
                       StateFilter(URLDownloadState.waiting_audio_format))
async def upload_audio(callback: types.CallbackQuery, state: FSMContext):
    url = await state.get_value('url')
    audio_path = None  # Для доступа в блоке finally

    await callback.answer()
    status_msg = await callback.message.answer("Скачиваю аудио, подождите...")

    try:
        file_name = await asyncio.to_thread(download_audio,
                                            url=url,
                                            target_format=callback.data)

        audio_path = OUTPUT_DIR / f"{file_name}.{callback.data}"
        audio_file = FSInputFile(audio_path)

        await callback.message.answer_document(document=audio_file, caption="Сделано с душой)")

    except Exception as ex:
        await callback.message.answer("Неизвестная ошибка во время загрузки видео")
        print(f"Сбой в url_download.py (upload_audio): {ex}")

    finally:
        # Удаляем статусное сообщение
        try:
            await status_msg.delete()
        except Exception:
            pass  # Если сообщение уже удалено

        if audio_path and audio_path.exists():
            audio_path.unlink()

        await state.clear()
