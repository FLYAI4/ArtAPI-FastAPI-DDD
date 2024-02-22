from enum import Enum
from starlette import status


class InsertImageError(Enum):
    NonRetrievalImage = {
        "code": status.HTTP_405_METHOD_NOT_ALLOWED,
        "message": "The image not allowed. Please picture again.",
        "log": "Image not match on DB."
    }
    UnknownError = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Please contact administrator.",
        "log": "Insert image unknown error. Please check the server."
    }
