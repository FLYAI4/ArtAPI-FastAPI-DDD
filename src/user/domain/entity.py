from dataclasses import dataclass


@dataclass
class OriginImageInfo:
    id: str
    image_file: bytes


@dataclass
class FileInfo:
    unique_id: str
    image_name: str


@dataclass
class UserReview:
    id: str
    image_name: str
    like_status: bool
    review_content: str


@dataclass
class UserId:
    id: str


@dataclass
class ContentName:
    image_name: str


@dataclass
class ContentInfo:
    tag: str
    data: bytes = None


@dataclass
class MainContent:
    resize_image: bytes
    text_content: str
    audio_content: bytes


@dataclass
class CoordContent:
    coord_content: str
