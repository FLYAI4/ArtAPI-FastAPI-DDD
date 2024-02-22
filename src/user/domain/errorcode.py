from enum import Enum


class InsertImageError(Enum):
    NonRetrievalImage = {
        "code": 405,
        "message": "The image not allowed. Please picture again.",
        "log": "Image not match on DB."
    }
    UnknownError = {
        "code": 500,
        "message": "Please contact administrator.",
        "log": "Insert image unknown error. Please check the server."
    }
