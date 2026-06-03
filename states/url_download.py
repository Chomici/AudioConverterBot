from aiogram.fsm.state import StatesGroup, State


class URLDownloadState(StatesGroup):
    """
    Состояния, в которых может находиться пользователь
    при работе через вставку ссылки на видео
    """
    waiting_url = State()
    waiting_video_format = State()
    waiting_audio_format = State()
