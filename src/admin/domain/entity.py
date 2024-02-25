from dataclasses import dataclass


@dataclass
class GeneratedContent:
    image_name: str
    origin_image: bytes = None
    audio_content: bytes = None
    video_content: bytes = None


@dataclass
class GeneratedContentName:
    image_name: str


@dataclass
class OriginImageInfo:
    image_name: str
    image_file: bytes


@dataclass
class GeneratedTextContent:
    image_name: str
    text_content: bytes = None
    coord_content: bytes = None
