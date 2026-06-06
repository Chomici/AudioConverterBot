import os
import uuid

from aiogram import F
from aiogram import types, Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.menu import get_menu_keyboard, get_audio_format_keyboard
from keyboards.menu import get_back_keyboard, get_file_choice_keyboard
from states.file_download import FileDownloadState

router = Router()


# Принимаем файл либо по команде(/uploadfile), либо после нажатия кнопки ("Получить аудио")
async def show_upload_file_prompt(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(FileDownloadState.waiting_file)

    # Из-за разных способов ответа Message и CallbackQuery проверяем тип события
    if isinstance(event, types.Message):
        await event.answer("Отправьте видео файл одного из поддерживаемых параметров:",
                           reply_markup=get_back_keyboard())
    else:
        await event.message.edit_text("Отправьте видео файл одного из поддерживаемых параметров:",
                                      reply_markup=get_back_keyboard())


@router.message(Command("uploadfile"))
async def cmd_upload_file(message: types.Message, state: FSMContext):
    await show_upload_file_prompt(message, state)


@router.callback_query(F.data == "file_get_audio")
async def handle_file_get_audio(callback: types.CallbackQuery, state: FSMContext):
    await show_upload_file_prompt(callback, state)


# Фильтры в декораторе через запятую это условие AND
@router.callback_query(F.data == "back", StateFilter(FileDownloadState.waiting_file))
async def back_to_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_file_choice_keyboard())


# StateFilter гарантирует, что обработчик сработает только в нужном состоянии FSM.
# Могут прислать либо несжатый(document), либо сжатый(video) файл
@router.message(F.document | F.video, StateFilter(FileDownloadState.waiting_file))
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
    file_name = getattr(file, "file_name", None) or f"{uuid.uuid4()}.mp4"
    await bot.download(file.file_id, destination=f"temp_videos/{file_name}", timeout=300)

    # Пока что отправляем тот же видос
    await state.update_data(full_name=f"temp_videos/{file_name}")
    await state.set_state(FileDownloadState.waiting_file_format)

    await message.answer("Готово! Выберите формат аудиофайла: ",
                         reply_markup=get_audio_format_keyboard())


@router.callback_query(F.data == "mp3", StateFilter(FileDownloadState.waiting_file_format))
async def return_audio(callback: types.CallbackQuery, state: FSMContext):
    # Пока что отправляем тот же видос
    file_name = await state.get_value("full_name")
    audio = FSInputFile(file_name)

    await callback.answer()
    await callback.message.answer_document(document=audio, caption="Сделано с душой)")

    if os.path.exists(file_name):
        os.remove(file_name)

    await state.clear()
