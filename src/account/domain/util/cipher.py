import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from src.shared_kernel.infra.fastapi.config import settings


class CipherManager:
    def __init__(self) -> None:
        dek = bytes(settings.DEK_KEY, 'utf-8')
        self.BLOCK_SIZE = 16
        self.aes = AES.new(dek, AES.MODE_ECB)

    def encrypt_password(self, origin_pw: str) -> bytes:
        """Encrypt password using pycryptodome"""
        encoding_pw = pad(origin_pw.encode(), self.BLOCK_SIZE)
        encrypt_pw = self.aes.encrypt(encoding_pw)
        return base64.b64encode(encrypt_pw)

    def decrypt_password(self, encrypt_pw: bytes) -> str:
        """Decrypt password using pycryptodome"""
        decrypt_pw = self.aes.decrypt(base64.b64decode(encrypt_pw))
        origin_pw = unpad(decrypt_pw, self.BLOCK_SIZE).decode()
        return origin_pw
