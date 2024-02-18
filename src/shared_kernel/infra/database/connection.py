from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.shared_kernel.adapter.database_abs import DBManager
from src.shared_kernel.infra.fastapi.config import settings


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
