from aiogram.fsm.state import State, StatesGroup

class MediaState(StatesGroup):
    """
    Основные состояния ожидания для пользователя
    """
    # При загрузке своего видео сразу запрашиваем аудио формат
    waiting_file_format = State()

    # При загрузке ссылки запрашиваем тип данных: аудио или видео, а потом формат
    waiting_url_type = State()
    waiting_url_format = State()