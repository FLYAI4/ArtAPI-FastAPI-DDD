import pymongo
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.shared_kernel.adapter.database_abs import DBManager
from src.shared_kernel.infra.fastapi.config import settings
from azure.storage.blob import BlobServiceClient


class PostgreManager(DBManager):
    @staticmethod
    def get_session():
        engin = create_engine(
            settings.POSTGRESQL_CONNECTION_URL + settings.DB_NAME,
            pool_size=5,
            pool_recycle=100,
            max_overflow=10
        )
        return Session(engin)


class MongoManager(DBManager):
    @staticmethod
    def get_session():
        session = pymongo.MongoClient(
            settings.MONGO_CONNECTION_URL
        )
        return session[settings.DB_NAME]


class BlobStorageManager(DBManager):
    @staticmethod
    def get_session():
        session = BlobServiceClient.from_connection_string(
            settings.AZURE_BLOB_STORAGE_CONNECTION_URL
        )
        return session
