import pydantic
from src.user.domain.entity import FileInfo
from src.shared_kernel.infra.fastapi.util import make_response


class SignUpUserResponse(pydantic.BaseModel):
    file_info: FileInfo

    def build(self):
        return make_response(
            {"generated_id": self.file_info.unique_id}
        )
