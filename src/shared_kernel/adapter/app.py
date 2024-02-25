from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.account.adapter.rest.api import account
from src.user.adapter.rest.api import user
from src.admin.adapter.rest.api import admin
from src.shared_kernel.infra.fastapi.error_handler import error_handlers


def create_app():
    app = FastAPI()

    # Router
    app.include_router(account)
    app.include_router(user)
    app.include_router(admin)

    # Handler
    error_handlers(app)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
