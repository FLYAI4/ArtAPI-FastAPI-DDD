from enum import Enum


class RepositoryError(Enum):
    DBProcess = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }


class SignUpError(Enum):
    NonMatchEmail = {
        "code": 401,
        "message": "The ID is not in email format. Please enter again.",
        "log": "User service sign up fail with wrong email."
    }
    AlreadyUserError = {
        "code": 401,
        "message": "The user email is already created. Please sign up another email.",
        "log": "User service sign up fail with already existence email."
    }


class LogInError(Enum):
    NonSignupError = {
        "code": 401,
        "message": "This account is not registered. Please sign up.",
        "log": "User request fail with non sign account."
    }
    WrongPasswordError = {
        "code": 401,
        "message": "The password is incorrect. Please check again..",
        "log": "User request fail with wrong password."
    }