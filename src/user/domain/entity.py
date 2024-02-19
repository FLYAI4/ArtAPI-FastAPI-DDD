from dataclasses import dataclass


@dataclass
class OriginImageInfo:
    id: str
    image_file: bytes


@dataclass
class FileInfo:
    path: str
