from Services.youtube_converter import YoutubeConverter
from Services.video_converter import VideoConverter


def download_video(url: str, target_format: str) -> str:
    video = YoutubeConverter(url=url)
    file_name = video.get_video_title()
    video.download_file(filename=f"{file_name}.{target_format}")
    return file_name


def download_audio(url: str, target_format: str) -> str:
    video = YoutubeConverter(url=url)
    file_name = video.get_video_title()
    video.download_with_quality(filename=f"{file_name}.{target_format}",
                                quality="audio_only",
                                audio_quality="medium")
    return file_name


def convert_video(filename: str, new_filename: str, target_format: str):
    video = VideoConverter(filename=filename)
    video.converter_file(new_filename=new_filename,
                         target_format=target_format)
