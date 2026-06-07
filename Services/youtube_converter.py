from pytubefix import YouTube
from urllib.parse import urlparse
from Services.config import *



class YoutubeConverter:
    """
    Класс для работы с URL
    """

    def __init__(self, url: str):
        if self.is_valid_url(url):
            self.url = url
            self.youtube_object = self.get_youtube_object()
        else:
            raise ValueError("Недопустимый URL")

    def get_video_title(self) -> str:
        """
        Возвращает название Youtube видео
        """
        return self.youtube_object.title

    def get_video_author(self) -> str:
        """
        Возвращает никнейм автора Youtube видео
        """
        return self.youtube_object.author

    def get_video_description(self) -> str:
        """
        Возвращает описание Youtube видео
        """
        return self.youtube_object.description

    def get_video_thumbnail_url(self) -> str:
        """
        Возвращает ссылку на превью Youtube видео
        """
        return self.youtube_object.thumbnail_url

    def get_video_captions(self):
        """
        Возвращает словарь доступных субтитров Youtube видео
        """
        return self.youtube_object.captions

    def get_youtube_object(self) -> YouTube:
        """
        Возвращает Youtube обьект
        """
        return YouTube(url=self.url)

    def get_available_streams(self) -> dict:
        """
        Возвращает доступные потоки для скачивания Youtube видео
        """
        return {
            "video": list(self.youtube_object.streams.filter(only_video=True)),
            "audio": list(self.youtube_object.streams.filter(only_audio=True)),
            "both": list(self.youtube_object.streams.filter(progressive=True))
        }

    def download_with_quality(
        self,
        filename: str | None = None,
        quality: str = "lowest",  # lowest, highest, audio_only
        audio_quality: str = "medium"  # low, medium, high
    ):
        """Скачивает файл с выбором качества"""
        if quality == "lowest":
            stream = self.youtube_object.streams.get_lowest_resolution()
        elif quality == "highest":
            stream = self.youtube_object.streams.get_highest_resolution()
        elif quality == "audio_only":
            # Выбираем качество аудио
            audio_bitrates = {"low": "64kbps", "medium": "128kbps", "high": "160kbps"}
            stream = self.youtube_object.streams.filter(
                only_audio=True,
                abr=audio_bitrates.get(audio_quality, "128kbps")
            ).first()
        else:
            raise ValueError(f"Неизвестное качество: {quality}")

        if not stream:
            raise ValueError(f"Не удалось найти поток с качеством {quality}")

        stream.download(output_path=OUTPUT_DIR, filename=filename)
        return stream

    def save_video_captions(
        self,
        filename: str | None = None,
        path: Path = OUTPUT_DIR,
        lang: str = "ru"
    ):
        """
        Сохраняет субтитры Youtube видео
        """
        caption = self.get_video_caption_by_lang_code(lang=lang)
        if caption is None:
            raise ValueError("Субтитров не существует")

        if filename is None:
            filename = self.youtube_object.title.strip()

        caption.save_captions(filename=filename)

    def get_video_caption_by_lang_code(self, lang: str = "ru"):
        """
        Возвращает обьект Caption если субтитры существуют, если нет то возвращает None
        """
        return self.youtube_object.captions.get(lang, None)

    def download_file(self, filename: str | None = None):
        """
        Производит скачивание файла (Устаревшая версия: лучше пользоваться download_with_quality)
        """
        # Важное уточнение: output_path - это директория, а не конечное имя
        self.youtube_object.streams.get_lowest_resolution().download(output_path="temp_videos", filename=filename)

    def is_valid_url(self, url: str):
        """
        Проверяет, существует ли заданные домен
        """
        try:
            result = urlparse(url)
            # Проверяем есть ли и протокол, и домен
            return all([result.scheme, result.netloc])
        except Exception:
            return False


"""
Для тестов оставил
test1 = YoutubeConverter(url="https://music.youtube.com/watch?v=mRXRg6fR-nU&list=RDAMVMmRXRg6fR-nU")
test1.download_file(filename='Дотка.mp4')
test1 = VideoConverter(filename="Дотка.mp4")
test1.converter_file(new_filename='ТестНовойФичи', target_format='mp3')
"""
