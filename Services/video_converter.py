from moviepy import VideoFileClip

class VideoConverter:
    """
    Класс для работы с видеофайлами
    """
    def __init__(
            self,
            filename: str, # Имя файла для обработки
            ):
        self.filename = filename # исходное имя файла
        self.input_video_file = VideoFileClip(f"temp_videos\\{filename}") # Обьект типа VideoFileClip для работы с видеофайлом

    def converter_file(
            self,
            new_filename: str = None,
            target_format: str = "mp4"
    ):
        """
        Принимает новое имя файла и формат файла... Возвращает его в новом формате 
        """
        
        if not new_filename:
            new_filename = self.filename

        return self.input_video_file(f"temp_videos\\{new_filename + '.' + target_format}") # Возвращаем измененный файл