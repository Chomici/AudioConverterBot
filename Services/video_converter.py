import pathlib
from re import search  # для обрезки расширения файла
from moviepy import VideoFileClip
from Services.config import *


class VideoConverter:
    """
    Класс для работы с видео файлами
    """

    def __init__(self, filename: str):
        # SRE_Match - объект хранящий индекс и информацию о расширении
        regex_file_format = search(r'\.\w*$', filename)

        # Записанные в телеге видео не имеют имени и формата, по умолчанию mp4
        if regex_file_format is None:
            self.file_format = "mp4"
        else:
            # Формат файла, полученный из регулярного выражения без точки
            self.file_format = regex_file_format.group(0)[1:]

        # Убираем выход из папки, ибо запуск бота из main.py,
        # который на уровне с temp_videos
        file_path = Path(OUTPUT_DIR / filename)

        # Исходное имя файла без расширения
        self.filename = file_path.stem

        # Объект типа VideoFileClip для работы с видео файлом
        self.input_video_file = VideoFileClip(str(file_path))

    def converter_file(
        self,
        new_filename: str = None,  # Новое имя для файла
        target_format: str = "mp3"  # Новый формат для файла
    ):
        """
        Принимает новое имя файла и формат файла... возвращает его в новом формате
        """
        # Делаем все буквы строчными, чтобы избежать ошибки с POSSIBLE_AUDIO_FORMATS
        target_format = target_format.lower()

        # Проверяем было ли передано имя в метод, если нет, то берем изначальное имя
        if not new_filename:
            new_filename = self.filename

        # Проверяем на наличие аудиодорожки у видео файла
        if self.input_video_file.audio is None:
            raise ValueError("Файл не содержит аудио дорожку")

        # Конвертация в аудио формат
        try:
            # Проверяем на допустимость формата
            if target_format in POSSIBLE_AUDIO_CODECS:
                output_path = OUTPUT_DIR / f"{new_filename}.{target_format}"
                codec_settings = POSSIBLE_AUDIO_CODECS[target_format]

                # Аргументы для кодировки файла
                write_args = {
                    "filename": str(output_path),
                    "codec": codec_settings["codec"],
                    "logger": None
                }

                # Если для формата нужен битрейт (для wav/flac он не нужен)
                if codec_settings.get("bitrate"):
                    write_args["bitrate"] = codec_settings["bitrate"]

                # Создаем измененный файл аудио формата
                self.input_video_file.audio.write_audiofile(**write_args)

                # Файл нужно закрыть для правильной очистки временного видео
                self.close()

                # Конвертер будет чистить временное видео сам
                temp_path = OUTPUT_DIR / f"{self.filename}.{self.file_format}"
                if temp_path.exists():
                    temp_path.unlink()

                return str(output_path)
            else:
                # TODO : добавить связь с ботом о ошибке формата
                pass
        except Exception as ex:
            # Если словили ошибку, то закроем здесь, если в блоке try не смогли
            self.close()
            print(ex)

    def close(self):
        """
        Закрывает видеофайл и освобождает ресурсы
        """
        self.input_video_file.close()

    def __exit__(self, exc_type, exc, tb):
        self.close()
