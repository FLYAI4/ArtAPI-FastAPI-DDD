from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from src.account.adapter.rest.request import SignUpUserRequest, LogInUserRequest
from src.account.application.command import AccountCommandUseCase
from src.account.adapter.rest.response import SignUpUserResponse, LogInUserResponse
from src.shared_kernel.infra.container import AppContainer

account = APIRouter(prefix="/account")


@account.post("/signup")
@inject
async def user_signup(
    requst: SignUpUserRequest,
    account_command: AccountCommandUseCase = Depends(
        Provide[AppContainer.account.account_command]
    ),
):
    # print(account_command)
    user_info = account_command.sign_up_user(requst)
    return SignUpUserResponse(user_info=user_info).build()


@account.post("/login")
@inject
async def user_login(
    requst: LogInUserRequest,
    account_command: AccountCommandUseCase = Depends(
        Provide[AppContainer.account.account_command]
    ),
):
    token_info = account_command.log_in_user(requst)
    return LogInUserResponse(token_info=token_info).build()
