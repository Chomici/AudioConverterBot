from aiogram.filters import Command, StateFilter
from aiogram import types, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from states.file_download import FileDownloadState

router = Router()


# Принимаем файл либо по команде, либо после нажатия кнопки
async def get_file(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(FileDownloadState.waiting_file)

    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    builder.button(text="В главное меню", callback_data="main_menu")

    # Из-за разных способов ответа Message и CallbackQuery проверяем тип события
    if isinstance(event, types.Message):
        await event.answer("Отправьте видео файл одного из поддерживаемых параметров:",
                           reply_markup=builder.as_markup())
    else:
        await event.message.edit_text("Отправьте видео файл одного из поддерживаемых параметров:",
                                      reply_markup=builder.as_markup())


@router.message(Command("file"))
async def cmd_get_file(message: types.Message, state: FSMContext):
    await get_file(message, state)


@router.callback_query(F.data == "get_audio")
async def handle_get_file(callback: types.CallbackQuery, state: FSMContext):
    await get_file(callback, state)


# Могут прислать либо несжатый(document), либо сжатый(video) файл
@router.message(F.document | F.video, StateFilter(FileDownloadState.waiting_file))
async def download_video(message: types.Message, bot: Bot, state: FSMContext):
    file = message.document or message.video

    # У TelegramAPI ограничение в 20МБ приема и 50МБ отдачи (вот это проблема)
    size_mb = file.file_size / (1024 * 1024)
    await message.answer(f"Размер файла: {size_mb:.1f} МБ")

    if file.file_size > 20 * 1024 * 1024:
        await message.answer("Файл слишком большой, максимум 20 МБ")
        return

    await message.answer("Скачивается...")
    await bot.download(file.file_id, destination=f"temp_videos/{file.file_name}", timeout=300)
    await state.clear()  # Временно, чтобы обновлять состояние после проверки
