from enum import Enum


class RepositoryError(Enum):
    DBProcess = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }
