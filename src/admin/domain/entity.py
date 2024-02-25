from dataclasses import dataclass


@dataclass
class GeneratedContent:
    image_name: str
    origin_image: bytes
    audio_content: bytes
    video_content: bytes


@dataclass
class GeneratedContentName:
    image_name: str


@dataclass
class OriginImageInfo:
    image_name: str
    image_file: bytes
