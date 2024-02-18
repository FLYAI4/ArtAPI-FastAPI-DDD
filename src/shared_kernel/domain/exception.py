class BaseHttpException(Exception):
    def __init__(self, code: int, message: str, log: str) -> None:
        self.code = code
        self.message = message
        self.log = log
        self.error = None
