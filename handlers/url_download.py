from aiogram import F
from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.menu import get_menu_keyboard, get_paste_url_keyboard, get_url_choice_keyboard
from states.url_download import URLDownloadState

router = Router()


@router.callback_query(F.data.in_(["url_get_video", "url_get_audio"]))
async def show_paste_url_prompt(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(URLDownloadState.waiting_url)
    # Берем состояние сразу, ибо ссылку в обоих случаях принимаем
    await state.update_data(type=callback.data)

    await callback.answer()
    await callback.message.edit_text("Вставьте ссылку на ваше видео (Youtube):",
                                     reply_markup=get_paste_url_keyboard())


@router.callback_query(F.data == "back", StateFilter(URLDownloadState.waiting_url))
async def back_to_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_url_choice_keyboard())


@router.callback_query(F.data == "main_menu", StateFilter(URLDownloadState.waiting_url))
async def to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выберите действие:", reply_markup=get_menu_keyboard())
