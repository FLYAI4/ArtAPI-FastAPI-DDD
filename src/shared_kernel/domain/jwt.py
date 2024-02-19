import os
import jwt
from datetime import datetime, timedelta
from src.shared_kernel.infra.fastapi.config import settings


class TokenManager:
    def __init__(self) -> None:
        self.TOKEN_KEY = settings.TOKEN_KEY

    def create_token(self, id: str):
        """Create token using jwt"""
        return jwt.encode({
                "id": id,
                "exp": datetime.utcnow() + timedelta(hours=5)
            }, self.TOKEN_KEY, algorithm="HS256")

    def decode_token(self, token: str):
        """Decode token using jwt"""
        return jwt.decode(token, self.TOKEN_KEY, algorithms="HS256")
