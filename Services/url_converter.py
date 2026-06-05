from pytubefix import YouTube

from re import search # для обрезки расширения файла
from pathlib import Path # для отправки в temp_videos
from urllib.parse import urlparse

class UrlConverter:
    """
    Класс для работы с URL
    """
    def __init__(self, url: str):
        if self.is_valid_url(url):
            self.url = url
        else:
            raise ValueError("Недопустимый URL")
        
    def downoload_file(self):
        """
        Производит скачивание файла
        """
        yt = YouTube(url=self.url)
        output_dir = Path("..\\temp_videos")        
        yt.streams.get_lowest_resolution().download(output_path=output_dir) # Важное уточнее что output_path это директория а не конечное имя

    def is_valid_url(self, url: str):
        """
        Проверяет существует ли заданные домен
        """
        try:
            result = urlparse(url)
            # Проверяем есть ли и протокол, и домен
            return all([result.scheme, result.netloc])
        except Exception:
            return False