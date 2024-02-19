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


@dataclass
class GeneratedContent:
    generated_id: str
    tag: str
    content: bytes = None


@dataclass
class GeneratedContentModel:
    id: str
    generated_id: str
    text_content: GeneratedContent
    coord_content: GeneratedContent
