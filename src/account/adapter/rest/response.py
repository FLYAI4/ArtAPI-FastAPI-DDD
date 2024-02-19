import pydantic
from src.account.domain.entity import UserInfo, TokenInfo
from src.shared_kernel.infra.fastapi.util import make_response
from dataclasses import asdict


class SignUpUserResponse(pydantic.BaseModel):
    user_info: UserInfo

    def build(self):
        return make_response(
            {"id": self.user_info.id}
        )
    

class LogInUserResponse(pydantic.BaseModel):
    token_info: TokenInfo

    def build(self):
        return make_response(
            asdict(self.token_info)
        )
