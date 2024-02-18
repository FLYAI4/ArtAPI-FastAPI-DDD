from src.shared_kernel.infra.database.model import Base
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary


class Account(Base):
    __tablename__ = 'user_account'

    seq = Column(Integer, primary_key=True)
    id = Column(String(500), nullable=False)
    password = Column(LargeBinary, nullable=False)
    name = Column(String(500), nullable=False)
    gender = Column(String(20), nullable=False)
    age = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
