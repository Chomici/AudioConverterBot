from pathlib import Path

OUTPUT_DIR = Path("..\\temp_videos")

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
