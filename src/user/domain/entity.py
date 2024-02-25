from dataclasses import dataclass


@dataclass
class OriginImageInfo:
    id: str
    image_file: bytes


@dataclass
class FileInfo:
    unique_id: str
    path: str


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
