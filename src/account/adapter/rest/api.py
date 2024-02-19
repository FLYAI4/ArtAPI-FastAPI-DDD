from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.account.adapter.rest.request import SignUpUserRequest, LogInUserRequest
from src.account.infra.database.repository import AccountRepository
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.application.command import AccountCommandUseCase
from src.account.adapter.rest.response import SignUpUserResponse, LogInUserResponse


account = APIRouter(prefix="/account")


@account.post("/signup")
def user_signup(
    requst: SignUpUserRequest,
    session: Session = Depends(PostgreManager().get_session)
):
    command = AccountCommandUseCase(AccountRepository, session)
    user_info = command.sign_up_user(requst)
    return SignUpUserResponse(user_info=user_info).build()


@account.post("/login")
def user_login(
    requst: LogInUserRequest,
    session: Session = Depends(PostgreManager().get_session)
):
    command = AccountCommandUseCase(AccountRepository, session)
    token_info = command.log_in_user(requst)
    return LogInUserResponse(token_info=token_info).build()
