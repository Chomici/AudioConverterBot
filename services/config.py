import re
from pathlib import Path

# Так как бот запускается из main.py, выход из папки services не нужен
OUTPUT_DIR = Path("temp_videos")

# Для корректной конвертации по ссылке через YoutubeConverter
POSSIBLE_AUDIO_CODECS = {  # Взято из use-case
    "mp3": {"codec": "libmp3lame", "bitrate": "192k"},
    "ogg": {"codec": "libvorbis", "bitrate": "192k"},
    "wav": {"codec": "pcm_s16le", "bitrate": None},
    "flac": {"codec": "flac", "bitrate": None},
}

POSSIBLE_VIDEO_FORMATS = [  # Взято из use-case
    "mp4", 
    "avi",
    "mov",
    "mkv",
    "webm"
]


def sanitize_filename(filename: str, replacement: str = "") -> str:
    """
    Очищает строку от символов, запрещенных в именах файлов.
    """
    bad_chars = r'[\\/*?:"<>|]'
    return re.sub(bad_chars, replacement, filename).strip()
