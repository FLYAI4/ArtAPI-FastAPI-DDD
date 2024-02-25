import pydantic


class InsertUserContentReview(pydantic.BaseModel):
    like_status: bool
    review_content: str
