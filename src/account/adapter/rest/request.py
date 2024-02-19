import pydantic


class SignUpUserRequest(pydantic.BaseModel):
    id: str
    password: str
    name: str
    gender: str
    age: str


class LogInUserRequest(pydantic.BaseModel):
    id: str
    password: str
