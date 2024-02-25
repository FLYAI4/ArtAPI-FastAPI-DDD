import jwt
from fastapi import Header
from src.shared_kernel.domain.jwt import TokenManager
from src.shared_kernel.domain.exception import AuthError
from src.shared_kernel.domain.error_code import TokenError


async def get_current_user(
        id: str = Header(...),
        token: str = Header(...),
):
    try:
        payload = TokenManager().decode_token(token)
        if payload["id"] != id:
            raise AuthError(**TokenError.WrongTokenError.value)
    except jwt.ExpiredSignatureError:
        raise AuthError(**TokenError.ExpireTokenError.value)
    except Exception:
        raise AuthError(**TokenError.UnknownTokenError.value)
