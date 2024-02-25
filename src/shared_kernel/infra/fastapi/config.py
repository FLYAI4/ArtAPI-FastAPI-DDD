import os
from typing import ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class EnvSettings(BaseSettings):
    POSTGRESQL_CONNECTION_URL: ClassVar[str] = os.environ.get(
        'POSTGRESQL_CONNECTION_URL'
        )
    DB_NAME: ClassVar[str] = os.environ.get('DB_NAME')
    DEK_KEY: ClassVar[str] = os.environ.get('DEK_KEY')
    TOKEN_KEY: ClassVar[str] = os.environ.get('TOKEN_KEY')
    MONGO_CONNECTION_URL: ClassVar[str] = os.environ.get(
        'MONGO_CONNECTION_URL'
        )
    AZURE_BLOB_STORAGE_CONNECTION_URL:  ClassVar[str] = os.environ.get(
        'AZURE_BLOB_STORAGE_CONNECTION_URL'
        )


settings = EnvSettings()
