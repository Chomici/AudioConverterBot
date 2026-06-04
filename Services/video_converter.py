from re import search # для обрезки расширения файла
from os import path # для отправки в temp_videos
from moviepy import VideoFileClip

POSSIBLE_AUDIO_FORMATS = [ # Взято из use-case
    "mp3", 
    "wav",
    "flac",
    "ogg"
]

class VideoConverter:
    """
    Класс для работы с видеофайлами
    """
    def __init__(
            self,
            filename: str, # Имя файла для обработки
            ):
        
        regex_file_format = search(r'\.\w*$', filename) # SRE_Match Обьект хранящий индекс и информацию о расширении
        
        # Проверка не пустое ли руглярное выражение
        if regex_file_format is None:
            raise ValueError("Файл без формата") 
            
        self.file_format = regex_file_format.group(0)[1:] # Формат файла, полученный из регулярного выражения без точки
        self.filename = filename[:regex_file_format.start()] # Исходное имя файла без расширения
        self.input_video_file = VideoFileClip(f"{filename}") # Обьект типа VideoFileClip для работы с видеофайлом

    def converter_file(
            self,
            new_filename: str = None, # Новое имя для файла
            target_format: str = "mp3" # Новый формат для файла
    ):
        """
        Принимает новое имя файла и формат файла... Возвращает его в новом формате 
        """
        target_format = target_format.lower() # Делаем все буквы строчными чтобы избежать ошибки с POSSIBLE_AUDIO_FORMATS
 
        if not new_filename: # Проверяем было ли передано имя в метод, если нет то берем изначальное имя
            new_filename = self.filename

        # Проверяем на наличие аудиодорожки у видеофайла
        if self.input_video_file.audio is None:
            raise ValueError("Файл не содержит аудио дорожку")

        # Конвертация в аудиоформат
        try:                
            # Проверяем на допустимость формата
            if target_format in POSSIBLE_AUDIO_FORMATS:
                self.input_video_file.audio.write_audiofile(path.join("..\\temp_videos\\", f"{new_filename}.{target_format}")) # Возвращаем измененный файл аудио формата 
            else:
                #TODO : добавить связь с ботом о ошибке формата
                pass
        except Exception as ex:
            print(ex) 
        finally:
            self.close()

    def close(self):
        """
        Закрывает видеофайл и освобождает ресурсы
        """
        self.input_video_file.close()

    def __exit__(self, exc_type, exc, tb):
        self.close()