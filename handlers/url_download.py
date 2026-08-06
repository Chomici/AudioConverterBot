import asyncio

from aiogram import F
from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.menu import get_url_choice_keyboard, get_audio_format_keyboard, get_video_format_keyboard
from states.media import MediaState

from services.config import POSSIBLE_VIDEO_FORMATS, POSSIBLE_AUDIO_CODECS, OUTPUT_DIR
from services.utils import download_video, download_audio

router = Router()


@router.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_paste_url(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(url=url)

    await state.set_state(MediaState.waiting_url_type)
    await message.answer("Выберите тип файла:", reply_markup=get_url_choice_keyboard())


@router.message(F.text == "Получить аудио", StateFilter(MediaState.waiting_url_type))
async def url_get_audio(message: types.Message, state: FSMContext):
    await state.set_state(MediaState.waiting_url_format)
    await message.answer("Выберите формат аудиофайла:", reply_markup=get_audio_format_keyboard())


@router.message(F.text == "Получить видео", StateFilter(MediaState.waiting_url_type))
async def url_get_video(message: types.Message, state: FSMContext):
    await state.set_state(MediaState.waiting_url_format)
    await message.answer("Выберите формат видеофайла:", reply_markup=get_video_format_keyboard())


@router.message(F.text.lower().in_(POSSIBLE_VIDEO_FORMATS), StateFilter(MediaState.waiting_url_format))
async def upload_video(message: types.Message, state: FSMContext):
    url = await state.get_value('url')
    target_format = message.text.lower()
    video_path = None  # Для доступа в блоке finally

    status_msg = await message.answer("Скачиваю видео, подождите...")

    try:
        # Чтобы не выносить в несколько потоков, выполняем в отдельной функции
        file_name = await asyncio.to_thread(download_video,
                                            url=url,
                                            target_format=target_format)

        video_path = OUTPUT_DIR / f"{file_name}.{target_format}"
        video_file = FSInputFile(video_path)

        await message.answer_document(document=video_file, caption="Сделано с душой)")

    # Ошибки загрузки через поток или непредвиденные ошибки
    except Exception as ex:
        await message.answer("Неизвестная ошибка во время загрузки видео")
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


@router.message(F.text.lower().in_(list(POSSIBLE_AUDIO_CODECS.keys())), StateFilter(MediaState.waiting_url_format))
async def upload_audio(message: types.Message, state: FSMContext):
    url = await state.get_value('url')
    target_format = message.text.lower()
    audio_path = None  # Для доступа в блоке finally

    status_msg = await message.answer("Скачиваю аудио, подождите...")

    try:
        file_name = await asyncio.to_thread(download_audio,
                                            url=url,
                                            target_format=target_format)

        audio_path = OUTPUT_DIR / f"{file_name}.{target_format}"
        audio_file = FSInputFile(audio_path)

        await message.answer_document(document=audio_file, caption="Сделано с душой)")

    except Exception as ex:
        await message.answer("Неизвестная ошибка во время загрузки видео")
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