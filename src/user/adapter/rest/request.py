import pydantic


class InsertUserContentReview(pydantic.BaseModel):
    like_satus: bool
    review_content: str
