from enum import Enum
from starlette import status


class RepositoryError(Enum):
    DBProcess = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }
