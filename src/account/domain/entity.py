from dataclasses import dataclass


@dataclass
class AccountInfo:
    id: str
    password: str
    name: str
    gender: str
    age: str
    status: str = True

@dataclass
class UserInfo:
    id: str
    password: str = ""


@dataclass
class TokenInfo:
    id: str
    token: str
