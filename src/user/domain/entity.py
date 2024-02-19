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
class GeneratedIdInfo:
    id: str
    generated_id: str
