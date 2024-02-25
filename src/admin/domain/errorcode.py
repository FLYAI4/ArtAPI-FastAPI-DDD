from enum import Enum
from starlette import status


class GeneratedContentsError(Enum):
    AlreadyExistenceImage = {
        "code": status.HTTP_405_METHOD_NOT_ALLOWED,
        "message": "The image name already existence",
        "log": "Image already existence"
    }
    UnKnowError = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Unknown error.",
        "log": "Unknown error."
    }
