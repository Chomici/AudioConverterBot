import os

from aiogram.filters import Command, StateFilter
from aiogram import types, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import FSInputFile

from states.file_download import FileDownloadState
from keyboards.menu import get_upload_prompt_keyboard, get_file_choice_keyboard
from keyboards.menu import get_menu_keyboard, get_audio_format_keyboard

router = Router()


# Принимаем файл либо по команде(/uploadfile), либо после нажатия кнопки ("Получить аудио")
async def show_upload_prompt(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(FileDownloadState.waiting_file)

    # Из-за разных способов ответа Message и CallbackQuery проверяем тип события
    if isinstance(event, types.Message):
        await event.answer("Отправьте видео файл одного из поддерживаемых параметров:",
                           reply_markup=get_upload_prompt_keyboard())
    else:
        await event.message.edit_text("Отправьте видео файл одного из поддерживаемых параметров:",
                                      reply_markup=get_upload_prompt_keyboard())


@router.message(Command("uploadfile"))
async def cmd_upload_file(message: types.Message, state: FSMContext):
    await show_upload_prompt(message, state)


@router.callback_query(F.data == "get_audio")
async def handle_get_audio(callback: types.CallbackQuery, state: FSMContext):
    await show_upload_prompt(callback, state)


@router.callback_query(F.data == "back", StateFilter(FileDownloadState.waiting_file))
async def back_to_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_file_choice_keyboard())


@router.callback_query(F.data == "main_menu", StateFilter(FileDownloadState.waiting_file))
async def to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_menu_keyboard())


# Могут прислать либо несжатый(document), либо сжатый(video) файл
@router.message(F.document | F.video, StateFilter(FileDownloadState.waiting_file))
async def handle_file_upload(message: types.Message, bot: Bot, state: FSMContext):
    file = message.document or message.video

    # У TelegramAPI ограничение в 20МБ приема и 50МБ отдачи (вот это проблема)
    size_mb = file.file_size / (1024 * 1024)
    await message.answer(f"Размер файла: {size_mb:.1f} МБ")

    if file.file_size > 20 * 1024 * 1024:
        await message.answer("Файл слишком большой, максимум 20 МБ")
        return

    await message.answer("Скачивается...")
    await bot.download(file.file_id, destination=f"temp_videos/{file.file_name}", timeout=300)

    # Пока что отправляем тот же видос
    await state.update_data(full_name=f"temp_videos/{file.file_name}")
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