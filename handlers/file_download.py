import asyncio
import pathlib
import uuid

from aiogram import F
from aiogram import types, Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.menu import get_audio_format_keyboard

from services.config import POSSIBLE_AUDIO_CODECS, OUTPUT_DIR
from services.utils import convert_video
from states.media import MediaState

router = Router()


# Могут прислать либо несжатый(document), либо сжатый(video) файл
@router.message(F.document | F.video)
async def handle_file_upload(message: types.Message, bot: Bot, state: FSMContext):
    # bot и state автоматически достаются aiogram из контекста
    file = message.document or message.video

    # У TelegramAPI ограничение в 20МБ приема и 50МБ отдачи (вот это проблема)
    size_mb = file.file_size / (1024 * 1024)
    await message.answer(f"Размер файла: {size_mb:.1f} МБ")

    if file.file_size > 20 * 1024 * 1024:
        await message.answer("Файл слишком большой, максимум 20 МБ")
        return

    await message.answer("Скачивается...")
    # Если телеграм не дал имя файлу, генерируем
    file_name = getattr(file, "file_name", None) or f"{uuid.uuid4()}"

    video_path = OUTPUT_DIR / file_name
    await bot.download(file.file_id, destination=str(video_path), timeout=300)

    # Сохраняем имя файла для класса VideoConverter
    await state.update_data(full_name=file_name)
    await state.set_state(MediaState.waiting_file_format)

    await message.answer("Готово! Выберите формат аудиофайла: ",
                         reply_markup=get_audio_format_keyboard())


@router.callback_query(F.data.in_(list(POSSIBLE_AUDIO_CODECS.keys())),
                       StateFilter(MediaState.waiting_file_format))
async def return_audio(callback: types.CallbackQuery, state: FSMContext):
    file_name = await state.get_value("full_name")
    audio_path = None

    await callback.answer()
    status_msg = await callback.message.answer("Извлекаю аудиодорожку, подождите...")

    try:
        if not file_name:
            raise ValueError("Файл не найден")

        # Получаем имя без расширения
        base_name = pathlib.Path(file_name).stem
        audio_path = OUTPUT_DIR / f"{base_name}.{callback.data}"

        # Чтобы не выносить в несколько потоков, выполняем в отдельной функции
        await asyncio.to_thread(convert_video,
                                filename=file_name,
                                new_filename=base_name,
                                target_format=callback.data)

        audio_file = FSInputFile(audio_path)
        await callback.message.answer_document(document=audio_file, caption="Сделано с душой)")

    # Ошибки, возможные при конвертации в VideoConverter
    except ValueError as value_ex:
        await callback.message.answer(f"Ошибка обработки: {value_ex}")
    # Непредвиденные ошибки
    except Exception as ex:
        await callback.message.answer(f"Неизвестная ошибка во время конвертации. Возможно, файл поврежден")
        print(f"Сбой в file_download.py (return_audio): {ex}")

    finally:
        # Удаляем статусное сообщение
        try:
            await status_msg.delete()
        except Exception:
            pass  # Если сообщение уже удалено

        # Чистим аудио файл
        if audio_path and audio_path.exists():
            audio_path.unlink()

        await state.clear()

