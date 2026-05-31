from aiogram.fsm.state import State, StatesGroup


class FileDownloadState(StatesGroup):
    waiting_action = State()
    waiting_file = State()
    waiting_file_format = State()
    