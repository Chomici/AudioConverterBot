from pytubefix import YouTube

from pathlib import Path # для отправки в temp_videos
from urllib.parse import urlparse

class YoutubeConverter:
    """
    Класс для работы с URL
    """
    def __init__(self, url: str):
        self.output_dir = Path("..\\temp_videos")        
        
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

    def downoload_file(self):
        """
        Производит скачивание файла
        """
        self.youtube_object.streams.get_lowest_resolution().download(output_path=self.output_dir) # Важное уточнее что output_path это директория а не конечное имя

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