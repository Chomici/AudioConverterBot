from aiogram.fsm.state import State, StatesGroup


class FileDownloadState(StatesGroup):
    waiting_file = State()
    waiting_file_format = State()


class URLDownloadState(StatesGroup):
    waiting_url = State()
    waiting_video_format = State()
    waiting_audio_format = State()
