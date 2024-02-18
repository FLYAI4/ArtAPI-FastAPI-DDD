from dataclasses import dataclass


@dataclass
class AccountInfo:
    id: str
    password: str
    name: str
    gender: str
    age: str


@dataclass
class UserInfo:
    id: str
    password: str
