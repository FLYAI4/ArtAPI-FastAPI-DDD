from fastapi import Request
from src.shared_kernel.domain.exception import BaseHttpException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.shared_kernel.infra.fastapi.logger import Logger


def error_handlers(app) -> JSONResponse:
    @app.exception_handler(BaseHttpException)
    async def http_custom_exception_handler(
        request: Request,
        exc: BaseHttpException
    ):
        content = {
            "meta": {
                "code": exc.code,
                "error": str(exc.error),
                "message": exc.message
            },
            "data": None
        }
        Logger("ERROR", str(exc.error))
        return JSONResponse(
            status_code=exc.code,
            content=content
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        content = {
            "meta": {
                "code": 422,
                "error": str(exc.errors),
                "message": "A required value is missing. Please check."
            },
            "data": None
        }
        Logger("INFO", str(exc.errors))
        return JSONResponse(
            status_code=422,
            content=content
        )
