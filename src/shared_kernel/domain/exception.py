class BaseHttpException(Exception):
    def __init__(self, code: int, message: str, log: str) -> None:
        self.code = code
        self.message = message
        self.log = log
        self.error = None


class DBError(BaseHttpException):
    def __init__(
            self, code: int, message: str, log: str, err: Exception = None
            ) -> None:
        super().__init__(code, message, log)
        self.error = err


class AuthError(BaseHttpException):
    def __init__(
            self, code: int, message: str, log: str, err: Exception = None
            ) -> None:
        super().__init__(code, message, log)
        self.error = err
