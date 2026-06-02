from aiogram.fsm.state import StatesGroup, State


class URLDownloadState(StatesGroup):
    waiting_url = State()
    waiting_video_format = State()
    waiting_audio_format = State()
