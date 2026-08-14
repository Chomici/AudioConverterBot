from re import search  # для обрезки расширения файла
from moviepy import VideoFileClip
from services.config import *


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

        # Сохраняем Path-объект исходного файла
        self.filename = sanitize_filename(filename)

        # Убираем выход из папки, ибо запуск бота из main.py,
        # который на уровне с temp_videos
        self.file_path = Path(OUTPUT_DIR / self.filename)

        # Исходное имя файла без расширения
        self.filename = self.file_path.stem

        # Объект типа VideoFileClip для работы с видео файлом
        self.input_video_file = VideoFileClip(str(self.file_path))

    def converter_file(
            self,
            new_filename: str | None = None,
            target_format: str = "mp3"
    ) -> str:
        """
        Принимает новое имя файла и формат файла... возвращает его в новом формате
        """
        output_path = None
        try:
            target_format = target_format.lower()

            if target_format not in POSSIBLE_AUDIO_CODECS:
                raise ValueError(f"Неподдерживаемый тип данных: {target_format}")

            if self.input_video_file.audio is None:
                raise ValueError("Файл не содержит аудио дорожку")

            new_filename = sanitize_filename(new_filename) if new_filename else self.filename
            output_path = OUTPUT_DIR / f"{new_filename}.{target_format}"
            codec_settings = POSSIBLE_AUDIO_CODECS[target_format]

            write_args = {
                "filename": str(output_path),
                "codec": codec_settings["codec"],
                "logger": None
            }

            if codec_settings.get("bitrate"):
                write_args["bitrate"] = codec_settings["bitrate"]

            # Создаем измененный файл аудио формата
            self.input_video_file.audio.write_audiofile(**write_args)
            return str(output_path)

        except Exception as ex:
            # Если конвертация упала — подчищаем недописанный битый выходной файл
            if output_path and output_path.exists():
                try:
                    output_path.unlink()
                except OSError:
                    pass

            # Пробрасываем ошибку дальше для логирования / ответа пользователю
            raise ex

        finally:
            # Гарантированно освобождаем ресурсы MoviePy
            self.close()

            # Безопасно удаляем временный исходник
            if self.file_path.exists():
                try:
                    self.file_path.unlink()
                except OSError:
                    pass  # Если файл временно заблокирован ОС, не падаем

    def close(self):
        """
        Закрывает видеофайл и освобождает ресурсы
        """
        if hasattr(self, 'input_video_file') and self.input_video_file:
            self.input_video_file.close()
