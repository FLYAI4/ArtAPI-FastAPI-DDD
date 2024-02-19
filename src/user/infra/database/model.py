from src.shared_kernel.infra.database.model import Base
from sqlalchemy import Column, Integer, String


class Content(Base):
    __tablename__ = 'user_content'

    seq = Column(Integer, primary_key=True)
    id = Column(String(500), nullable=False)
    generated_id = Column(String(500), nullable=False)
