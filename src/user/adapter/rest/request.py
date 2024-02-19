import pydantic


class GeneratedContentRequest(pydantic.BaseModel):
    generated_id: str
