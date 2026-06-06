from aiogram.fsm.state import State, StatesGroup


class FileDownloadState(StatesGroup):
    """
    Состояния, в которых может находиться пользователь
    при работе через загрузку своего видео  файла
    """
    waiting_file = State()
    waiting_file_format = State()


