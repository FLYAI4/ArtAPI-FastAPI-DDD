from enum import Enum
from starlette import status


class RepositoryError(Enum):
    DBProcess = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }
    DBNoNExist = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Not created."
    }


class TokenError(Enum):
    ExpireTokenError = {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "Please log in again",
        "log": "Token expire error"
    }
    WrongTokenError = {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "Not allow access. Please log in again",
        "log": "Wrong token error"
    }
    UnknownTokenError = {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "Not allow access. Please log in again",
        "log": "Wrong access error"
    }
