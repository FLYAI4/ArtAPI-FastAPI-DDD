from src.shared_kernel.domain.exception import BaseHttpException


class UserServiceError(BaseHttpException):
    def __init__(
            self, code: int, message: str, log: str, err: Exception = None
            ) -> None:
        super().__init__(code, message, log)
        self.error = err


class UserApplicationError(BaseHttpException):
    def __init__(
            self, code: int, message: str, log: str, err: Exception = None
            ) -> None:
        super().__init__(code, message, log)
        self.error = err
