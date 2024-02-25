import pydantic
from src.admin.domain.entity import GeneratedContentName
from src.shared_kernel.infra.fastapi.util import make_response


class GeneratedContentResponse(pydantic.BaseModel):
    generated_content_name: GeneratedContentName

    def build(self):
        return make_response(
            {"image_name": self.generated_content_name.image_name}
        )
