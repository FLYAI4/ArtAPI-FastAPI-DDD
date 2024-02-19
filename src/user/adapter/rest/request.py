import pydantic


class InsertImageRequest(pydantic.BaseModel):
    id: str
    image_file: bytes
